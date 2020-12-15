from PIL import Image
from .base_album import BaseAlbum
from .folder import Folder
from .image_name_formatter import ImageNameFormatter
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

    def get_album_description(self):
        if not self.album_folder.file_exists_in_folder("description.txt"):
            return ""

        return self.album_folder.read_file_in_folder("description.txt")

    def set_album_description(self, content):
        self.album_folder.write_file_in_folder("description.txt", content)

    def get_relative_url_of_last_image(self):
        """Returns the url of the last image captured to the album."""
        current_image_number = self.__get_current_image_number()
        if current_image_number == 0:
            return None

        if self.__image_with_number_and_extension_exists(current_image_number, ".jpg"):
            image_filename = self.image_name_formatter.format_name(current_image_number, ".jpg")
            return self.images_folder.get_relative_url_to_file(image_filename)

        if self.__image_with_number_and_extension_exists(current_image_number, ".png"):
            image_filename = self.image_name_formatter.format_name(current_image_number, ".png")
            return self.images_folder.get_relative_url_to_file(image_filename)

    def get_relative_urls_of_all_images(self):
        return self.images_folder.get_relative_urls_to_all_files()

    def get_relative_urls_of_all_thumbnails(self):
        return self.thumbnails_folder.get_relative_urls_to_all_files()

    def try_capture_image_to_album(self, camera_module):
        next_image_number = self.__get_current_image_number() + 1
        next_image_name = self.image_name_formatter.format_name(
            next_image_number,
            camera_module.file_extension
        )

        next_image_filepath = self.images_folder.get_path_to_file(next_image_name)
        camera_module.try_capture_image(next_image_filepath)

        self.__create_thumbnail_for_image(next_image_name)
        self.__set_current_image_number(next_image_number)

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

    def __current_image_number_file_exists(self):
        return self.album_folder.file_exists_in_folder(".image_number.txt")

    def __set_current_image_number(self, image_number):
        self.album_folder.write_file_in_folder(".image_number.txt", str(image_number))

    def __ensure_current_image_number_file_exists(self):
        if not self.__current_image_number_file_exists():
            self.__set_current_image_number(0)

    def __image_with_number_and_extension_exists(self, image_number, extension):
        possible_file_name = self.image_name_formatter.format_name(image_number, extension)

        if self.images_folder.file_exists_in_folder(possible_file_name):
            return True

    def __image_with_image_number_exists(self, image_number):
        if self.__image_with_number_and_extension_exists(image_number, ".jpg"):
            return True

        if self.__image_with_number_and_extension_exists(image_number, ".png"):
            return True

        return False

    def __current_image_number_correct(self):
        current_image_number = int(self.album_folder.read_file_in_folder(".image_number.txt"))
        if not self.__image_with_image_number_exists(current_image_number):
            return False

        next_image_number = current_image_number + 1
        if self.__image_with_image_number_exists(next_image_number):
            return False

        return True

    def __get_image_number_from_filename(self, filename):
        """Example: if the name is image_0042.png, should return 42"""
        return int(filename[-8:-4])

    def __recreate_current_image_number_file(self):
        """Recreates the image number file based on the image files present"""
        image_names = self.images_folder.get_sorted_folder_contents()
        if not image_names:
            image_number = 0
        else:
            last_name = image_names[-1]
            image_number = self.__get_image_number_from_filename(last_name)

        self.__set_current_image_number(image_number)

    def __ensure_current_image_number_file_correct(self):
        if not self.__current_image_number_correct():
            self.__recreate_current_image_number_file()

    def __get_current_image_number(self):
        self.__ensure_current_image_number_file_exists()
        self.__ensure_current_image_number_file_correct()
        return int(self.album_folder.read_file_in_folder(".image_number.txt"))

    def __create_thumbnail(self, input_path, output_path):
        image = Image.open(input_path)
        image = image.convert('RGB')
        image.thumbnail(MAX_THUMBNAIL_SIZE)
        image.save(output_path)

    def __create_thumbnail_for_image(self, image_name):
        # All thumbnails are saved as .jpg
        thumbnail_name = self.image_name_formatter.change_extension_of_filename(image_name, ".jpg")
        thumbnail_path = self.thumbnails_folder.get_path_to_file(thumbnail_name)
        image_path = self.images_folder.get_path_to_file(image_name)
        self.__create_thumbnail(image_path, thumbnail_path)
