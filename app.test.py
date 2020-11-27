import unittest
from app import create_app
import tempfile
import os


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        # Create a new album directory so that the "albums" directory
        # is left untouched while testing.
        self.album_dir = tempfile.TemporaryDirectory(dir=".")
        self.album_dir_name = self.album_dir.name
        self.app = create_app(self.album_dir_name)

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
        test_client.post('/', query_string=PARAMS, content_type='application/json')

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


if __name__ == '__main__':
    unittest.main()
