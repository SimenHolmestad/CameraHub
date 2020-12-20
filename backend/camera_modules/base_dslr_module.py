from abc import ABC, abstractmethod
from .base_camera_module import BaseCameraModule
import subprocess
import gphoto2 as gp
import signal
import time
import os


class BaseDSLRModule(BaseCameraModule, ABC):
    """Camera module provinging basic DSLR functionality using GPhoto2"""

    def __init__(self):
        super().__init__(".jpg")
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

    @abstractmethod
    def capture_dslr_image(self, camera, image_path, raw_image_path=None):
        """Method for capturing dlsr image and storing it in image_path.
        Should raise IOError if something goes wrong with capture.

        It should not be necessary to use this function directly. Use
        the try_capture_image instead
        """
        pass

    def try_capture_image(self, image_path, raw_image_path=None):
        """Captures an image and saves it in "image_path"."""
        start_time = time.time()
        camera = gp.Camera()
        camera.init()
        print("Capturing image...")

        # The image capturing process different for each dslr module
        self.capture_dslr_image(camera, image_path, raw_image_path)

        camera.exit()
        print("Image capture took", round(time.time() - start_time, 2), "seconds")

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

    def save_jpg_file(self, image_path, camera, camera_image_folder, camera_image_filename):
        camera_file = camera.file_get(
            camera_image_folder, camera_image_filename, gp.GP_FILE_TYPE_NORMAL)

        print("Saving jpg image to", image_path)
        camera_file.save(image_path)

    def save_raw_image(self, raw_image_path, camera, camera_file_path):
        print("Saving raw image to", raw_image_path)
        camera_file = camera.file_get(
            camera_file_path.folder,
            camera_file_path.name,
            gp.GP_FILE_TYPE_NORMAL
        )
        camera_file.save(raw_image_path)
