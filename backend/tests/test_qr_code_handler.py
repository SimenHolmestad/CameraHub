import os
import unittest
import tempfile
from pyzbar.pyzbar import decode
from PIL import Image
from backend.qr_code_api.qr_code_handler import QrCodeHandler


class QrCodeHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.static_test_dir = tempfile.TemporaryDirectory(dir=".")
        self.static_test_dir_name = self.static_test_dir.name.split("./")[1]
        self.qr_code_handler = QrCodeHandler(self.static_test_dir_name)

    def tearDown(self):
        self.static_test_dir.cleanup()  # Remove directory from file system

    def print_zbar_error_message(self):
        print("-----------------------------")
        print("Could not decode qr code using zbar.")
        print("To install zbar correctly, go to https://pypi.org/project/pyzbar/")
        print("-----------------------------")

    def test_empty_list_is_returned_when_no_qr_codes(self):
        qr_codes = self.qr_code_handler.get_qr_codes()
        self.assertEqual(qr_codes, [])

    def test_qr_code_is_returned_after_code_is_created(self):
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        qr_codes = self.qr_code_handler.get_qr_codes()
        self.assertEqual(len(qr_codes), 1)
        self.assertEqual(qr_codes[0].get_name(), "test_url_qr_code")

    def test_create_two_qr_codes(self):
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code2",
            "www.test2.com",
            "Scan this qr code to go to www.test.com!"
        )
        qr_codes = self.qr_code_handler.get_qr_codes()

        self.assertEqual(len(qr_codes), 2)
        self.assertEqual(qr_codes[0].get_name(), "test_url_qr_code")
        self.assertEqual(qr_codes[1].get_name(), "test_url_qr_code2")

    def test_qr_code_file_is_created(self):
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        expected_qr_code_path = os.path.join(
            self.static_test_dir_name,
            "qr_codes",
            "test_url_qr_code.png"
        )
        self.assertTrue(os.path.exists(expected_qr_code_path))

    def test_get_relative_url_of_qr_code(self):
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        self.assertEqual(
            self.qr_code_handler.get_qr_codes()[0].get_relative_url(),
            "qr_codes/test_url_qr_code.png"
        )

    def test_generated_url_qr_code_is_correct(self):
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        qr_code_filepath = os.path.join(
            self.static_test_dir_name,
            "qr_codes",
            "test_url_qr_code.png"
        )
        try:
            decoded_qr_code = decode(Image.open(qr_code_filepath))
        except ImportError:
            self.print_zbar_error_message()
            return

        qr_code_text = decoded_qr_code[0].data.decode("utf-8")
        self.assertEqual(qr_code_text, "www.test.com")

    def test_generated_wifi_qr_code_is_correct(self):
        self.qr_code_handler.add_wifi_qr_code(
            "wifi_qr_code",
            "my_netwok_ssid",
            "WPA/WPA2",
            "my_super_secret_password",
            "Scan this qr code to connect to the wifi!"
        )
        qr_code_filepath = os.path.join(
            self.static_test_dir_name,
            "qr_codes",
            "wifi_qr_code.png"
        )
        try:
            decoded_qr_code = decode(Image.open(qr_code_filepath))
        except ImportError:
            self.print_zbar_error_message()
            return

        qr_code_text = decoded_qr_code[0].data.decode("utf-8")
        self.assertEqual(
            qr_code_text,
            "WIFI:S:my_netwok_ssid;T:WPA/WPA2;P:my_super_secret_password;;"
        )


if __name__ == '__main__':
    unittest.main()
