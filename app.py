import os
from flask import Flask, request, url_for, redirect


def create_app(album_dir_name):
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
                return {"error": "Missing required parameter <album_name>"}

            album_name = request.args.get("album_name")
            album_directory_path = os.path.join(album_dir_name, album_name)

            # Create album if it does noe exist
            if not os.path.exists(album_directory_path):
                os.makedirs(album_directory_path)
                album_images_path = os.path.join(album_directory_path, "images")
                os.makedirs(album_images_path)

            # Update album description if <param:description> is given.
            if "description" in request.args:
                description_file_path = os.path.join(album_directory_path, "description.txt")
                f = open(description_file_path, "w")
                f.write(request.args.get("description"))
                f.close()

            return redirect(url_for("album_info", album_name=album_name))

        albums = os.listdir(album_dir_name)
        albums.sort()
        return {"available_albums": albums}

    @app.route("/<album_name>")
    def album_info(album_name):
        """Returns a list of the image links for all images in <album_name>.
        If an album with <album_name> does not exist, an error response is
        returned instead.

        """
        try:
            image_names = os.listdir(
                os.path.join(album_dir_name, album_name, "images"))
        except FileNotFoundError:
            return {"error": "no such album exists"}

        description = ""
        album_description_path = os.path.join(
            album_dir_name,
            album_name,
            "description.txt")
        if os.path.exists(album_description_path):
            f = open(album_description_path)
            description = f.read()
            f.close()

        image_names.sort()
        image_urls = list(map(
            lambda image: url_for(
                "static",
                filename="{}/images/{}".format(album_name, image)
            ), image_names))

        return {
            "album_name": album_name,
            "image_urls": image_urls,
            "description": description,
        }

    return app


if __name__ == '__main__':
    album_dir_name = "albums"
    app = create_app(album_dir_name)
    app.run(debug=True)
