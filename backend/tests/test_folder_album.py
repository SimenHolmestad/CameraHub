import os
import shutil
import unittest
import tempfile
from backend.album_storage.folder_album import FolderAlbum
from backend.album_storage.folder import Folder
from .test_utils import create_fast_dummy_module


class FolderAlbumTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory(dir=".")
        self.test_dir_name = self.test_dir.name.split("./")[1]
        folder_for_album = Folder(".", self.test_dir_name)
        self.album = FolderAlbum("test_album", folder_for_album)

    def tearDown(self):
        self.test_dir.cleanup()  # Remove test_dir from file system

    def add_dummy_image_file_to_album(self, album_name, image_name):
        """Create a dummy image file with the specified name to the specified album. """
        path_to_image_file = os.path.join(
            self.test_dir_name,
            album_name,
            "images",
            image_name
        )
        open(path_to_image_file, 'a').close()

    def create_current_image_number_file(self, album_name, current_image_number):
        current_image_number_file_path = os.path.join(
            self.test_dir_name,
            album_name,
            ".current_image_number.txt"
        )

        f = open(current_image_number_file_path, "w")
        f.write(str(current_image_number))
        f.close()

    def test_creating_album_creates_album_folder(self):
        expected_album_folder_path = os.path.join(
            self.test_dir_name,
            "test_album"
        )
        self.assertTrue(os.path.exists(expected_album_folder_path))

    def test_creating_album_creates_images_folder(self):
        expected_images_folder_path = os.path.join(
            self.test_dir_name,
            "test_album",
            "images"
        )
        self.assertTrue(os.path.exists(expected_images_folder_path))

    def test_creating_album_creates_thumbnails_folder(self):
        expected_thumbnails_folder_path = os.path.join(
            self.test_dir_name,
            "test_album",
            "thumbnails"
        )
        self.assertTrue(os.path.exists(expected_thumbnails_folder_path))

    def test_newly_created_album_has_no_description(self):
        self.assertEqual(self.album.get_album_description(), "")

    def test_newly_created_album_has_no_last_image(self):
        self.assertEqual(self.album.get_relative_url_of_last_image(), None)

    def test_newly_created_album_has_no_last_thumbnail(self):
        self.assertEqual(self.album.get_relative_url_of_last_thumbnail(), None)

    def test_set_album_description(self):
        self.album.set_album_description("This album is a test")
        self.assertEqual(self.album.get_album_description(), "This album is a test")

    def test_capture_image_to_album(self):
        camera_module = create_fast_dummy_module()
        self.album.try_capture_image_to_album(camera_module)

        expected_relative_image_url = "{}/test_album/images/image0001.png".format(self.test_dir_name)
        expected_relative_thumbnail_url = "{}/test_album/thumbnails/image0001.jpg".format(self.test_dir_name)

        self.assertEqual(self.album.get_relative_url_of_last_image(), expected_relative_image_url)
        self.assertEqual(self.album.get_relative_url_of_last_thumbnail(), expected_relative_thumbnail_url)

    def test_captured_image_exists(self):
        camera_module = create_fast_dummy_module()
        self.album.try_capture_image_to_album(camera_module)

        expected_image_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "images",
            "image0001.png"
        )

        self.assertTrue(os.path.exists(expected_image_filepath))

    def test_capture_image_after_externally_adding_files(self):
        self.add_dummy_image_file_to_album("test_album", "image0001.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0002.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0003.jpg")

        camera_module = create_fast_dummy_module()
        self.album.try_capture_image_to_album(camera_module)

        expected_image_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "images",
            "image0004.png"
        )

        self.assertTrue(os.path.exists(expected_image_filepath))

    def test_capture_image_after_externally_adding_files_weird_order(self):
        self.add_dummy_image_file_to_album("test_album", "image0001.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0002.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0003.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0017.jpg")

        camera_module = create_fast_dummy_module()
        self.album.try_capture_image_to_album(camera_module)

        expected_image_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "images",
            "image0018.png"
        )

        self.assertTrue(os.path.exists(expected_image_filepath))

    def test_capture_image_with_wrong_image_number_file(self):
        self.add_dummy_image_file_to_album("test_album", "image0001.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0002.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0003.jpg")
        self.create_current_image_number_file("test_album", 20)

        camera_module = create_fast_dummy_module()
        self.album.try_capture_image_to_album(camera_module)

        expected_image_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "images",
            "image0004.png"
        )

        self.assertTrue(os.path.exists(expected_image_filepath))

    def test_capture_image_creates_thumbnail(self):
        camera_module = create_fast_dummy_module()
        self.album.try_capture_image_to_album(camera_module)

        expected_thumbnail_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "thumbnails",
            "image0001.jpg"
        )

        self.assertTrue(os.path.exists(expected_thumbnail_filepath))

    def test_image_and_thumbnail_same_number_after_capture(self):
        camera_module = create_fast_dummy_module()
        self.add_dummy_image_file_to_album("test_album", "image0001.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0002.jpg")
        self.add_dummy_image_file_to_album("test_album", "image0003.jpg")

        self.album.try_capture_image_to_album(camera_module)

        expected_thumbnail_filepath = os.path.join(
            self.test_dir_name,
            "test_album",
            "thumbnails",
            "image0004.jpg"
        )

        self.assertTrue(os.path.exists(expected_thumbnail_filepath))

    def test_ensure_thumbnails_correct(self):
        camera_module = create_fast_dummy_module()
        self.album.try_capture_image_to_album(camera_module)
        self.album.try_capture_image_to_album(camera_module)

        thumbnails_path = os.path.join(
            self.test_dir_name,
            "test_album",
            "thumbnails"
        )
        shutil.rmtree(thumbnails_path)  # Remove thumbnails folder

        self.album.ensure_thumbnails_correct()

        thumbnails_folder_content = os.listdir(thumbnails_path)
        self.assertEqual(thumbnails_folder_content, ['image0001.jpg', 'image0002.jpg'])

    def test_ensure_thumbnails_correct_with_deleted_image(self):
        camera_module = create_fast_dummy_module()
        self.album.try_capture_image_to_album(camera_module)
        self.album.try_capture_image_to_album(camera_module)
        self.album.try_capture_image_to_album(camera_module)

        path_to_image2 = os.path.join(
            self.test_dir_name,
            "test_album",
            "images",
            "image0002.png"
        )
        os.remove(path_to_image2)
        self.album.ensure_thumbnails_correct()

        thumbnails_path = os.path.join(
            self.test_dir_name,
            "test_album",
            "thumbnails"
        )
        thumbnails_folder_content = os.listdir(thumbnails_path)
        self.assertEqual(thumbnails_folder_content, ['image0001.jpg', 'image0003.jpg'])

    def test_get_url_of_all_images(self):
        camera_module = create_fast_dummy_module()
        self.album.try_capture_image_to_album(camera_module)
        self.album.try_capture_image_to_album(camera_module)
        self.album.try_capture_image_to_album(camera_module)

        relative_image_urls = self.album.get_relative_urls_of_all_images()

        expected_realtive_image_urls = [
            self.test_dir_name + "/test_album/images/image0001.png",
            self.test_dir_name + "/test_album/images/image0002.png",
            self.test_dir_name + "/test_album/images/image0003.png",
        ]
        self.assertEqual(relative_image_urls, expected_realtive_image_urls)

    def test_get_url_of_all_thumbnails(self):
        camera_module = create_fast_dummy_module()
        self.album.try_capture_image_to_album(camera_module)
        self.album.try_capture_image_to_album(camera_module)

        relative_thumbnail_urls = self.album.get_relative_urls_of_all_thumbnails()

        # The urls should be relative to album container (The folder
        # which contains all the album folders)
        expected_relative_thumnail_urls = [
            self.test_dir_name + "/test_album/thumbnails/image0001.jpg",
            self.test_dir_name + "/test_album/thumbnails/image0002.jpg",
        ]
        self.assertEqual(relative_thumbnail_urls, expected_relative_thumnail_urls)

    def test_album_empty_after_deleting_all_images(self):
        camera_module = create_fast_dummy_module()
        self.album.try_capture_image_to_album(camera_module)
        self.album.try_capture_image_to_album(camera_module)

        images_path = os.path.join(
            self.test_dir_name,
            "test_album",
            "images"
        )
        shutil.rmtree(images_path)  # Remove images folder
        os.mkdir(images_path)

        self.assertEqual(self.album.get_relative_url_of_last_image(), None)


if __name__ == '__main__':
    unittest.main()
