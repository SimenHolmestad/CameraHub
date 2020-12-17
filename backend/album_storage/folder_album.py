from PIL import Image
from .base_album import BaseAlbum
from .folder import Folder
from .image_name_formatter import ImageNameFormatter
from .current_image_tracker import CurrentImageTracker
MAX_THUMBNAIL_SIZE = (600, 600)


class FolderAlbum(BaseAlbum):
    """An Album implementation where all album-related information is
    stored in a single folder.
    """

    def __init__(self, album_name, path_to_album_folders, image_name_prefix="image"):
        self.album_folder = Folder(path_to_album_folders, album_name)
        self.images_folder = Folder(self.album_folder.get_path(), "images")
        self.thumbnails_folder = Folder(self.album_folder.get_path(), "thumbnails")
        self.image_name_formatter = ImageNameFormatter(image_name_prefix)
        self.current_image_tracker = CurrentImageTracker(
            self.album_folder,
            self.images_folder,
            self.image_name_formatter
        )

    def get_album_description(self):
        if not self.album_folder.file_exists_in_folder("description.txt"):
            return ""

        return self.album_folder.read_file_in_folder("description.txt")

    def set_album_description(self, content):
        self.album_folder.write_file_in_folder("description.txt", content)

    def get_relative_url_of_last_image(self):
        """Returns the url of the last image captured to the album."""
        last_image_filename = self.current_image_tracker.get_name_of_last_image()
        if not last_image_filename:
            return None  # This means album is empty

        return self.images_folder.get_relative_url_to_file(last_image_filename)

    def get_relative_url_of_last_thumbnail(self):
        """Returns the url of the last thumbnail captured to the album."""
        last_image_filename = self.current_image_tracker.get_name_of_last_image()
        if not last_image_filename:
            return None  # This means album is empty

        thumbnail_filename = self.__convert_image_name_to_thumbnail_name(last_image_filename)
        return self.thumbnails_folder.get_relative_url_to_file(thumbnail_filename)

    def get_relative_urls_of_all_images(self):
        return self.images_folder.get_relative_urls_to_all_files()

    def get_relative_urls_of_all_thumbnails(self):
        return self.thumbnails_folder.get_relative_urls_to_all_files()

    def try_capture_image_to_album(self, camera_module):
        next_image_name = self.current_image_tracker.get_next_image_name(
            camera_module.file_extension
        )

        next_image_filepath = self.images_folder.get_path_to_file(next_image_name)
        camera_module.try_capture_image(next_image_filepath)

        self.__create_thumbnail_for_image(next_image_name)
        self.current_image_tracker.increase_image_number()

    def ensure_thumbnails_correct(self):
        self.thumbnails_folder.create_folder_if_not_exist()

        number_of_images = self.images_folder.count_files()
        number_of_thumbnails = self.thumbnails_folder.count_files()
        if not number_of_images == number_of_thumbnails:
            self.recreate_all_thumbnails()

    def recreate_all_thumbnails(self):
        self.thumbnails_folder.remove_all_folder_content()

        image_names = self.images_folder.get_folder_contents()
        for name in image_names:
            self.__create_thumbnail_for_image(name)

    def __create_thumbnail(self, input_path, output_path):
        image = Image.open(input_path)
        image = image.convert('RGB')
        image.thumbnail(MAX_THUMBNAIL_SIZE)
        image.save(output_path)

    def __create_thumbnail_for_image(self, image_name):
        # All thumbnails are saved as .jpg
        thumbnail_name = self.__convert_image_name_to_thumbnail_name(image_name)
        thumbnail_path = self.thumbnails_folder.get_path_to_file(thumbnail_name)
        image_path = self.images_folder.get_path_to_file(image_name)
        self.__create_thumbnail(image_path, thumbnail_path)

    def __convert_image_name_to_thumbnail_name(self, image_name):
        return self.image_name_formatter.change_extension_of_filename(image_name, ".jpg")
