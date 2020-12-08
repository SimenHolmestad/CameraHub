from .base_dslr_module import BaseDSLRModule
import gphoto2 as gp


class DSLRRawTransferModule(BaseDSLRModule):
    """A dslr module where raw images are stored on the Raspberry PI"""

    def __init__(self, album_dir_name):
        super().__init__(album_dir_name)

        # To get both raw images and jpg images, the capture target
        # needs to be 1 so that both images are transferred to the
        # camera's SD card
        self.set_capture_target(1)

    def capture_dslr_image(self, camera, image_path):
        # camera.capture returns the file path of the raw image
        camera_file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

        # Save raw file to the raw_images folder in the album
        if "CR2" in camera_file_path.name:
            self.save_raw_file(image_path, camera, camera_file_path)

        # The jpg filename is the same as raw but with .JPG extension
        jpg_filename = camera_file_path.name.replace("CR2", "JPG")

        # Transfer the jpg file from the camera to image_path
        self.save_jpg_file(image_path, camera, camera_file_path.folder, jpg_filename)
