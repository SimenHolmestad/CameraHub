from .base_album_handler import BaseAlbumHandler
from .folder_album import FolderAlbum
from .folder import Folder


class FolderAlbumHandler(BaseAlbumHandler):
    """An AlbumHandler implementation for handling FolderAlbums"""

    def __init__(self, base_path, folder_for_albums_name):
        self.folder_for_albums = Folder(base_path, folder_for_albums_name)

    def get_available_album_names(self):
        return self.folder_for_albums.get_folder_contents()

    def get_album(self, album_name):
        if album_name in self.get_available_album_names():
            return FolderAlbum(album_name, self.folder_for_albums.get_path())

        raise AlbumNotFoundError()

    def get_or_create_album(self, album_name, description=""):
        album = FolderAlbum(album_name, self.folder_for_albums.get_path())
        if description != "":
            album.set_album_description(description)
        return album

    def album_exists(self, album_name):
        return self.folder_for_albums.file_exists_in_folder(album_name)

    def ensure_all_thumbnails_correct(self):
        album_names = self.get_available_album_names()
        for name in album_names:
            album = self.get_album(name)
            album.ensure_thumbnails_correct()


class AlbumNotFoundError(RuntimeError):
    pass
