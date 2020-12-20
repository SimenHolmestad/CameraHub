import qrcode


class QrCode:
    """A class for creating an keeping track of a single qr code."""

    def __init__(self, qr_code_folder, name, content, information_text):
        self.folder = qr_code_folder
        self.name = name
        self.filename = self.name + ".png"
        self.information_text = information_text
        self.__generate_qr_code(self.folder.get_path_to_file(self.filename), content)

    def get_relative_url(self):
        return "{}/{}".format(
            self.folder.get_name(),
            self.filename
        )

    def get_name(self):
        return self.name

    def get_information_text(self):
        return self.information_text

    def __generate_qr_code(self, file_path, content):
        """Generate a QR-code at <file_path> with the contents of
        <content>.
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(content)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        img.save(file_path)
