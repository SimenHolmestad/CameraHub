import os
import shutil
from PIL import Image
MAX_THUMBNAIL_SIZE = (600, 600)


def get_thumbnail_path_from_album_image_path(image_path):
    """For a given image path, output the path to the corresponding
    thumbnail
    """
    head, image_name = os.path.split(image_path)
    image_name = image_name.split(".")[0] + ".jpg"
    album_path = os.path.dirname(head)
    return os.path.join(
        album_path,
        "thumbnails",
        image_name
    )


def create_thumbnail(input_path, output_path):
    image = Image.open(input_path)
    image = image.convert('RGB')
    image.thumbnail(MAX_THUMBNAIL_SIZE)
    image.save(output_path)


def create_thumbnail_from_album_image(path_to_image):
    """Create thumbnail using file in <path_to_image>.

    Returns the thumbnail filename.
    """
    path_to_thumbnail = get_thumbnail_path_from_album_image_path(path_to_image)
    create_thumbnail(path_to_image, path_to_thumbnail)
    return os.path.split(path_to_thumbnail)[1]


def create_thumbnails_for_album(path_to_album):
    """Creates thumbnails for all images in album"""
    images_path = os.path.join(
        path_to_album,
        "images"
    )
    thumbnails_path = os.path.join(
        path_to_album,
        "thumbnails"
    )
    image_names = os.listdir(images_path)

    for image_name in image_names:
        thumbnail_name = image_name.split(".")[0] + ".jpg"
        image_path = os.path.join(
            images_path,
            image_name
        )
        thumbnail_path = os.path.join(
            thumbnails_path,
            thumbnail_name
        )
        create_thumbnail(image_path, thumbnail_path)


def create_thumbnails_for_all_albums(path_to_album_folder):
    """Checks if there are the same amount of thumbnails and images in
    each album. If not, deletes the thumbnails for the album and
    creates new ones.

    """
    for album_name in os.listdir(path_to_album_folder):
        path_to_album = os.path.join(
            path_to_album_folder,
            album_name
        )
        path_to_album_images = os.path.join(
            path_to_album,
            "images"
        )
        path_to_album_thumbnails = os.path.join(
            path_to_album,
            "thumbnails"
        )
        if not os.path.exists(path_to_album_thumbnails):
            os.makedirs(path_to_album_thumbnails)

        number_of_images = len(os.listdir(path_to_album_images))
        number_of_thumbnails = len(os.listdir(path_to_album_thumbnails))
        if number_of_images != number_of_thumbnails:
            shutil.rmtree(path_to_album_thumbnails)
            os.makedirs(path_to_album_thumbnails)
            create_thumbnails_for_album(path_to_album)
