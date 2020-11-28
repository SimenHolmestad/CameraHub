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

        next_image_number = self.find_next_image_number(album_name)
        next_image_name = self.image_name_prefix + str(next_image_number).rjust(4, "0")
        next_image_path = os.path.join(
            self.album_dir_name,
            album_name,
            "images",
            next_image_name + self.file_extension
        )
        try:
            self.capture_image(next_image_path)
            self.write_next_image_number_file(album_name, next_image_number + 1)
        except IOError as error:
            return {"error": str(error)}

        return {
            "success": "Image successfully captured",
            "image_file_path": next_image_path
        }

    def find_next_image_number(self, album_name):
        """Find the image number of the next image.

        The function reads the content of the file
        ".next_image_number.txt". If this file does not exist (or the
        an image file is in risk of getting overwritten), it tries to
        figure out next image number by reading the file names of the
        images present in the images folder of the specified album.

        """
        path_to_album = os.path.join(self.album_dir_name, album_name)
        path_to_album_images = os.path.join(path_to_album, "images")
        next_image_number_file_path = os.path.join(
            path_to_album,
            ".next_image_number.txt"
        )

        if os.path.exists(next_image_number_file_path):
            f = open(next_image_number_file_path)
            next_image_number = int(f.read())
            f.close()

            # Make sure to not overwrite an image if .next_image_number.txt is wrong
            possible_next_image_filepath = os.path.join(
                path_to_album_images,
                self.image_name_prefix + str(next_image_number).rjust(4, "0")
            )
            if not (os.path.exists(possible_next_image_filepath + ".png")
                    or os.path.exists(possible_next_image_filepath + ".jpg")):
                return next_image_number

        # Get all images in album on the right format
        p = re.compile("^" + self.image_name_prefix + "\\d\\d\\d\\d$")
        images_in_folder = os.listdir(path_to_album_images)
        image_names = list(map(lambda x: x.split(".")[0], images_in_folder))
        correctly_formatted_images = [s for s in image_names if p.match(s)]

        if not correctly_formatted_images:
            next_image_number = 1
        else:
            # Set next_image_number to the image number of the last element in the list + 1
            correctly_formatted_images.sort()
            next_image_number = int(correctly_formatted_images[-1][-4:]) + 1

        self.write_next_image_number_file(album_name, next_image_number)
        return next_image_number

    def write_next_image_number_file(self, album_name, next_image_number):
        """Write the parameter "next_image_number" to the file
        ".next_image_number.txt" in the corresponding album.

        """
        next_image_number_file_path = os.path.join(
            self.album_dir_name,
            album_name,
            ".next_image_number.txt"
        )
        f = open(next_image_number_file_path, "w")
        f.write(str(next_image_number))
        f.close()
