from backend.album_storage.folder import Folder
from .qr_code import QrCode


class QrCodeHandler:
    """A class for creating an keeping track of qr-codes and related
    information.
    """

    def __init__(self, static_dir_path):
        self.qr_code_folder = Folder(static_dir_path, "qr_codes")
        self.qr_codes = []

    def add_url_qr_code(self, name, url, information_text):
        self.qr_codes.append(
            QrCode(
                self.qr_code_folder,
                name,
                url,
                information_text
            )
        )

    def add_wifi_qr_code(self, name, wifi_name, wifi_protocol, wifi_password, information_text):
        wifi_qr_code_content = F"WIFI:S:{wifi_name};T:{wifi_protocol};P:{wifi_password};;"
        self.qr_codes.append(
            QrCode(
                self.qr_code_folder,
                name,
                wifi_qr_code_content,
                information_text
            )
        )

    def get_qr_codes(self):
        return self.qr_codes
