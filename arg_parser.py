import argparse
import magic
import sys
from pathlib import Path


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "-l",
            "--logo",
            metavar="image_file",
            help="path to image logo to include in header",
        )
        self.parser.add_argument(
            "-d",
            "--details",
            metavar="details_file",
            required=True,
            help="path to json file with invoice details",
        )
        self.parser.add_argument(
            "-i",
            "--items",
            metavar="items_file",
            required=True,
            help="path to csv file with invoice items",
        )

    def validate_input(self):
        args = self.parser.parse_args()
        self.__check_logo(args.logo)
        self.__check_file(args.details, "details")
        self.__check_file(args.items, "items")
        return args.logo, args.details, args.items

    def __check_logo(self, logo):
        if logo:
            try:
                file_type = magic.from_file(logo, mime=True)
                if file_type != "image/png" and file_type != "image/jpeg":
                    print("Invalid image: expected a png or jpg", file=sys.stderr)
                    sys.exit(2)
            except FileNotFoundError:
                print(f"Logo image '{logo}' not found", file=sys.stderr)
                sys.exit(1)

    def __check_file(self, file_path, label):
        file = Path(file_path)
        if not file.exists():
            print(f"Invoice {label} file '{file}' not found", file=sys.stderr)
            exit(3)
