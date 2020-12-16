from abc import ABC, abstractmethod


class BaseAlbum(ABC):
    """Base class for album-related storage of images"""

    @abstractmethod
    def get_album_description(self):
        pass

    @abstractmethod
    def set_album_description(self, content):
        pass

    @abstractmethod
    def get_relative_url_of_last_image(self):
        pass

    @abstractmethod
    def get_relative_urls_of_all_images(self):
        pass

    @abstractmethod
    def get_relative_urls_of_all_thumbnails(self):
        pass

    @abstractmethod
    def try_capture_image_to_album(self, camera_module):
        pass

    @abstractmethod
    def ensure_thumbnails_correct(self):
        pass
