class ImageNameFormatter():
    """A class for formatting image names"""

    def __init__(self, image_name_prefix):
        self.image_name_prefix = image_name_prefix

    def format_name(self, image_number, file_extension):
        return self.image_name_prefix + str(image_number).rjust(4, "0") + file_extension
