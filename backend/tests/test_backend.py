import unittest
import tempfile
import os
import json
from backend.album_storage.folder_album_handler import FolderAlbumHandler
from backend.app import create_app
from .test_utils import create_fast_dummy_module


class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Create a new album directory so that the "albums" directory
        # is left untouched while testing.
        self.static_dir = tempfile.TemporaryDirectory(dir=".")
        self.static_dir_name = self.static_dir.name.split("./")[1]
        self.album_dir_path = os.path.join(self.static_dir_name, "albums")
        os.makedirs(self.album_dir_path)

        self.camera_module = create_fast_dummy_module()

        self.album_handler = FolderAlbumHandler(self.static_dir_name, "albums")
        self.app = create_app(self.album_handler, self.static_dir_name, self.camera_module)

    def tearDown(self):
        self.static_dir.cleanup()

    def create_temp_album(self, album_name, description=""):
        """Create an album with the specified name and description."""
        album_directory_path = os.path.join(
            self.album_dir_path,
            album_name)

        os.makedirs(os.path.join(
            album_directory_path,
            "images"
        ))

        os.makedirs(os.path.join(
            album_directory_path,
            "thumbnails"
        ))

        if description != "":
            description_file_path = os.path.join(album_directory_path, "description.txt")
            f = open(description_file_path, "w")
            f.write(description)
            f.close()

    def add_dummy_image_file_to_album(self, album_name):
        """Create a dummy image file with the specified name to the specified album. """
        album = self.album_handler.get_album(album_name)
        album.try_capture_image_to_album(self.camera_module)

    def create_current_image_number_file(self, album_name, current_image_number):
        current_image_number_file_path = os.path.join(
            self.album_dir_path,
            album_name,
            ".current_image_number.txt"
        )

        f = open(current_image_number_file_path, "w")
        f.write(str(current_image_number))
        f.close()

    def test_list_albums(self):
        self.create_temp_album("album1")
        self.create_temp_album("album2")
        test_client = self.app.test_client()
        response = test_client.get('/albums/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        content = response.json
        self.assertEqual(len(content["available_albums"]), 2)
        self.assertIn("album1", content["available_albums"])
        self.assertIn("album2", content["available_albums"])

    def test_create_album(self):
        test_client = self.app.test_client()
        PARAMS = {
            "album_name": "album1",
            "description": "A very nice album indeed"
        }

        # Make sure there are no albums
        album_folders = os.listdir(self.album_dir_path)
        self.assertEqual(len(album_folders), 0)

        # This request should create the album specified with PARAMS
        response = test_client.post(
            '/albums',
            data=json.dumps(PARAMS),
            content_type='application/json',
            follow_redirects=True)
        content = response.json

        # Check that the response is correct
        self.assertIn("album_url", content)
        self.assertIn("album_name", content)
        self.assertIn(content["album_name"], "album1")
        self.assertEqual(content["album_url"], "/albums/album1")

        # Check that the album exists
        album_folders = os.listdir(self.album_dir_path)
        self.assertEqual(len(album_folders), 1)
        self.assertIn("album1", os.listdir(self.album_dir_path))

        # Check that the album contains the right files and folders
        album_content = os.listdir(os.path.join(self.album_dir_path, "album1"))
        self.assertIn("description.txt", album_content)
        self.assertIn("images", album_content)
        self.assertIn("thumbnails", album_content)

        # Check that the description is correct
        description_file_path = os.path.join(
            self.album_dir_path,
            "album1",
            "description.txt"
        )
        f = open(description_file_path, "r")
        content = f.read()
        f.close()
        self.assertEqual(content, "A very nice album indeed")

    def test_create_album_without_album_name_parameter(self):
        test_client = self.app.test_client()

        # Make sure there are no albums
        album_folders = os.listdir(self.album_dir_path)
        self.assertEqual(len(album_folders), 0)

        # This request should give an error
        response = test_client.post('/albums/', content_type='application/json')
        content = response.json

        # Make sure the response was an error
        self.assertIn("error", content)

        # Check that there are still no albums
        album_folders = os.listdir(self.album_dir_path)
        self.assertEqual(len(album_folders), 0)

    def test_update_album_description(self):
        self.create_temp_album("album1", description="This is not a very nice album")

        # Make sure there only exist one album
        album_folders = os.listdir(self.album_dir_path)
        self.assertEqual(len(album_folders), 1)

        test_client = self.app.test_client()
        PARAMS = {
            "album_name": "album1",
            "description": "This is definitely a very nice album"
        }

        # This request should update the album description
        response = test_client.post(
            '/albums',
            data=json.dumps(PARAMS),
            content_type='application/json',
            follow_redirects=True)
        content = response.json

        # Check that the response is correct
        self.assertIn("album_url", content)
        self.assertIn("album_name", content)
        self.assertIn(content["album_name"], "album1")
        self.assertEqual(content["album_url"], "/albums/album1")

        # Check that there still exists only one album
        album_folders = os.listdir(self.album_dir_path)
        self.assertEqual(len(album_folders), 1)
        self.assertIn("album1", os.listdir(self.album_dir_path))

        # Check that the description file is correct
        description_file_path = os.path.join(
            self.album_dir_path,
            "album1",
            "description.txt"
        )
        f = open(description_file_path, "r")
        content = f.read()
        f.close()
        self.assertEqual(content, "This is definitely a very nice album")

    def test_access_nonexistent_album(self):
        test_client = self.app.test_client()

        # This request should give an error as album1 does not exist
        response = test_client.get('/albums/album1', content_type='application/json')
        content = response.json

        self.assertIn("error", content)
        error_message = content["error"]
        self.assertEqual(error_message, "No album with the name \"album1\" exists")

    def test_get_info_for_empty_album_without_description_file(self):
        self.create_temp_album("album1")
        test_client = self.app.test_client()

        response = test_client.get('/albums/album1', content_type='application/json')
        content = response.json

        self.assertIn("album_name", content)
        self.assertIn("image_urls", content)
        self.assertIn("thumbnail_urls", content)
        self.assertIn("description", content)

        self.assertEqual(content["description"], "")
        self.assertEqual(len(content["image_urls"]), 0)
        self.assertEqual(len(content["thumbnail_urls"]), 0)
        self.assertEqual(content["album_name"], "album1")

    def test_get_info_for_album_with_description_file(self):
        self.create_temp_album("album1", description="This is a very nice album")

        # Create some dummy files to add to the album
        self.add_dummy_image_file_to_album("album1")
        self.add_dummy_image_file_to_album("album1")

        test_client = self.app.test_client()
        response = test_client.get('/albums/album1', content_type='application/json')
        content = response.json

        self.assertIn("album_name", content)
        self.assertIn("image_urls", content)
        self.assertIn("thumbnail_urls", content)
        self.assertIn("description", content)

        self.assertEqual(content["description"], "This is a very nice album")
        self.assertEqual(content["album_name"], "album1")

        # Check that the dummy file paths exist in the image_urls list
        self.assertEqual(len(content["image_urls"]), 2)
        self.assertEqual(len(content["thumbnail_urls"]), 2)

        expected_image1_url = "/{}/albums/album1/images/image0001.png".format(self.static_dir_name)
        self.assertIn(expected_image1_url, content["image_urls"])
        expected_image2_url = "/{}/albums/album1/images/image0002.png".format(self.static_dir_name)
        self.assertIn(expected_image2_url, content["image_urls"])

        expected_thumbnail1_url = "/{}/albums/album1/thumbnails/image0001.jpg".format(self.static_dir_name)
        self.assertIn(expected_thumbnail1_url, content["thumbnail_urls"])
        expected_thumbnail2_url = "/{}/albums/album1/thumbnails/image0002.jpg".format(self.static_dir_name)
        self.assertIn(expected_thumbnail2_url, content["thumbnail_urls"])

    def test_last_image_for_album(self):
        self.create_temp_album("album1")
        self.add_dummy_image_file_to_album("album1")
        self.add_dummy_image_file_to_album("album1")
        self.add_dummy_image_file_to_album("album1")

        test_client = self.app.test_client()
        response = test_client.get("/albums/album1/last_image")
        content = response.json

        self.assertIn("last_image_url", content)
        expected_url = "/{}/albums/album1/images/image0003.png".format(self.static_dir_name)
        self.assertEqual(content["last_image_url"], expected_url)

    def test_last_image_for_album_jpg(self):
        self.create_temp_album("album1")
        self.add_dummy_image_file_to_album("album1")
        self.add_dummy_image_file_to_album("album1")
        self.add_dummy_image_file_to_album("album1")

        test_client = self.app.test_client()
        response = test_client.get("/albums/album1/last_image")
        content = response.json

        self.assertIn("last_image_url", content)
        expected_url = "/{}/albums/album1/images/image0003.png".format(self.static_dir_name)
        self.assertEqual(content["last_image_url"], expected_url)

    def test_last_image_for_album_on_empty_album(self):
        self.create_temp_album("album1")

        test_client = self.app.test_client()
        response = test_client.get("/albums/album1/last_image")
        content = response.json

        self.assertNotIn("last_image_url", content)
        self.assertIn("error", content)
        self.assertEqual(content["error"], "album is empty")

    def test_capture_image_endpoint(self):
        self.create_temp_album("album1")
        test_client = self.app.test_client()

        response = test_client.post(
            "/albums/album1",
            content_type='application/json',
            follow_redirects=True)
        content = response.json

        self.assertIn("success", content)
        self.assertIn("image_url", content)
        expected_image_url = "/{}/albums/album1/images/image0001.png".format(self.static_dir_name)
        self.assertEqual(content["image_url"], expected_image_url)

        self.assertIn("thumbnail_url", content)
        expected_thumbnail_url = "/{}/albums/album1/thumbnails/image0001.jpg".format(self.static_dir_name)
        self.assertEqual(content["thumbnail_url"], expected_thumbnail_url)


if __name__ == '__main__':
    unittest.main()
