import unittest
import tempfile
from backend.app import create_app
from backend.album_storage.folder_album_handler import FolderAlbumHandler
from backend.qr_code_api.qr_code_handler import QrCodeHandler
from .camera_modules_for_testing import create_fast_dummy_module


class QrCodeApiTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary static dir which is deleted after every test
        self.static_dir = tempfile.TemporaryDirectory(dir=".")
        self.static_dir_name = self.static_dir.name.split("./")[1]
        camera_module = create_fast_dummy_module()
        album_handler = FolderAlbumHandler(self.static_dir_name, "albums")

        self.qr_code_handler = QrCodeHandler(self.static_dir_name)
        app = create_app(album_handler, self.static_dir_name, camera_module, self.qr_code_handler)
        self.test_client = app.test_client()

    def tearDown(self):
        self.static_dir.cleanup()

    def test_response_when_no_qr_codes_added(self):
        response = self.test_client.get('/qr_codes/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'qr_codes': []})

    def test_response_after_adding_url_qr_code(self):
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        json_response = self.test_client.get('/qr_codes/', content_type='application/json').json
        self.assertEqual(json_response, {
            'qr_codes': [
                {
                    'name': 'test_url_qr_code',
                    'information': 'Scan this qr code to go to www.test.com!',
                    'url': '/{}/qr_codes/test_url_qr_code.png'.format(self.static_dir_name)
                }
            ]
        })

    def test_response_after_adding_url_and_wifi_qr_code(self):
        self.qr_code_handler.add_url_qr_code(
            "test_url_qr_code",
            "www.test.com",
            "Scan this qr code to go to www.test.com!"
        )
        self.qr_code_handler.add_wifi_qr_code(
            "wifi_qr_code",
            "my_netwok_ssid",
            "WPA/WPA2",
            "my_super_secret_password",
            "Scan this qr code to connect to the wifi!"
        )
        json_response = self.test_client.get('/qr_codes/', content_type='application/json').json
        self.assertEqual(json_response, {
            'qr_codes': [
                {
                    'information': 'Scan this qr code to go to www.test.com!',
                    'name': 'test_url_qr_code',
                    'url': '/{}/qr_codes/test_url_qr_code.png'.format(self.static_dir_name)
                }, {
                    'information': 'Scan this qr code to connect to the wifi!',
                    'name': 'wifi_qr_code',
                    'url': '/{}/qr_codes/wifi_qr_code.png'.format(self.static_dir_name)
                }
            ]
        })
