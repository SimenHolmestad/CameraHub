from abc import ABC, abstractmethod
import os
import re


class BaseCameraModule(ABC):
    """Abstract class containing common image capture related code"""

    def __init__(self,
                 album_dir_name,
                 file_extension,
                 image_name_prefix="image"):
        assert os.path.exists(album_dir_name)
        self.album_dir_name = album_dir_name
        self.file_extension = file_extension
        self.image_name_prefix = image_name_prefix

    @abstractmethod
    def capture_image(self, image_path):
        """Method for capturing image and storing it in image_path. Should
        raise IOError if something goes wrong with capture.

        It should not be necessary to use this function directly. Use
        try_capture_image instead.

        """
        pass

    def try_capture_image(self, album_name):
        """Try to capture an image using the capture_image method.

        On success: Returns a dictionary containing the file path of
        the created image.

        On fail: Returns a dictionary containing a message of what
        went wrong.
        """
        assert os.path.exists(os.path.join(
            self.album_dir_name,
            album_name,
            "images"
        ))

        next_image_number = self.find_current_image_number(album_name) + 1
        next_image_name = self.image_name_prefix + str(next_image_number).rjust(4, "0") + self.file_extension
        next_image_path = os.path.join(
            self.album_dir_name,
            album_name,
            "images",
            next_image_name
        )

        self.capture_image(next_image_path)
        self.write_current_image_number_file(album_name, next_image_number)

        return "albums/{}/images/{}".format(album_name, next_image_name)

    def find_current_image_number(self, album_name):
        """Find the image number of the current image.

        The function tries to read the content of the file
        ".current_image_number.txt" and creates it if it does not
        exist.

        It also makes some checks to the file and reacreates it if one
        of the following conditions occur:
        - The current image file does not exist
        - The next image file does exist (and is about to get overwritten)

        """
        path_to_album = os.path.join(self.album_dir_name, album_name)
        path_to_album_images = os.path.join(path_to_album, "images")
        current_image_number_file_path = os.path.join(
            path_to_album,
            ".current_image_number.txt"
        )

        # Check if file does not exist
        if not os.path.exists(current_image_number_file_path):
            return self.recreate_image_number_file(album_name)

        f = open(current_image_number_file_path)
        current_image_number = int(f.read())
        f.close()

        # Check if the current image file exist
        current_image_filepath = os.path.join(
            path_to_album_images,
            self.image_name_prefix + str(current_image_number).rjust(4, "0"),
            self.file_extension
        )
        if not os.path.exists(current_image_filepath):
            return self.recreate_image_number_file(album_name)

        # Check if the next image file exist
        possible_next_image_filepath = os.path.join(
            path_to_album_images,
            self.image_name_prefix + str(current_image_number + 1).rjust(4, "0")
        )
        next_file_exists = (os.path.exists(possible_next_image_filepath + ".png")
                            or os.path.exists(possible_next_image_filepath + ".jpg"))
        if next_file_exists:
            return self.recreate_image_number_file(album_name)

        return current_image_number

    def recreate_image_number_file(self, album_name):
        """Goes through all files in the images folder of the album and use
        this information to write the current_image_number file. The next
        image number is returned from the function.

        This function is handy if the next_image_number file is wrong.

        """
        path_to_album_images = os.path.join(
            self.album_dir_name,
            album_name,
            "images")
        # Get all images in album on the right format
        p = re.compile("^" + self.image_name_prefix + "\\d\\d\\d\\d$")
        images_in_folder = os.listdir(path_to_album_images)
        image_names = list(map(lambda x: x.split(".")[0], images_in_folder))
        correctly_formatted_images = [s for s in image_names if p.match(s)]

        if not correctly_formatted_images:
            current_image_number = 0
        else:
            # Set current_image_number to the image number of the last element in the list
            correctly_formatted_images.sort()
            current_image_number = int(correctly_formatted_images[-1][-4:])

        self.write_current_image_number_file(album_name, current_image_number)
        return current_image_number

    def get_current_image_name(self, album_name):
        """Returns the name of the last image added to the album."""
        current_image_number = self.find_current_image_number(album_name)
        return self.image_name_prefix + str(current_image_number).rjust(4, "0") + self.file_extension

    def write_current_image_number_file(self, album_name, current_image_number):
        """Write the parameter "current_image_number" to the file
        ".current_image_number.txt" in the corresponding album.

        """
        current_image_number_file_path = os.path.join(
            self.album_dir_name,
            album_name,
            ".current_image_number.txt"
        )
        f = open(current_image_number_file_path, "w")
        f.write(str(current_image_number))
        f.close()
