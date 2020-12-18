from abc import ABC, abstractmethod


class BaseCameraModule(ABC):
    """Abstract class containing common image capture related code"""

    def __init__(self, file_extension, needs_raw_folder=False):
        self.file_extension = file_extension
        self.need_raw_folder = needs_raw_folder

    @abstractmethod
    def try_capture_image(self, image_path, raw_file_folder=None):
        """Method for capturing image and storing it in image_path. Should
        raise ImageCaptureError with and error message if something
        goes wrong with capture.
        """
        pass


class ImageCaptureError(RuntimeError):
    pass
