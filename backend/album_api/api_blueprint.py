from flask import Blueprint, request, url_for, jsonify


def construct_album_api_blueprint(album_handler, camera_module):
    """Constructs route related to accessing the albums and adding new
    images to them using the camera module
    """
    album_api_blueprint = Blueprint("albums", __name__)

    @album_api_blueprint.route("/", methods=["GET", "post"])
    def available_albums():
        """An endpoint for listing albums and create new albums.

        On GET: Return list of all available albums.

        On POST: Create a new album with the given album name if it
        does not already exists. If a description is given, set the
        description of the album.
        """

        if request.method == "POST":
            return create_or_update_album(request)
        return get_available_albums(request)

    @album_api_blueprint.route("/<album_name>", methods=["GET", "POST"])
    def album_info(album_name):
        """An endpoint for listing images in an album or capture a new image
        to the album

        On GET: Returns a list of the image links for all images in
        <album_name>.

        On POST: Try to capture an image with the camera module and
        add the image to <album_name>.

        If the album does not exist, an error message is returned.
        """
        if not album_handler.album_exists(album_name):
            error_message = "No album with the name \"{}\" exists".format(album_name)
            return jsonify({"error": error_message})

        if request.method == "POST":
            return capture_image_to_album(album_name)

        return get_album_information(album_name)

    @album_api_blueprint.route("/<album_name>/last_image", methods=["GET"])
    def last_image_for_album(album_name):
        """Returns the url of the last image captured to the specified
        album
        """
        if not album_handler.album_exists(album_name):
            error_message = "No album with the name \"{}\" exists".format(album_name)
            return jsonify({"error": error_message})

        album = album_handler.get_album(album_name)
        relative_url = album.get_relative_url_of_last_image()
        if not relative_url:
            return jsonify({
                "error": "album is empty"
            })

        return jsonify({
            "last_image_url": relative_url
        })

    def create_or_update_album(request):
        if (not request.data) or ("album_name" not in request.json):
            return jsonify({"error": "Missing required parameter <album_name>"})

        album_name = request.json.get("album_name")
        album = album_handler.get_or_create_album(album_name)

        if "description" in request.json:
            album.set_album_description(request.json.get("description"))

        return jsonify({
            "album_name": album_name,
            "album_url": url_for("albums.album_info", album_name=album_name)
        })

    def get_available_albums(request):
        album_names = album_handler.get_available_album_names()
        return jsonify({"available_albums": album_names})

    def capture_image_to_album(album_name):
        album = album_handler.get_album(album_name)
        album.try_capture_image_to_album(camera_module)

        image_url = album.get_relative_url_of_last_image()
        thumbnail_url = album.get_relative_url_of_last_thumbnail()
        return jsonify({
            "success": "Image successfully captured",
            "image_url": image_url,
            "thumbnail_url": thumbnail_url
        })

    def get_album_information(album_name):
        album = album_handler.get_album(album_name)
        description = album.get_album_description()
        image_urls = album.get_relative_urls_of_all_images()
        thumbnail_urls = album.get_relative_urls_of_all_thumbnails()

        return jsonify({
            "album_name": album_name,
            "image_urls": image_urls,
            "thumbnail_urls": thumbnail_urls,
            "description": description,
        })

    return(album_api_blueprint)
