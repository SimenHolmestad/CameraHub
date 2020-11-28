import unittest
from app import create_app
import tempfile
import os
from camera_modules.dummy_camera_module import DummyCameraModule


class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Create a new album directory so that the "albums" directory
        # is left untouched while testing.
        self.album_dir = tempfile.TemporaryDirectory(dir=".")
        self.album_dir_name = self.album_dir.name.split("./")[1]

        self.camera_module = DummyCameraModule(self.album_dir_name)
        self.app = create_app(self.album_dir_name, self.camera_module)

    def tearDown(self):
        self.album_dir.cleanup()

    def create_temp_album(self, album_name, description=""):
        """Create an album with the specified name and description."""
        album_directory_path = os.path.join(
            self.album_dir.name,
            album_name)

        os.makedirs(os.path.join(
            album_directory_path,
            "images"
        ))

        if description != "":
            description_file_path = os.path.join(album_directory_path, "description.txt")
            f = open(description_file_path, "w")
            f.write(description)
            f.close()

    def test_list_albums(self):
        self.create_temp_album("album1")
        self.create_temp_album("album2")
        test_client = self.app.test_client()
        response = test_client.get('/', content_type='application/json')
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
        album_folders = os.listdir(self.album_dir_name)
        self.assertEqual(len(album_folders), 0)

        # This request should create the album specified with PARAMS
        response = test_client.post(
            '/',
            query_string=PARAMS,
            content_type='application/json',
            follow_redirects=True)
        content = response.json

        # Check that the response is redirected correctly
        self.assertIn("album_name", content)
        self.assertIn("image_urls", content)
        self.assertIn("description", content)

        # Check that the album exists
        album_folders = os.listdir(self.album_dir_name)
        self.assertEqual(len(album_folders), 1)
        self.assertIn("album1", os.listdir(self.album_dir_name))

        # Check that the album contains the right files and folders
        album_content = os.listdir(os.path.join(self.album_dir_name, "album1"))
        self.assertIn("description.txt", album_content)
        self.assertIn("images", album_content)

        # Check that the description is correct
        description_file_path = os.path.join(
            self.album_dir_name,
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
        album_folders = os.listdir(self.album_dir_name)
        self.assertEqual(len(album_folders), 0)

        # This request should give an error
        response = test_client.post('/', content_type='application/json')
        content = response.json

        # Make sure the response was an error
        self.assertIn("error", content)

        # Check that there are still no albums
        album_folders = os.listdir(self.album_dir_name)
        self.assertEqual(len(album_folders), 0)

    def test_update_album_description(self):
        self.create_temp_album("album1", description="This is not a very nice album")

        # Make sure there only exist one album
        album_folders = os.listdir(self.album_dir_name)
        self.assertEqual(len(album_folders), 1)

        test_client = self.app.test_client()
        PARAMS = {
            "album_name": "album1",
            "description": "This is definitely a very nice album"
        }

        # This request should update the album description
        response = test_client.post(
            '/',
            query_string=PARAMS,
            content_type='application/json',
            follow_redirects=True)
        content = response.json

        # Check that the response is redirected correctly
        self.assertIn("album_name", content)
        self.assertIn("image_urls", content)
        self.assertIn("description", content)
        self.assertEqual(content["description"], "This is definitely a very nice album")

        # Check that there still exists only one album
        album_folders = os.listdir(self.album_dir_name)
        self.assertEqual(len(album_folders), 1)
        self.assertIn("album1", os.listdir(self.album_dir_name))

        # Check that the description file is correct
        description_file_path = os.path.join(
            self.album_dir_name,
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
        response = test_client.get('/album1', content_type='application/json')
        content = response.json

        self.assertIn("error", content)
        error_message = content["error"]
        self.assertEqual(error_message, "No album with the name \"album1\" exists")

    def test_get_info_for_empty_album_without_description_file(self):
        self.create_temp_album("album1")
        test_client = self.app.test_client()

        response = test_client.get('/album1', content_type='application/json')
        content = response.json

        self.assertIn("album_name", content)
        self.assertIn("image_urls", content)
        self.assertIn("description", content)

        self.assertEqual(content["description"], "")
        self.assertEqual(len(content["image_urls"]), 0)
        self.assertEqual(content["album_name"], "album1")

    def test_get_info_for_album_with_description_file(self):
        self.create_temp_album("album1", description="This is a very nice album")
        path_to_album_images = os.path.join(
            self.album_dir_name,
            "album1",
            "images"
        )

        # Create some dummy files to add to the album
        open(os.path.join(path_to_album_images, "image1.jpg"), 'a').close()
        open(os.path.join(path_to_album_images, "image2.jpg"), 'a').close()
        open(os.path.join(path_to_album_images, "image3.jpg"), 'a').close()

        test_client = self.app.test_client()
        response = test_client.get('/album1', content_type='application/json')
        content = response.json

        self.assertIn("album_name", content)
        self.assertIn("image_urls", content)
        self.assertIn("description", content)

        self.assertEqual(content["description"], "This is a very nice album")
        self.assertEqual(content["album_name"], "album1")

        # Check that the dummy file paths exists in the image_urls list
        self.assertEqual(len(content["image_urls"]), 3)
        self.assertIn(os.path.join("/", path_to_album_images, "image1.jpg"), content["image_urls"])
        self.assertIn(os.path.join("/", path_to_album_images, "image2.jpg"), content["image_urls"])
        self.assertIn(os.path.join("/", path_to_album_images, "image3.jpg"), content["image_urls"])


if __name__ == '__main__':
    unittest.main()
