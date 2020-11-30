import os
import socket
import subprocess
import platform
import argparse
from app import create_app
from camera_modules.dummy_camera_module import DummyCameraModule
from camera_modules.rpicam_module import RPICameraModule

CAMERA_MODULE_OPTIONS = {"dummy_module": DummyCameraModule,
                         "rpicam_module": RPICameraModule}


def find_ip_address_for_device():
    # Find IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def open_start_page_in_browser(host_ip):
    """Open start page in browser."""
    start_url = "http://" + host_ip + ":5000/"

    if(os.path.exists("/usr/bin/chromium-browser")):
        os.environ["DISPLAY"] = ":0"
        cmd = ["sleep", "2", "&&" "/usr/bin/chromium-browser", "--start-fullscreen", start_url]
        return subprocess.Popen(" ".join(cmd), shell=True)
    elif platform.system() == "Darwin":
        cmd = "open " + start_url
        subprocess.run(cmd, shell=True)

    return None


if __name__ == '__main__':
    """Run the flask application."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Run in debug mode", action="store_true")
    parser.add_argument("-c", "--camera_module",
                        help="The camera module to use. Defaults to \"dummy module\"",
                        choices=CAMERA_MODULE_OPTIONS.keys(),
                        default="dummy_module")

    args = parser.parse_args()

    ALBUM_DIR_NAME = "albums"

    # Create album directory if it does not exist
    if not os.path.exists(ALBUM_DIR_NAME):
        os.makedirs(ALBUM_DIR_NAME)

    # Initialize camera module based on input args
    camera_module = CAMERA_MODULE_OPTIONS[args.camera_module](ALBUM_DIR_NAME)

    host_ip = find_ip_address_for_device()

    browser_process = None
    if not args.debug:
        browser_process = open_start_page_in_browser(host_ip)

    app = create_app(ALBUM_DIR_NAME, camera_module)
    app.run(debug=args.debug, host=host_ip)

    # Delete browser process if it was created
    if browser_process:
        browser_process.terminate()
