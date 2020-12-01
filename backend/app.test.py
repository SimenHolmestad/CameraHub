import unittest
from app import create_app
import tempfile
import os
from camera_modules.dummy_camera_module import DummyCameraModule


class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Create a new album directory so that the "albums" directory
        # is left untouched while testing.
        self.static_dir = tempfile.TemporaryDirectory(dir=".")
        self.static_dir_name = self.static_dir.name.split("./")[1]
        self.album_dir_path = os.path.join(self.static_dir_name, "albums")
        os.makedirs(self.album_dir_path)

        self.camera_module = DummyCameraModule(
            self.album_dir_path,
            number_of_circles=10)
        self.app = create_app(self.static_dir_name, self.album_dir_path, self.camera_module)

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

        if description != "":
            description_file_path = os.path.join(album_directory_path, "description.txt")
            f = open(description_file_path, "w")
            f.write(description)
            f.close()

    def add_dummy_image_file_to_album(self, album_name, image_name):
        """Create a dummy image file with the specified name to the specified album. """
        path_to_image_file = os.path.join(
            self.album_dir_path,
            album_name,
            "images",
            image_name
        )
        open(path_to_image_file, 'a').close()

    def create_next_image_number_file(self, album_name, next_image_number):
        next_image_number_file_path = os.path.join(
            self.album_dir_path,
            album_name,
            ".next_image_number.txt"
        )

        f = open(next_image_number_file_path, "w")
        f.write(str(next_image_number))
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
            query_string=PARAMS,
            content_type='application/json',
            follow_redirects=True)
        content = response.json

        # Check that the response is redirected correctly
        self.assertIn("album_name", content)
        self.assertIn("image_urls", content)
        self.assertIn("description", content)

        # Check that the album exists
        album_folders = os.listdir(self.album_dir_path)
        self.assertEqual(len(album_folders), 1)
        self.assertIn("album1", os.listdir(self.album_dir_path))

        # Check that the album contains the right files and folders
        album_content = os.listdir(os.path.join(self.album_dir_path, "album1"))
        self.assertIn("description.txt", album_content)
        self.assertIn("images", album_content)

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
        self.assertIn("description", content)

        self.assertEqual(content["description"], "")
        self.assertEqual(len(content["image_urls"]), 0)
        self.assertEqual(content["album_name"], "album1")

    def test_get_info_for_album_with_description_file(self):
        self.create_temp_album("album1", description="This is a very nice album")

        # Create some dummy files to add to the album
        self.add_dummy_image_file_to_album("album1", "image1.jpg")
        self.add_dummy_image_file_to_album("album1", "image2.jpg")
        self.add_dummy_image_file_to_album("album1", "image3.jpg")

        test_client = self.app.test_client()
        response = test_client.get('/albums/album1', content_type='application/json')
        content = response.json

        self.assertIn("album_name", content)
        self.assertIn("image_urls", content)
        self.assertIn("description", content)

        self.assertEqual(content["description"], "This is a very nice album")
        self.assertEqual(content["album_name"], "album1")

        # Check that the dummy file paths exists in the image_urls list
        self.assertEqual(len(content["image_urls"]), 3)
        path_to_album_images = os.path.join(
            self.album_dir_path,
            "album1",
            "images"
        )
        self.assertIn(os.path.join("/", path_to_album_images, "image1.jpg"), content["image_urls"])
        self.assertIn(os.path.join("/", path_to_album_images, "image2.jpg"), content["image_urls"])
        self.assertIn(os.path.join("/", path_to_album_images, "image3.jpg"), content["image_urls"])

    def test_camera_module_write_next_image_number(self):
        self.create_temp_album("album1")
        self.camera_module.write_next_image_number_file("album1", 4)
        next_image_number_file_path = os.path.join(
            self.album_dir_path,
            "album1",
            ".next_image_number.txt"
        )
        f = open(next_image_number_file_path)
        next_image_number = int(f.read())
        f.close()

        self.assertEqual(next_image_number, 4)

    def test_camera_module_find_next_image_number(self):
        self.create_temp_album("album1")
        self.create_next_image_number_file("album1", 3)
        self.assertEqual(self.camera_module.find_next_image_number("album1"), 3)

    def test_find_next_image_number_empty_dir_and_nonexistent_file(self):
        self.create_temp_album("album1")
        self.assertEqual(self.camera_module.find_next_image_number("album1"), 1)

    def test_find_next_image_number_with_multiple_images_and_nonexistent_file(self):
        self.create_temp_album("album1")
        self.add_dummy_image_file_to_album("album1", "image0001.png")
        self.add_dummy_image_file_to_album("album1", "image0002.png")
        self.add_dummy_image_file_to_album("album1", "image0003.png")
        self.assertEqual(self.camera_module.find_next_image_number("album1"), 4)

    def test_find_next_image_number_with_multiple_images_weird_order_and_nonexistent_file(self):
        self.create_temp_album("album1")
        self.add_dummy_image_file_to_album("album1", "image0003.png")
        self.add_dummy_image_file_to_album("album1", "image0005.png")
        self.add_dummy_image_file_to_album("album1", "image0011.png")
        self.assertEqual(self.camera_module.find_next_image_number("album1"), 12)

    def test_find_next_image_number_with_wrong_file(self):
        self.create_temp_album("album1")
        self.add_dummy_image_file_to_album("album1", "image0001.png")
        self.add_dummy_image_file_to_album("album1", "image0002.png")
        self.add_dummy_image_file_to_album("album1", "image0003.png")
        self.create_next_image_number_file("album1", 1)
        self.assertEqual(self.camera_module.find_next_image_number("album1"), 4)

    def test_camera_module_try_capture_image(self):
        self.create_temp_album("album1")
        self.add_dummy_image_file_to_album("album1", "image0001.png")
        self.add_dummy_image_file_to_album("album1", "image0002.png")
        self.add_dummy_image_file_to_album("album1", "image0003.png")
        self.create_next_image_number_file("album1", 4)

        static_image_path = self.camera_module.try_capture_image("album1")
        self.assertIn("0004", static_image_path)

        image_path = os.path.join(self.static_dir_name, static_image_path)

        # Make sure the new image file exist
        self.assertTrue(os.path.exists(image_path))

        # Make sure image number file is updated
        next_image_number_file_path = os.path.join(
            self.album_dir_path,
            "album1",
            ".next_image_number.txt"
        )
        f = open(next_image_number_file_path)
        next_image_number = int(f.read())
        f.close()

        self.assertEqual(next_image_number, 5)

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
        expected_url = "/{}/albums/album1/images/image0001.png".format(self.static_dir_name)
        self.assertEqual(content["image_url"], expected_url)


if __name__ == '__main__':
    unittest.main()
