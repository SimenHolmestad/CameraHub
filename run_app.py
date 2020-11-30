import os
import socket
import subprocess
import platform
import argparse
import qrcode
import json
from app import create_app
from camera_modules.dummy_camera_module import DummyCameraModule
from camera_modules.rpicam_module import RPICameraModule

ALBUM_DIR_NAME = "albums"
CAMERA_MODULE_OPTIONS = {"dummy_module": DummyCameraModule,
                         "rpicam_module": RPICameraModule}


def find_ip_address_for_device():
    """Returns the IP address for this device"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def open_webpage_in_device_browser(url):
    """Open webpage in browser.

    If chromium is used, the chromium subprocess is returned so that
    it can be terminated later.

    """
    if(os.path.exists("/usr/bin/chromium-browser")):
        os.environ["DISPLAY"] = ":0"
        cmd = ["sleep", "2", "&&" "/usr/bin/chromium-browser", "--start-fullscreen", url]
        return subprocess.Popen(" ".join(cmd), shell=True)
    elif platform.system() == "Darwin":
        cmd = "open " + url
        subprocess.run(cmd, shell=True)

    return None


def generate_qr_code(file_path, content):
    """Generate a QR-code at <file_path> with the contents of
    <contents>.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    img.save(file_path)


def generate_and_fill_qr_code_album(album_dir_name, start_page_url):
    """Creates an album containing QR codes related to the application."""
    # Create qr-code album if it does not exist.
    QR_CODE_ALBUM_NAME = ".qr_codes"
    qr_code_folder_path = os.path.join(album_dir_name, QR_CODE_ALBUM_NAME)
    if not os.path.exists(qr_code_folder_path):
        os.makedirs(qr_code_folder_path)

    # Create QR code for start page
    start_page_qr_code_file_path = os.path.join(
        qr_code_folder_path,
        "start_page_qr_code.png"
    )
    generate_qr_code(start_page_qr_code_file_path, start_page_url)

    # Create QR code for joining wifi network if the file network_details.json exists
    if os.path.exists("network_details.json"):
        f = open("network_details.json", "r")
        content = json.loads(f.read())
        f.close()
        wifi_name = content["wifi_name"]
        wifi_protocol = content["wifi_protocol"]
        wifi_password = content["wifi_password"]

        wifi_qr_code_content = F"WIFI:S:{wifi_name};T:{wifi_protocol};P:{wifi_password};;"
        wifi_qr_code_file_path = os.path.join(
            qr_code_folder_path,
            "wifi_qr_code.png"
        )
        generate_qr_code(wifi_qr_code_file_path, wifi_qr_code_content)


if __name__ == '__main__':
    """Run the flask application."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Run in debug mode", action="store_true")
    parser.add_argument("-c", "--camera_module",
                        help="The camera module to use. Defaults to \"dummy module\"",
                        choices=CAMERA_MODULE_OPTIONS.keys(),
                        default="dummy_module")
    args = parser.parse_args()

    # Create album directory if it does not exist
    if not os.path.exists(ALBUM_DIR_NAME):
        os.makedirs(ALBUM_DIR_NAME)

    host_ip = find_ip_address_for_device()

    # Create QR codes
    start_page_url = "http://{}:5000/".format(host_ip)
    generate_and_fill_qr_code_album(ALBUM_DIR_NAME, start_page_url)

    # Print QR code URLs to console
    start_page_qr_code_url = "http://" + host_ip + ":5000/albums/.qr_codes/start_page_qr_code.png"
    print("Url for start page QR code:", start_page_qr_code_url)
    wifi_qr_code_url = "http://" + host_ip + ":5000/albums/.qr_codes/wifi_qr_code.png"
    print("Url for wifi QR code (if it exists):", wifi_qr_code_url)

    # NOTE: start_page_qr_code_url should be changed to an actual
    # webpage displaying both QR codes when a front-end is developed
    # in the future.

    # Open the start page QR code URL in browser if not in debug mode
    browser_process = None
    if not args.debug:
        browser_process = open_webpage_in_device_browser(start_page_qr_code_url)

    # Initialize camera module based on input args
    camera_module = CAMERA_MODULE_OPTIONS[args.camera_module](ALBUM_DIR_NAME)

    # Run app
    app = create_app(ALBUM_DIR_NAME, camera_module)
    app.run(debug=args.debug, host=host_ip)

    # Delete browser process if it was created
    if browser_process:
        browser_process.terminate()
