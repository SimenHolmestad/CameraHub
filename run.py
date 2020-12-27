import sys
import argparse
from backend.camera_module_options import get_camera_module_name_options
from run_commands.command_options import get_instance_of_run_config_by_name, get_command_names


def main():
    raw_args = sys.argv
    parsed_args = parse_command_line_args()
    run_config = get_instance_of_run_config_by_name(parsed_args.command, parsed_args, raw_args)
    run_config.run()


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("command",
                        help="The name of the command you want to use",
                        choices=get_command_names())
    camera_module_name_options = get_camera_module_name_options()
    parser.add_argument("-c", "--camera_module",
                        help="The name of the camera module to use. Defaults to \"dummy\"",
                        choices=camera_module_name_options,
                        default=camera_module_name_options[0])
    return parser.parse_args()


if __name__ == '__main__':
    main()
