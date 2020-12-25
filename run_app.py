import os
import shutil
import socket
import subprocess
import platform
import argparse
from backend.app import create_app
from backend.camera_module_options import get_camera_module_name_options, get_instance_of_camera_module_by_name
from backend.album_storage.folder_album_handler import FolderAlbumHandler
from backend.qr_code_api.qr_code_handler import QrCodeHandler

STATIC_FOLDER_NAME = "static"
STATIC_FOLDER_PATH = os.path.join("backend", STATIC_FOLDER_NAME)
DEBUG_PORT = 3000
PRODUCTION_PORT = 5000


def initialize_application():
    """Run the flask application."""
    args = parse_command_line_args()

    album_handler = FolderAlbumHandler(STATIC_FOLDER_PATH, "albums")
    camera_module = get_instance_of_camera_module_by_name(args.camera_module)

    if args.debug:
        run_backend_in_debug_mode(album_handler, camera_module)
    else:
        run_application(album_handler, camera_module)


def run_backend_in_debug_mode(album_handler, camera_module):
    """This should only need to be done when working on or testing the
    frontend.

    """
    qr_code_handler = create_qr_code_handler(DEBUG_PORT)
    print("Running the backend in debug mode. Start the frontend in a separate terminal window")
    qr_code_url = get_url_for_qr_codes(DEBUG_PORT)
    print("Url for qr codes (when frontend is running):", qr_code_url)

    app = create_app(album_handler, STATIC_FOLDER_NAME, camera_module, qr_code_handler)
    app.run(debug=True, host="localhost")


def run_application(album_handler, camera_module):
    build_frontend()

    qr_code_handler = create_qr_code_handler(PRODUCTION_PORT)
    qr_code_url = get_url_for_qr_codes(PRODUCTION_PORT)
    print("Url for qr codes:", qr_code_url)
    browser_process = open_webpage_in_device_browser(qr_code_url)

    app = create_app(album_handler, STATIC_FOLDER_NAME, camera_module, qr_code_handler)
    app.run(host=find_ip_address_for_device())

    # Delete browser process if it was created
    if browser_process:
        browser_process.terminate()


def build_frontend():
    os.chdir("frontend")
    run_npm_build_commands()
    move_frontend_folder_to_flask()
    os.chdir("./..")


def run_npm_build_commands():
    with open(os.devnull, 'w') as fp:
        print("Installing react dependencies...")
        subprocess.run("npm install", shell=True, stdout=fp)
        print("Building react application...")
        subprocess.run("npm run build", shell=True, stdout=fp)


def move_frontend_folder_to_flask():
    print("moving build folder to flask...")
    if os.path.exists("./../backend/static/react"):
        shutil.rmtree("./../backend/static/react")
    shutil.move("./build", "./../backend/static/react")


def open_webpage_in_device_browser(url):
    """If chromium is used, the chromium subprocess is returned so that
    it can be terminated later.

    """
    if(os.path.exists("/usr/bin/chromium-browser")):
        os.environ["DISPLAY"] = ":0"
        cmd = ["sleep", "2", "&&" "/usr/bin/chromium-browser", "--start-fullscreen", url]

        # Return a chromium subprocessed with suppressed output
        with open(os.devnull, 'w') as fp:
            return subprocess.Popen(" ".join(cmd), shell=True, stdout=fp, stderr=fp)
    elif platform.system() == "Darwin":
        cmd = "open " + url
        subprocess.run(cmd, shell=True)

    return None


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Run in debug mode", action="store_true")
    camera_module_name_options = get_camera_module_name_options()
    parser.add_argument("-c", "--camera_module",
                        help="The name of the camera module to use. Defaults to \"dummy\"",
                        choices=camera_module_name_options,
                        default=camera_module_name_options[0])
    return parser.parse_args()


def find_ip_address_for_device():
    """Returns the IP address for this device"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def get_url_for_qr_codes(port):
    return "http://" + find_ip_address_for_device() + ":" + str(port) + "/qr"


def create_qr_code_handler(port):
    return QrCodeHandler.create_qr_code_handler_with_qr_codes(
        STATIC_FOLDER_PATH,
        find_ip_address_for_device(),
        port,
        use_center_images=True
    )


if __name__ == '__main__':
    initialize_application()
