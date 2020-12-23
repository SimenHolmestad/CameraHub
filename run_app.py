import os
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


def initialize_application():
    """Run the flask application."""
    args = parse_command_line_args()

    camera_module = get_instance_of_camera_module_by_name(args.camera_module)
    album_handler = FolderAlbumHandler(STATIC_FOLDER_PATH, "albums")
    qr_code_handler = QrCodeHandler.create_qr_code_handler_with_qr_codes(
        STATIC_FOLDER_PATH,
        find_ip_address_for_device(),
        use_center_images=True
    )

    if args.debug:
        run_backend_in_debug_mode(album_handler, camera_module, qr_code_handler)
    else:
        run_application(album_handler, camera_module, qr_code_handler)


def run_backend_in_debug_mode(album_handler, camera_module, qr_code_handler):
    """Runs the backend in debug mode.

    This should only need to be done when working on or testing the
    frontend.
    """
    print("Running the backend in debug mode. Start the frontend in a separate terminal window")
    change_frontend_proxy_config("localhost")
    print("Url for qr codes:", get_url_for_qr_codes("localhost"))

    # run app
    app = create_app(album_handler, STATIC_FOLDER_NAME, camera_module, qr_code_handler)
    app.run(debug=True, host="localhost")


def run_application(album_handler, camera_module, qr_code_handler):
    host_ip = find_ip_address_for_device()
    npm_process = run_frontend(host_ip)
    qr_code_url = get_url_for_qr_codes(host_ip)
    print("Url for qr codes:", qr_code_url)

    # Open qr code page in browser
    browser_process = open_webpage_in_device_browser(qr_code_url)

    # Run app
    app = create_app(album_handler, STATIC_FOLDER_NAME, camera_module, qr_code_handler)
    app.run(host=host_ip)

    # Delete browser process if it was created
    if browser_process:
        browser_process.terminate()

    npm_process.terminate()


def run_frontend(host_ip):
    """Runs the frontend and returns the npm process so that it can be
    terminated later.

    In the future, the frontend should be built and served by flask
    instead of doing this.
    """
    change_frontend_proxy_config(host_ip)
    os.chdir("frontend")
    if not os.path.exists("node_modules"):
        print("Installing react dependencies")
        subprocess.run("npm install", shell=True)

    npm_process = subprocess.Popen("BROWSER=none npm start", shell=True)
    os.chdir("./..")
    return npm_process


def change_frontend_proxy_config(host_ip):
    """Change the proxy-value of the package.json file so that it has the right ip.

    This is probably not a good idea, but I guess it might work for now.
    """
    f = open("frontend/package.json", "r")
    lines = f.readlines()
    f.close()

    for i in range(len(lines)):
        if lines[i].startswith("  \"proxy\": "):
            lines[i] = "  \"proxy\": \"http://{}:5000/\"\n".format(host_ip)

    f = open("frontend/package.json", "w")
    lines = f.writelines(lines)
    f.close()


def open_webpage_in_device_browser(url):
    """Open webpage in browser.

    If chromium is used, the chromium subprocess is returned so that
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


def get_url_for_qr_codes(host_ip):
    return "http://" + host_ip + ":3000/qr_codes"


if __name__ == '__main__':
    initialize_application()
