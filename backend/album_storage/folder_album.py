import os
import shutil
from PIL import Image
from .base_album import BaseAlbum
MAX_THUMBNAIL_SIZE = (600, 600)


class FolderAlbum(BaseAlbum):
    """An Album implementation where all album-related information is
    stored in a single folder.
    """

    def __init__(self, album_name, path_to_album_folders, image_name_prefix="image"):
        self.path_to_album_folders = path_to_album_folders
        self.album_name = album_name
        self.image_name_prefix = image_name_prefix
        self.path_to_album_folders_name = os.path.split(path_to_album_folders)[1]

        self.__ensure_correct_folder_structure()

    def get_album_description(self):
        if not self.__description_file_exists():
            return ""

        return self.__get_description_file_content()

    def set_album_description(self, content):
        self.__write_description_file(content)

    def get_relative_url_of_last_image(self):
        """Returns the url of the last image captured to the album."""
        current_image_number = self.__get_current_image_number()
        if current_image_number == 0:
            return None

        if self.__image_with_number_and_extension_exists(current_image_number, ".jpg"):
            image_filename = self.__format_image_name(current_image_number, ".jpg")
            return self.__create_relative_url_to_image_file(image_filename)

        if self.__image_with_number_and_extension_exists(current_image_number, ".png"):
            image_filename = self.__format_image_name(current_image_number, ".png")
            return self.__create_relative_url_to_image_file(image_filename)

    def get_relative_urls_of_all_images(self):
        image_filenames = self.__get_sorted_list_of_image_names()
        urls = list(map(
            lambda name: self.__create_relative_url_to_image_file(name),
            image_filenames
        ))
        return urls

    def get_relative_urls_of_all_thumbnails(self):
        image_filenames = self.__get_sorted_list_of_thumbnail_names()
        urls = list(map(
            lambda name: self.__create_relative_url_to_thumbnail_file(name),
            image_filenames
        ))
        return urls

    def try_capture_image_to_album(self, camera_module):
        next_image_number = self.__get_current_image_number() + 1
        next_image_name = self.__format_image_name(
            next_image_number,
            camera_module.file_extension
        )

        next_image_filepath = self.__get_image_path_from_name(next_image_name)
        camera_module.try_capture_image(next_image_filepath)

        self.__create_thumbnail_for_image(next_image_name)
        self.__set_current_image_number(next_image_number)

    def ensure_thumbnails_correct(self):
        self.__create_thumbnails_folder_if_not_exists()
        if not self.__count_images() == self.__count_thumbnails():
            self.recreate_all_thumbnails()

    def recreate_all_thumbnails(self):
        self.__delete_all_thumbnails()

        image_names = self.__get_all_image_names()
        for name in image_names:
            self.__create_thumbnail_for_image(name)

    # Private methods below

    def __get_path_to_album_folder(self):
        return os.path.join(
            self.path_to_album_folders,
            self.album_name
        )

    def __get_path_to_images_folder(self):
        return os.path.join(
            self.__get_path_to_album_folder(),
            "images"
        )

    def __get_path_to_thumbnails_folder(self):
        return os.path.join(
            self.__get_path_to_album_folder(),
            "thumbnails"
        )

    def __get_path_to_description_file(self):
        return os.path.join(
            self.__get_path_to_album_folder(),
            "description.txt"
        )

    def __get_path_to_current_image_number_file(self):
        return os.path.join(
            self.__get_path_to_album_folder(),
            ".current_image_number.txt"
        )

    def __current_image_number_file_exists(self):
        return os.path.exists(self.__get_path_to_current_image_number_file())

    def __get_current_image_number_file_content(self):
        with open(self.__get_path_to_current_image_number_file()) as f:
            return int(f.read())

    def __write_current_image_number_file(self, image_number):
        with open(self.__get_path_to_current_image_number_file(), "w") as f:
            f.write(str(image_number))

    def __set_current_image_number(self, image_number):
        self.__write_current_image_number_file(image_number)

    def __description_file_exists(self):
        return os.path.exists(self.__get_path_to_description_file())

    def __get_description_file_content(self):
        with open(self.__get_path_to_description_file()) as f:
            return f.read()

    def __write_description_file(self, content):
        with open(self.__get_path_to_description_file(), "w") as f:
            f.write(content)

    def __create_album_folder_if_not_exists(self):
        if not os.path.exists(self.__get_path_to_album_folder()):
            os.makedirs(self.__get_path_to_album_folder())

    def __create_images_folder_if_not_exists(self):
        images_folder_path = self.__get_path_to_images_folder()
        if not os.path.exists(images_folder_path):
            os.makedirs(images_folder_path)

    def __create_thumbnails_folder_if_not_exists(self):
        if not os.path.exists(self.__get_path_to_thumbnails_folder()):
            os.makedirs(self.__get_path_to_thumbnails_folder())

    def __ensure_correct_folder_structure(self):
        self.__create_album_folder_if_not_exists()
        self.__create_images_folder_if_not_exists()
        self.__create_thumbnails_folder_if_not_exists()

    def __ensure_current_image_number_file_exists(self):
        if not self.__current_image_number_file_exists():
            self.__write_current_image_number_file(0)

    def __image_with_number_and_extension_exists(self, image_number, extension):
        file_path = self.__create_image_filepath(image_number, extension)
        if os.path.exists(file_path):
            return True

    def __image_with_image_number_exists(self, image_number):
        if self.__image_with_number_and_extension_exists(image_number, ".jpg"):
            return True

        if self.__image_with_number_and_extension_exists(image_number, ".png"):
            return True

        return False

    def __current_image_number_correct(self):
        current_image_number = self.__get_current_image_number_file_content()
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
        image_names = self.__get_sorted_list_of_image_names()
        if not image_names:
            image_number = 0
        else:
            last_name = image_names[-1]
            image_number = self.__get_image_number_from_filename(last_name)

        self.__write_current_image_number_file(image_number)

    def __ensure_current_image_number_file_correct(self):
        if not self.__current_image_number_correct():
            self.__recreate_current_image_number_file()

    def __get_current_image_number(self):
        self.__ensure_current_image_number_file_exists()
        self.__ensure_current_image_number_file_correct()
        return self.__get_current_image_number_file_content()

    def __format_image_name(self, image_number, file_extension):
        return self.image_name_prefix + str(image_number).rjust(4, "0") + file_extension

    def __get_image_path_from_name(self, image_name):
        return os.path.join(
            self.__get_path_to_images_folder(),
            image_name
        )

    def __create_image_filepath(self, image_number, file_extension):
        return os.path.join(
            self.__get_path_to_images_folder(),
            self.__format_image_name(image_number, file_extension)
        )

    def __create_thumbnail_filepath(self, image_number):
        return os.path.join(
            self.__get_path_to_thumbnails_folder(),
            self.__format_image_name(image_number, ".jpg")
        )

    def __get_sorted_list_of_image_names(self):
        return sorted(self.__get_all_image_names())

    def __get_sorted_list_of_thumbnail_names(self):
        return sorted(self.__get_all_thumbnail_names())

    def __create_relative_url_to_image_file(self, image_filename):
        return "{}/{}/images/{}".format(
            self.path_to_album_folders_name,
            self.album_name,
            image_filename
        )

    def __create_relative_url_to_thumbnail_file(self, thumbnail_filename):
        return "{}/{}/thumbnails/{}".format(
            self.path_to_album_folders_name,
            self.album_name,
            thumbnail_filename
        )

    def __create_thumbnail(self, input_path, output_path):
        image = Image.open(input_path)
        image = image.convert('RGB')
        image.thumbnail(MAX_THUMBNAIL_SIZE)
        image.save(output_path)

    def __get_thumbnail_path_from_image_name(self, image_name):
        image_number = self.__get_image_number_from_filename(image_name)
        return self.__create_thumbnail_filepath(image_number)

    def __create_thumbnail_for_image(self, image_name):
        image_path = self.__get_image_path_from_name(image_name)
        thumbnail_path = self.__get_thumbnail_path_from_image_name(image_name)
        self.__create_thumbnail(image_path, thumbnail_path)

    def __delete_all_thumbnails(self):
        shutil.rmtree(self.__get_path_to_thumbnails_folder())
        self.__create_thumbnails_folder_if_not_exists()

    def __get_all_image_names(self):
        images_folder = self.__get_path_to_images_folder()
        return os.listdir(images_folder)

    def __get_all_thumbnail_names(self):
        thumbnails_folder = self.__get_path_to_thumbnails_folder()
        return os.listdir(thumbnails_folder)

    def __count_images(self):
        return len(self.__get_all_image_names())

    def __count_thumbnails(self):
        return len(self.__get_all_thumbnail_names())
