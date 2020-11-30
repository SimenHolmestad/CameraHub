import os
import sys
import socket
import subprocess
import platform
from app import create_app
from camera_modules.dummy_camera_module import DummyCameraModule


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
    use_debug = False
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        use_debug = True

    ALBUM_DIR_NAME = "albums"

    # Create album directory if it does not exist
    if not os.path.exists(ALBUM_DIR_NAME):
        os.makedirs(ALBUM_DIR_NAME)

    # Initialize camera module
    camera_module = DummyCameraModule(ALBUM_DIR_NAME)

    host_ip = find_ip_address_for_device()

    browser_process = None
    if not use_debug:
        browser_process = open_start_page_in_browser(host_ip)

    app = create_app(ALBUM_DIR_NAME, camera_module)
    app.run(debug=use_debug, host=host_ip)

    # Delete browser process if it was created
    if browser_process:
        browser_process.terminate()
