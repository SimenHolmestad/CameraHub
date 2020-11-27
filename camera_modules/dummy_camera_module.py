from base_camera_module import BaseCameraModule
import os
import matplotlib.pyplot as plt
import numpy as np
from random import randint


class DummyCameraModule(BaseCameraModule):
    """Dummy camera module for creating somewhat random images without a
    camera"""

    def __init__(self,
                 album_dir_name,
                 file_extension=".png",
                 width=1200,
                 height=800,
                 number_of_circles=80,
                 min_circle_radius=30,
                 max_circle_radius=80):
        super().__init__(album_dir_name)
        self.file_extension = file_extension
        self.width = width
        self.height = height
        self.number_of_circles = number_of_circles
        self.min_circle_radius = min_circle_radius
        self.max_circle_radius = max_circle_radius

    def add_random_circle_to_image(self, image):
        """Add a random circle to the image based on the input parameters of
        the class. The function returns the input image with the added
        circle."""
        x_center = randint(0, self.width - 1)
        y_center = randint(0, self.height - 1)
        radius = randint(self.min_circle_radius, self.max_circle_radius)
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)

        # Create start and endpoints as iterating through the whole
        # image is not necessary
        x_start = max(0, x_center - radius - 1)
        x_end = min(self.width, x_center + radius + 1)
        y_start = max(0, y_center - radius - 1)
        y_end = min(self.height, y_center + radius + 1)

        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if (x - x_center)**2 + (y - y_center)**2 < radius**2:
                    image[y, x, 0] = r
                    image[y, x, 1] = g
                    image[y, x, 2] = b
        return image

    def capture_image(self, image_path_without_extension):
        """Creates an image and saves it in "image_path_without_extension"."""
        # Create white image
        image = np.full((self.height, self.width, 3), 255, dtype=np.uint8)

        # Add circles to image
        for x in range(self.number_of_circles):
            image = self.add_random_circle_to_image(image)

        # Save image
        plt.imsave(image_path_without_extension + self.file_extension, image)


if __name__ == '__main__':
    ALBUM_DIR_NAME = "test_albums"
    ALBUM_NAME = "dummy_module_images"
    if not os.path.exists(ALBUM_DIR_NAME):
        os.makedirs(ALBUM_DIR_NAME)

    path_to_album = os.path.join(ALBUM_DIR_NAME, ALBUM_NAME)

    if not os.path.exists(path_to_album):
        os.makedirs(path_to_album)
        os.makedirs(os.path.join(path_to_album, "images"))

    camera_module = DummyCameraModule(ALBUM_DIR_NAME)
    camera_module.try_capture_image(ALBUM_NAME)
