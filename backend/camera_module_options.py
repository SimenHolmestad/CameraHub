from .camera_modules.dummy_camera_module import DummyCameraModule
from .camera_modules.rpicam_module import RPICameraModule

CAMERA_MODULE_OPTIONS = {"dummy": DummyCameraModule,
                         "rpicam": RPICameraModule}

# The dslr modules can only be imported when gphoto2 is installed.
try:
    from .camera_modules.dslr_jpg_module import DSLRJpgModule
    from .camera_modules.dslr_raw_module import DSLRRawModule
    from .camera_modules.dslr_raw_transfer_module import DSLRRawTransferModule
    CAMERA_MODULE_OPTIONS["dslr_jpg"] = DSLRJpgModule
    CAMERA_MODULE_OPTIONS["dslr_raw"] = DSLRRawModule
    CAMERA_MODULE_OPTIONS["dslr_raw_transfer"] = DSLRRawTransferModule
except ModuleNotFoundError:
    print("DLSR modules cannot be used as gphoto2 is not available.")
    print("See intructions on how to install gphoto2 in readme.")


def get_camera_module_options():
    """returns a dictionary of the form
    {
        module_name: module_class
    }

    With the camera modules available for the system
    """
    return CAMERA_MODULE_OPTIONS
