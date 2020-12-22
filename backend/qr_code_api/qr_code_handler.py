import os
import json
from backend.album_storage.folder import Folder
from .qr_code import QrCode


class QrCodeHandler:
    """A class for creating an keeping track of qr-codes and related
    information.
    """

    def __init__(self, static_dir_path, use_center_images=False):
        self.qr_code_folder = Folder(static_dir_path, "qr_codes")
        self.qr_codes = []
        self.logo_image_path = None
        self.wifi_image_path = None

        if use_center_images:
            self.logo_image_path = self.__get_path_to_icon_file("Camera-icon.png")
            self.wifi_image_path = self.__get_path_to_icon_file("Wifi-icon.png")

    def add_url_qr_code(self, name, url, information_text):
        """Add a qr_code containing and url to the qr code handler"""
        self.qr_codes.append(
            QrCode(
                self.qr_code_folder,
                name,
                url,
                information_text,
                self.logo_image_path
            )
        )

    def add_wifi_qr_code(self, name, wifi_name, wifi_protocol, wifi_password, information_text):
        """Add a qr_code containing and wifi information to the qr code handler"""
        wifi_qr_code_content = F"WIFI:S:{wifi_name};T:{wifi_protocol};P:{wifi_password};;"
        self.qr_codes.append(
            QrCode(
                self.qr_code_folder,
                name,
                wifi_qr_code_content,
                information_text,
                self.wifi_image_path
            )
        )

    def get_qr_codes(self):
        return self.qr_codes

    def get_qr_code_urls_as_strings(self, host_ip):
        return list(map(
            lambda qr_code:
            "For accessing "
            + qr_code.get_name()
            + " : "
            + self.__get_absolute_url_for_qr_code(qr_code, host_ip),
            self.get_qr_codes()
        ))

    def __get_absolute_url_for_qr_code(self, qr_code, host_ip):
        return "http://" + host_ip + ":5000/static/" + qr_code.get_relative_url()

    def create_qr_code_handler_with_qr_codes(static_folder_path, host_ip, use_center_images=False):
        qr_code_handler = QrCodeHandler(static_folder_path, use_center_images)

        start_page_url = "http://{}:3000/".format(host_ip)
        qr_code_handler.add_url_qr_code(
            "start_page_url",
            start_page_url,
            "Scan this qr code to go to CameraHub!"
        )

        qr_code_handler.__add_wifi_qr_code_if_network_details_file_exists()
        return qr_code_handler

    def __add_wifi_qr_code_if_network_details_file_exists(self):
        if os.path.exists("network_details.json"):
            f = open("network_details.json", "r")
            content = json.loads(f.read())
            f.close()
            self.add_wifi_qr_code(
                "wifi_qr_code",
                content["wifi_name"],
                content["wifi_protocol"],
                content["wifi_password"],
                content["description"]
            )

    def __get_path_to_icon_file(self, filename):
        return os.path.join(
            "image_resources",
            "icons",
            filename
        )
