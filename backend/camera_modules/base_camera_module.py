from abc import ABC, abstractmethod


class BaseCameraModule(ABC):
    """Abstract class containing common image capture related code"""

    def __init__(self, file_extension, needs_raw_file_transfer=False, raw_file_extension=None):
        self.file_extension = file_extension
        self.needs_raw_file_transfer = needs_raw_file_transfer
        self.raw_file_extension = raw_file_extension

    @abstractmethod
    def try_capture_image(self, image_path, raw_file_path=None):
        """Method for capturing image and storing it in image_path. Should
        raise ImageCaptureError with and error message if something
        goes wrong with capture.

        The raw_file_path should be specified if
        needs_raw_file_transfer is true and raw_file_extension is
        given.
        """
        pass


class ImageCaptureError(RuntimeError):
    pass
