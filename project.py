import sys
from arg_parser import ArgParser


def main():
    try:
        logo, details, tasks = parse_args()
    except Exception as e:
        sys.exit(e)


def parse_args():
    """
    Parses command-line arguments, performing preliminary validation on user inputs.
    The function returns a tuple of three elements:
    element 1 -> optional company logo (a path to a valid png or jpg image) or None
    element 2 -> path to a json file with details about the invoice
    element 3 -> path to a csv file containing all line items to be included in the invoice
    """
    return ArgParser().validate_input()


if __name__ == "__main__":
    main()
