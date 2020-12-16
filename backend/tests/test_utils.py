from camera_modules.dummy_camera_module import DummyCameraModule


def create_fast_dummy_module():
    """Creates a faster dummy module for quicker test runs"""
    return DummyCameraModule(
        width=120,
        height=80,
        number_of_circles=5,
        min_circle_radius=5,
        max_circle_radius=15
    )
