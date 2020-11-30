import os
from flask import Flask, request, url_for, redirect, jsonify


def create_app(album_dir_name, camera_module):
    app = Flask(__name__, static_folder=album_dir_name)

    @app.route("/", methods=["GET", "POST"])
    def list_available_albums():
        """An endpoint for listing albums and creating new ones.

        On GET: List all available albums in CameraHub and return the
        names as a json-response.

        On POST: Create a new album named <param:album_name> if it does
        not already exists. If <param:description> is given, update the
        description of <param:album_name> with the contents of
        <param:description>. Redirects to the album info endpoint for
        <param:album_name> when done.

        """
        if request.method == "POST":
            if "album_name" not in request.args:
                return jsonify({"error": "Missing required parameter <album_name>"})

            album_name = request.args.get("album_name")
            path_to_album = os.path.join(album_dir_name, album_name)

            # Create album if it does noe exist
            if not os.path.exists(path_to_album):
                os.makedirs(path_to_album)
                album_images_path = os.path.join(path_to_album, "images")
                os.makedirs(album_images_path)

            # Update album description if <param:description> is given.
            if "description" in request.args:
                description_file_path = os.path.join(path_to_album, "description.txt")
                f = open(description_file_path, "w")
                f.write(request.args.get("description"))
                f.close()

            return redirect(url_for("album_info", album_name=album_name))

        albums = os.listdir(album_dir_name)
        albums.sort()
        return jsonify({"available_albums": albums})

    @app.route("/<album_name>", methods=["GET", "POST"])
    def album_info(album_name):
        """An endpoint for listing images in an album or capture a new one

        On GET: Returns a list of the image links for all images in
        <album_name>. If an album with <album_name> does not exist, an
        error response is returned instead.

        On POST: Try to capture an image with the camera module and
        add the image to <album_name>. The response is the dictionary
        returned from the try_capture_image function of the camera
        module.

        """
        try:
            image_names = os.listdir(
                os.path.join(album_dir_name, album_name, "images"))
        except FileNotFoundError:
            error_message = "No album with the name \"{}\" exists".format(album_name)
            return jsonify({"error": error_message})

        if request.method == "POST":
            return jsonify(camera_module.try_capture_image(album_name))

        description = ""
        album_description_path = os.path.join(
            album_dir_name,
            album_name,
            "description.txt"
        )

        if os.path.exists(album_description_path):
            f = open(album_description_path, "r")
            description = f.read()
            f.close()

        image_names.sort()
        image_urls = list(map(
            lambda image: url_for(
                "static",
                filename="{}/images/{}".format(album_name, image)
            ), image_names
        ))

        return jsonify({
            "album_name": album_name,
            "image_urls": image_urls,
            "description": description,
        })

    return app
