from abc import ABC, abstractmethod


class BaseAlbumHandler(ABC):
    """Base class for creating Album Class instances"""

    @abstractmethod
    def get_available_album_names(self):
        pass

    @abstractmethod
    def get_album(self, album_name):
        pass

    @abstractmethod
    def get_or_create_album(self, album_name, description=""):
        pass

    @abstractmethod
    def ensure_all_thumbnails_correct(self):
        pass
