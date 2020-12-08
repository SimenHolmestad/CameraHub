from abc import ABC, abstractmethod
from .base_camera_module import BaseCameraModule
import subprocess
import gphoto2 as gp
import signal
import time
import os


class BaseDSLRModule(BaseCameraModule, ABC):
    """Camera module provinging basic DSLR functionality using GPhoto2"""

    def kill_gphoto2_process(self):
        """Kill the gphoto-process that starts when the camera is first
        connected. A window opens when the camera is connected and we
        have to kill the process related to that window.
        """
        p = subprocess.Popen(["ps", "-A"], stdout=subprocess.PIPE)
        out, err = p.communicate()

        # Find the line with the gphoto-process and kill it.
        for line in out.splitlines():
            if b"gvfsd-gphoto2" in line:
                # Kill the process (must be done with the process id)
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    def set_capture_target(self, target_number):
        """Sets the capture target of the camera.

        The parameter target_number should be either 0 or 1, which
        means:

        - 1: Tranfer the image(s) to the cameras SD-card
        - 0: Do not Transfer the image(s) to the cameras SD-card and
          just keep it/them in flash memory.

        """
        subprocess.run("gphoto2 --set-config capturetarget=" + str(target_number), shell=True)

    def __init__(self, album_dir_name):
        super().__init__(album_dir_name, ".jpg")
        camera = gp.Camera()
        print("Please connect and switch on your DSLR Camera")
        while True:
            try:
                self.kill_gphoto2_process()
                camera.init()
            except gp.GPhoto2Error as ex:
                if ex.code == gp.GP_ERROR_MODEL_NOT_FOUND:
                    # no camera, try again in 3 seconds
                    time.sleep(3)
                    continue
                # some other error we can"t handle here
                raise
            # operation completed successfully so exit loop
            break
        print("DSLR Camera connected.")
        camera.exit()

    def save_jpg_file(self, image_path, camera, camera_image_folder, camera_image_filename):
        camera_file = camera.file_get(
            camera_image_folder, camera_image_filename, gp.GP_FILE_TYPE_NORMAL)

        print("Saving jpg image to", image_path)
        camera_file.save(image_path)

    def save_raw_file(self, image_path, camera, camera_image_file_path):
        """Saves a raw image to the album based on image_path.

        The image is saved in ./../raw_images/image_name.CR2 relative
        to the image in <image_path>.

        """
        image_folder, image_name = os.path.split(image_path)
        raw_image_folder = os.path.join(
            os.path.dirname(image_folder),
            "raw_images"
        )
        if not os.path.exists(raw_image_folder):
            os.makedirs(raw_image_folder)

        raw_image_path = os.path.join(
            raw_image_folder,
            image_name.replace("jpg", "CR2")
        )
        print("Saving raw image to", raw_image_path)
        camera_file = camera.file_get(
            camera_image_file_path.folder,
            camera_image_file_path.name,
            gp.GP_FILE_TYPE_NORMAL)
        camera_file.save(raw_image_path)

    @abstractmethod
    def capture_dslr_image(self, camera, image_path):
        """Method for capturing dlsr image and storing it in image_path.
        Should raise IOError if something goes wrong with capture.

        It should not be necessary to use this function directly. Use
        the try_capture_image function of BaseCameraModule instead.
        """
        pass

    def capture_image(self, image_path):
        """Captures an image and saves it in "image_path"."""
        start_time = time.time()
        camera = gp.Camera()
        camera.init()
        print("Capturing image...")

        # The image capturing process different for each dslr module
        self.capture_dslr_image(camera, image_path)

        camera.exit()
        print("Image capturing took", round(time.time() - start_time, 2), "seconds")
