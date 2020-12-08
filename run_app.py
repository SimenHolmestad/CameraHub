import os
import socket
import subprocess
import platform
import argparse
import qrcode
import json
from backend.app import create_app
from backend.camera_modules.dummy_camera_module import DummyCameraModule
from backend.camera_modules.rpicam_module import RPICameraModule
from backend.camera_modules.dslr_jpg_module import DSLRJpgModule
from backend.camera_modules.dslr_raw_module import DSLRRawModule
from backend.camera_modules.dslr_raw_transfer_module import DSLRRawTransferModule
from backend.utils.thumbnail_utils import create_thumbnails_for_all_albums

STATIC_FOLDER_NAME = "static"
STATIC_FOLDER_PATH = os.path.join("backend", STATIC_FOLDER_NAME)
ALBUM_DIR_PATH = os.path.join(STATIC_FOLDER_PATH, "albums")

CAMERA_MODULE_OPTIONS = {"dummy": DummyCameraModule,
                         "rpicam": RPICameraModule,
                         "dslr_jpg": DSLRJpgModule,
                         "dslr_raw": DSLRRawModule,
                         "dslr_raw_transfer": DSLRRawTransferModule}


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

        # Return a chromium subprocessed with suppressed output
        with open(os.devnull, 'w') as fp:
            return subprocess.Popen(" ".join(cmd), shell=True, stdout=fp, stderr=fp)
    elif platform.system() == "Darwin":
        cmd = "open " + url
        subprocess.run(cmd, shell=True)

    return None


def generate_qr_code(file_path, content):
    """Generate a QR-code at <file_path> with the contents of
    <content>.
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


def generate_and_save_qr_codes(static_folder_name, start_page_url):
    """Creates an album containing QR codes related to the application."""
    # Create qr-code album if it does not exist.
    QR_CODE_FOLDER_NAME = "qr_codes"
    qr_code_folder_path = os.path.join(static_folder_name, QR_CODE_FOLDER_NAME)
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


def run_frontend(host_ip):
    """Runs the frontend and returns the npm process so that it can be terminated later"""
    change_frontend_proxy_config(host_ip)
    os.chdir("frontend")
    if not os.path.exists("node_modules"):
        print("Installing react dependencies")
        subprocess.run("npm install", shell=True)

    npm_process = subprocess.Popen("BROWSER=none npm start", shell=True)
    os.chdir("./..")
    return npm_process


def run_application(camera_module):
    host_ip = find_ip_address_for_device()

    npm_process = run_frontend(host_ip)

    # Print QR code URLs to console
    start_page_qr_code_url = "http://" + host_ip + ":5000/static/qr_codes/start_page_qr_code.png"
    print("Url for start page QR code:", start_page_qr_code_url)
    wifi_qr_code_url = "http://" + host_ip + ":5000/static/qr_codes/wifi_qr_code.png"
    print("Url for wifi QR code (if it exists):", wifi_qr_code_url)

    # NOTE: start_page_qr_code_url should be changed to an actual
    # webpage displaying both QR codes when a front-end is developed
    # in the future.

    # Create QR codes
    start_page_url = "http://{}:3000/".format(host_ip)
    generate_and_save_qr_codes(STATIC_FOLDER_PATH, start_page_url)

    # Open qr-code page in browser
    browser_process = open_webpage_in_device_browser(start_page_qr_code_url)

    # Run app
    app = create_app(STATIC_FOLDER_NAME, STATIC_FOLDER_PATH, camera_module)
    app.run(debug=args.debug, host=host_ip)

    # Delete browser process if it was created
    if browser_process:
        browser_process.terminate()

    npm_process.terminate()


def run_backend_in_debug_mode(camera_module):
    print("Running the backend in debug mode. Start the frontend in a separate terminal window")

    change_frontend_proxy_config("localhost")

    # Create QR codes
    start_page_url = "http://{}:3000/".format(find_ip_address_for_device())
    generate_and_save_qr_codes(STATIC_FOLDER_PATH, start_page_url)

    # Run app
    app = create_app(STATIC_FOLDER_NAME, STATIC_FOLDER_PATH, camera_module)
    app.run(debug=True, host="localhost")


if __name__ == '__main__':
    """Run the flask application."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Run in debug mode", action="store_true")
    parser.add_argument("-c", "--camera_module",
                        help="The camera module to use. Defaults to \"dummy\"",
                        choices=CAMERA_MODULE_OPTIONS.keys(),
                        default="dummy")
    args = parser.parse_args()

    # Create album directory if it does not exist
    if not os.path.exists(ALBUM_DIR_PATH):
        os.makedirs(ALBUM_DIR_PATH)

    print("Creating thumbnails for albums")
    create_thumbnails_for_all_albums(ALBUM_DIR_PATH)

    # Initialize camera module based on input args
    camera_module = CAMERA_MODULE_OPTIONS[args.camera_module](ALBUM_DIR_PATH)

    if args.debug:
        run_backend_in_debug_mode(camera_module)
    else:
        run_application(camera_module)
