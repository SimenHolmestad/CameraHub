from abc import ABC, abstractmethod


class BaseCameraModule(ABC):
    """Abstract class containing common image capture related code"""

    def __init__(self, file_extension, needs_raw_file_transfer=False, raw_file_extension=None):
        """needs_raw_file_transfer should only be True if the camera captures
        both jpg and raw and the raw file needs to be stored in the system"""
        self.file_extension = file_extension
        self.needs_raw_file_transfer = needs_raw_file_transfer
        self.raw_file_extension = raw_file_extension
        self.is_busy = False

    @abstractmethod
    def capture_image(self, image_path, raw_file_path=None):
        """Method for capturing image and storing it in image_path. Should
        raise ImageCaptureError with and error message if something
        goes wrong with capture.

        The raw_file_path will only be neeeded if
        needs_raw_file_transfer is set to true and raw_file_extension
        is given.
        """
        pass

    def try_capture_image(self, image_path, raw_file_path=None):
        if self.is_busy:
            raise ImageCaptureError("Camera is already in use")
        self.is_busy = True
        self.capture_image(image_path, raw_file_path)
        self.is_busy = False


class ImageCaptureError(RuntimeError):
    pass
