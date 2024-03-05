import sys
from arg_parser import ArgParser
from details import Details
from invoice import Invoice
from item import Item


def main():
    try:
        logo, details, items = parse_args()
        invoice = create_invoice(logo, details, items)
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

def create_invoice(logo_image, details_file, items_file):
    """
    Creates an invoice instance from the user supplied information.
    """
    details = load_details(details_file)
    items = load_items(items_file)
    invoice: Invoice = Invoice(logo_image, details, items)
    return invoice

def load_details(details_file):
    """
    Loads invoice details from a user supplied json file.
    """
    return Details.load(details_file)

def load_items(items_file):
    """
    Loads line items from a user supplied csv file.
    """
    return Item.load_all(items_file)


if __name__ == "__main__":
    main()
