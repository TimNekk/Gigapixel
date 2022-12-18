import os
from enum import Enum
from typing import Optional
from pathlib import Path

from .logging import log, Level
from .exceptions import NotFile, FileAlreadyExists, ElementNotFound

from pywinauto import ElementNotFoundError
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
    LOW_RESOLUTION = "Low Resolution"
    VERY_COMPRESSED = "Very Compressed"


class Gigapixel:
    def __init__(self,
                 executable_path: Path,
                 output_suffix: str):
        self._executable_path = executable_path
        self._output_suffix = output_suffix

        instance = self._get_gigapixel_instance()
        self._app = self.App(instance)

    class App:
        def __init__(self, app: Application):
            self._app = app
            self._main_window = self._app.window()

            self.scale: Optional[Scale] = None
            self.mode: Optional[Mode] = None

        @log("Opening photo: {}", "Photo opened", format=(1,), level=Level.DEBUG)
        def open_photo(self, photo_path: Path) -> None:
            while photo_path.name not in self._main_window.element_info.name:
                logger.debug("Trying to open photo")
                self._main_window.set_focus()
                send_keys('{ESC}^o')
                clipboard.copy(str(photo_path))
                send_keys('^v {ENTER}')

        @log("Saving photo", "Photo saved", level=Level.DEBUG)
        def save_photo(self) -> None:
            send_keys('^S {ENTER}')
            self._main_window.child_window(title="Cancel Processing", control_type="Button").wait_not('visible',
                                                                                                      timeout=60)

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
                self._main_window.child_window(title=scale.value).click_input()
            except ElementNotFoundError:
                raise ElementNotFound(f"Scale button {scale.value} not found")
            self.scale = scale
            logger.debug(f"Scale set to {scale.value}")

        def _set_mode(self, mode: Mode) -> None:
            if self.mode == mode:
                return

            try:
                self._main_window.child_window(title=mode.value).click_input()
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

        save_path = self._get_save_path(path)
        if save_path.name in os.listdir(path.parent):
            raise FileAlreadyExists(f"Output file already exists: {save_path}")

    @staticmethod
    def _remove_suffix(input_string: str, suffix: str) -> str:
        if suffix and input_string.endswith(suffix):
            return input_string[:-len(suffix)]
        return input_string

    def _get_save_path(self, path: Path) -> Path:
        return path.parent / (Gigapixel._remove_suffix(path.name, path.suffix) + self._output_suffix + path.suffix)

    @log(start="Starting processing: {}", format=(1,))
    @log(end="Finished processing: {}", format=(1,), level=Level.SUCCESS)
    def process(self, photo_path: Path, scale: Scale = Scale.X2, mode: Mode = Mode.STANDARD) -> Path:
        self._check_path(photo_path)

        self._app.open_photo(photo_path)
        self._app.set_processing_options(scale, mode)
        self._app.save_photo()

        return self._get_save_path(photo_path)
