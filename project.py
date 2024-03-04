import sys
from arg_parser import ArgParser
from details import Details
from invoice import Invoice


def main():
    try:
        logo, details, tasks = parse_args()
        invoice = create_invoice(logo, details, tasks)
        invoice.print()
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

def create_invoice(logo_image, details_file, tasks_file):
    """
    Creates an invoice instance from the user supplied information.
    """
    details = load_details(details_file)
    invoice: Invoice = Invoice(logo_image, details)
    return invoice

def load_details(details_file):
    """
    Loads invoice details from a user supplied json file.
    """
    return Details.load(details_file)


if __name__ == "__main__":
    main()
