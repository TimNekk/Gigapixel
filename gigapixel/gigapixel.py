import os
from enum import Enum
from typing import Optional, Dict, Any
from pathlib import Path

from .logging import log, Level
from .exceptions import NotFile, FileAlreadyExists, ElementNotFound

from pywinauto import ElementNotFoundError, timings
import clipboard
from loguru import logger
from pywinauto.application import Application, ProcessNotFoundError
from pywinauto.keyboard import send_keys


class Scale(Enum):
    X05 = "0.5x"
    X2 = "2x"
    X4 = "4x"
    X6 = "6x"


class Mode(Enum):
    STANDARD = "Standard"
    Lines = "Lines"
    ART_AND_CG = "Art & CG"
    HIGH_QUALITY = "HQ"
    LOW_RESOLUTION = "Low Res"
    VERY_COMPRESSED = "Very Compressed"


class OutputFormat(Enum):
    PRESERVE_SOURCE_FORMAT = "Preserve Source Format"
    JPG = "JPG"
    JPEG = "JPEG"
    TIF = "TIF"
    TIFF = "TIFF"
    PNG = "PNG"
    DNG = "DNG"


class Gigapixel:
    def __init__(self,
                 executable_path: Path,
                 output_suffix: str,
                 processing_timeout: int = 900):
        """
        :param executable_path: Path to the executable (Topaz Gigapixel AI.exe)
        :param output_suffix: Suffix to be added to the output file name (e.g. pic.jpg -> pic-gigapixel.jpg)
        :param processing_timeout: Timeout for processing in seconds
        """
        self._executable_path = executable_path
        self._output_suffix = output_suffix

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
            self._delete_button: Optional[Any] = None
            self._output_combo_box: Optional[Any] = None
            self._preserve_source_format_button: Optional[Any] = None
            self._jpg_button: Optional[Any] = None
            self._jpeg_button: Optional[Any] = None
            self._tif_button: Optional[Any] = None
            self._tiff_button: Optional[Any] = None
            self._png_button: Optional[Any] = None
            self._dng_button: Optional[Any] = None
            self._scale_buttons: Dict[Scale, Any] = {}
            self._mode_buttons: Dict[Mode, Any] = {}

        @log("Opening photo: {}", "Photo opened", format=(1,), level=Level.DEBUG)
        def open_photo(self, photo_path: Path) -> None:
            while photo_path.name not in self._main_window.element_info.name:
                logger.debug("Trying to open photo")
                self._main_window.set_focus()
                send_keys('{ESC}^o')
                clipboard.copy(str(photo_path))
                send_keys('^v {ENTER}')

        @log("Saving photo", "Photo saved", level=Level.DEBUG)
        def save_photo(self, output_format: Optional[OutputFormat]) -> None:
            send_keys('^S')

            if output_format:
                self._set_output_format(output_format)

            send_keys('{ENTER}')
            if self._cancel_processing_button is None:
                self._cancel_processing_button = self._main_window.child_window(title="Cancel Processing",
                                                                                control_type="Button",
                                                                                depth=1)
            self._cancel_processing_button.wait_not('visible', timeout=self._processing_timeout)

        @log("Deleting photo from history", "Photo deleted", level=Level.DEBUG)
        def delete_photo(self) -> None:
            if self._delete_button is None:
                self._delete_button = self._main_window.Pane.Button2
            self._delete_button.click_input()

        @log("Setting processing options", "Processing options set", level=Level.DEBUG)
        def set_processing_options(self, scale: Optional[Scale] = None, mode: Optional[Mode] = None) -> None:
            if scale:
                self._set_scale(scale)
            if mode:
                self._set_mode(mode)

        def _set_output_format(self, save_format: OutputFormat) -> None:
            if self._output_combo_box is None:
                self._output_combo_box = self._main_window.ComboBox
            self._output_combo_box.click_input()

            if save_format == OutputFormat.PRESERVE_SOURCE_FORMAT:
                if self._preserve_source_format_button is None:
                    self._preserve_source_format_button = self._main_window.ListItem
                self._preserve_source_format_button.click_input()
                send_keys('{TAB}')
            elif save_format == OutputFormat.JPG:
                if self._jpg_button is None:
                    self._jpg_button = self._main_window.ListItem2
                self._jpg_button.click_input()
                send_keys('{TAB}')
            elif save_format == OutputFormat.JPEG:
                if self._jpeg_button is None:
                    self._jpeg_button = self._main_window.ListItem3
                self._jpeg_button.click_input()
                send_keys('{TAB}')
            elif save_format == OutputFormat.TIF:
                if self._tif_button is None:
                    self._tif_button = self._main_window.ListItem4
                self._tif_button.click_input()
                send_keys('{TAB} {TAB} {TAB}')
            elif save_format == OutputFormat.TIFF:
                if self._tiff_button is None:
                    self._tiff_button = self._main_window.ListItem5
                self._tiff_button.click_input()
                send_keys('{TAB} {TAB} {TAB}')
            elif save_format == OutputFormat.PNG:
                if self._png_button is None:
                    self._png_button = self._main_window.ListItem6
                self._png_button.click_input()
                send_keys('{TAB}')
            elif save_format == OutputFormat.DNG:
                if self._dng_button is None:
                    self._dng_button = self._main_window.ListItem7
                self._dng_button.click_input()
                send_keys('{TAB}')

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
    def _check_path(self, path: Path, output_format: Optional[OutputFormat]) -> None:
        if not path.is_file():
            raise NotFile(f"Path is not a file: {path}")

        save_path = self._get_save_path(path, output_format)
        if save_path.name in os.listdir(path.parent):
            raise FileAlreadyExists(f"Output file already exists: {save_path}")

    @staticmethod
    def _remove_suffix(input_string: str, suffix: str) -> str:
        if suffix and input_string.endswith(suffix):
            return input_string[:-len(suffix)]
        return input_string

    def _get_save_path(self, path: Path, output_format: Optional[OutputFormat]) -> Path:
        extension = path.suffix if output_format is None or output_format == OutputFormat.PRESERVE_SOURCE_FORMAT else \
            f".{output_format.value.lower()}"
        return path.parent / (Gigapixel._remove_suffix(path.name, path.suffix) + self._output_suffix + extension)

    @log(start="Starting processing: {}", format=(1,))
    @log(end="Finished processing: {}", format=(1,), level=Level.SUCCESS)
    def process(self,
                photo_path: Path,
                scale: Optional[Scale] = None,
                mode: Optional[Mode] = None,
                delete_from_history: bool = False,
                output_format: Optional[OutputFormat] = None
                ) -> Path:
        """
        Process a photo using Topaz Gigapixel AI

        :param photo_path: Path to the photo to be processed
        :param scale: Scale to be used for processing
        :param mode: Mode to be used for processing
        :param delete_from_history: Whether to delete the photo from history after processing
        :param output_format: Output format of the processed photo
        :return: Path to the processed photo
        """
        self._check_path(photo_path, output_format)

        self._app.open_photo(photo_path)
        self._app.set_processing_options(scale, mode)
        self._app.save_photo(output_format)

        if delete_from_history:
            self._app.delete_photo()

        return self._get_save_path(photo_path, output_format)
