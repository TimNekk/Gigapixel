from enum import Enum
from typing import Optional, Dict, Any, Union
from pathlib import Path
import win32api
import win32con

from .logging import log, Level
from .exceptions import NotFile, ElementNotFound

from pywinauto import ElementNotFoundError, timings
import clipboard
from loguru import logger
from pywinauto.application import Application, ProcessNotFoundError
from pywinauto.keyboard import send_keys
from pywinauto.timings import TimeoutError
from the_retry import retry


class Scale(Enum):
    X1 = "1x"
    X2 = "2x"
    X4 = "4x"
    X6 = "6x"


class Mode(Enum):
    STANDARD = "Standard"
    HIGH_FIDELITY = "High fidelity"
    LOW_RESOLUTION = "Low res"
    TEXT_AND_SHAPES = "Text & shapes"
    ART_AND_CG = "Art & CG"
    RECOVERY = "Recovery"


class Gigapixel:
    def __init__(self,
                 executable_path: Union[Path, str],
                 processing_timeout: int = 900) -> None:
        """
        :param executable_path: Path to the executable (Topaz Gigapixel AI.exe)
        :param processing_timeout: Timeout for processing in seconds
        """
        self._executable_path = executable_path
        if isinstance(executable_path, str):
            self._executable_path = Path(executable_path)

        instance = self._get_gigapixel_instance()
        self._app = self._App(instance, processing_timeout)

    class _App:
        def __init__(self, app: Application, processing_timeout: int):
            timings.Timings.window_find_timeout = 0.5

            self.app = app
            self._processing_timeout = processing_timeout
            self._main_window = self.app.window()

            self.scale: Optional[Scale] = None
            self.mode: Optional[Mode] = None

            self._cancel_processing_button: Optional[Any] = None
            self._save_button: Optional[Any] = None
            self._scale_buttons: Dict[Scale, Any] = {}
            self._mode_buttons: Dict[Mode, Any] = {}

        @retry(
            expected_exception=(ElementNotFoundError,),
            attempts=5,
            backoff=0.5,
            exponential_backoff=True,
        )
        @log("Opening photo: {}", "Photo opened", format=(1,), level=Level.DEBUG)
        def open_photo(self, photo_path: Path) -> None:
            while photo_path.name not in self._main_window.element_info.name:
                logger.debug("Trying to open photo")
                self._main_window.set_focus()
                send_keys('{ESC}^o')
                clipboard.copy(str(photo_path))
                send_keys('^v {ENTER}{ESC}')
                

        @log("Saving photo", "Photo saved", level=Level.DEBUG)
        def save_photo(self) -> None:
            self._open_export_dialog()

            send_keys('{ENTER}')
            if self._cancel_processing_button is None:
                self._cancel_processing_button = self._main_window.child_window(title="Close window",
                                                                                control_type="Button",
                                                                                depth=1)
            self._cancel_processing_button.wait('visible', timeout=self._processing_timeout)

            self._close_export_dialog()

        @retry(
            expected_exception=(TimeoutError,),
            attempts=10,
            backoff=0.1,
            exponential_backoff=True,
        )
        @log("Opening export dialog", "Export dialog opened", level=Level.DEBUG)
        def _open_export_dialog(self) -> None:
            send_keys('^S')
            if self._save_button is None:
                self._save_button = self._main_window.child_window(title="Save", control_type="Button", depth=1)
            self._save_button.wait('visible', timeout=0.1)
        
        @retry(
            expected_exception=(TimeoutError,),
            attempts=10,
            backoff=0.1,
            exponential_backoff=True,
        )
        @log("Closing export dialog", "Export dialog closed", level=Level.DEBUG)
        def _close_export_dialog(self) -> None:
            send_keys('{ESC}')
            self._cancel_processing_button.wait_not('visible', timeout=0.1)

        @log("Setting processing options", "Processing options set", level=Level.DEBUG)
        def set_processing_options(self, scale: Optional[Scale] = None, mode: Optional[Mode] = None) -> None:
            if scale:
                self._set_scale(scale)
            if mode:
                self._set_mode(mode)

        def _set_scale(self, scale: Scale):
            if self.scale == scale:
                return

            try:
                if scale not in self._scale_buttons:
                    self._scale_buttons[scale] = self._main_window.child_window(title=scale.value)
                self._scale_buttons[scale].click_input()
            except ElementNotFoundError:
                raise ElementNotFound(f"Scale button {scale.value} not found")
            self.scale = scale
            logger.debug(f"Scale set to {scale.value}")

        def _set_mode(self, mode: Mode) -> None:
            if self.mode == mode:
                return

            try:
                if mode not in self._mode_buttons:
                    self._mode_buttons[mode] = self._main_window.child_window(title=mode.value)
                self._mode_buttons[mode].click_input()
            except ElementNotFoundError:
                raise ElementNotFound(f"Mode button {mode.value} not found")
            self.mode = mode
            logger.debug(f"Mode set to {mode.value}")

        def _print_elements(self):
            self._main_window.print_control_identifiers()

    @log(start="Getting Gigapixel instance...")
    @log(end="Got Gigapixel instance: {}", format=(-1,), level=Level.SUCCESS)
    def _get_gigapixel_instance(self) -> Application:
        try:
            instance = Application(backend="uia").connect(path=self._executable_path)
            return instance
        except ProcessNotFoundError:
            logger.debug("Gigapixel instance not found.")
            instance = self._open_topaz()
            return instance

    @log("Starting new Gigapixel instance...", "Started new Gigapixel instance: {}", format=(-1,), level=Level.DEBUG)
    def _open_topaz(self) -> Application:
        instance = Application(backend="uia").start(str(self._executable_path)).connect(path=self._executable_path)
        return instance

    @log("Checking path: {}", "Path is valid", format=(1,), level=Level.DEBUG)
    def _check_path(self, path: Path) -> None:
        if not path.is_file():
            raise NotFile(f"Path is not a file: {path}")

    @staticmethod
    def _remove_suffix(input_string: str, suffix: str) -> str:
        if suffix and input_string.endswith(suffix):
            return input_string[:-len(suffix)]
        return input_string
    
    def _set_english_layout(self) -> None:
        english_layout = 0x0409
        win32api.LoadKeyboardLayout(hex(english_layout), win32con.KLF_ACTIVATE)

    @log(start="Starting processing: {}", format=(1,))
    @log(end="Finished processing: {}", format=(1,), level=Level.SUCCESS)
    def process(self,
                photo_path: Union[Path, str],
                scale: Optional[Scale] = None,
                mode: Optional[Mode] = None,
                ) -> None:
        """
        Process a photo using Topaz Gigapixel AI

        :param photo_path: Path to the photo to be processed
        :param scale: Scale to be used for processing
        :param mode: Mode to be used for processing
        """
        if isinstance(photo_path, str):
            photo_path = Path(photo_path)
        
        self._set_english_layout()
        self._check_path(photo_path)

        self._app.open_photo(photo_path)
        self._app.set_processing_options(scale, mode)
        self._app.save_photo()
