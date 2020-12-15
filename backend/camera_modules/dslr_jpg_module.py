from .base_dslr_module import BaseDSLRModule
import gphoto2 as gp
import time


class DSLRJpgModule(BaseDSLRModule):
    """A dslr module where no raw images are stored"""

    def __init__(self, album_dir_name):
        super().__init__(album_dir_name)

        # For maximum speed, we set capture target to 0, so that the
        # jpg image is not written to the SD card before being written
        # to the Raspberry PI.
        self.set_capture_target(0)

        print("---------------------------------------------------")
        print()
        print("IMPORTANT!")
        print("Make sure your camera is set to only capture .jpg")
        print("images and not raw images.")
        print()
        print("---------------------------------------------------")
        time.sleep(2)

    def capture_dslr_image(self, camera, image_path):
        # camera.capture should return the file path of the jpg image
        camera_file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

        if "CR2" in camera_file_path.name:
            print("Raw image captured when using JPG module!")
            print("Set camera to only capture jpg files and restart server.")

        # Transfer the jpg file from the camera to image_path
        self.save_jpg_file(image_path, camera, camera_file_path.folder, camera_file_path.name)