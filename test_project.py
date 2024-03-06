import csv
import json
from item import Item
from project import load_items, parse_args, load_details, create_invoice
from details import Details
import pytest
import sys

"""
parse_args tests
"""


def test_parse_args(monkeypatch, capsys):
    assert_valid_logo(monkeypatch, "test_data/smp.jpg")
    assert_valid_logo(monkeypatch, "test_data/smp.png")


def assert_valid_logo(monkeypatch, image_file):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "project.py",
            "-d" "test_data/details.json",
            "-i",
            "test_data/items.csv",
            "-l",
            image_file,
        ],
    )
    logo, _, _ = parse_args()
    assert logo == image_file


def test_parse_args_details_required(capsys):
    with pytest.raises(SystemExit) as pytest_error:
        parse_args()

    captured = capsys.readouterr()
    assert pytest_error.type == SystemExit
    assert "required: -d/--details" in captured.err


def test_parse_args_items_required(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["project.py", "-d" "test_data/details.json"])
    with pytest.raises(SystemExit) as pytest_error:
        parse_args()

    captured = capsys.readouterr()
    assert pytest_error.type == SystemExit
    assert "required: -i/--items" in captured.err


def test_parse_args_logo_optional(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["project.py", "-d" "test_data/details.json", "-i", "test_data/items.csv"],
    )
    logo, details, items = parse_args()
    assert details == "test_data/details.json"
    assert items == "test_data/items.csv"


def test_parse_args_logo_missing(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["project.py", "-d" "test_data/details.json", "-i", "items.csv", "-l", "bad"],
    )
    with pytest.raises(SystemExit) as pytest_error:
        parse_args()

    captured = capsys.readouterr()
    assert pytest_error.type == SystemExit
    assert captured.err == "Logo image 'bad' not found\n"


def test_parse_args_logo_invalid(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "project.py",
            "-d" "test_data/details.json",
            "-i",
            "items.csv",
            "-l",
            "project.py",
        ],
    )
    with pytest.raises(SystemExit) as pytest_error:
        parse_args()

    captured = capsys.readouterr()
    assert pytest_error.type == SystemExit
    assert captured.err == "Invalid image: expected a png or jpg\n"


def test_parse_args_details_file_missing(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["project.py", "-d" "missing.json", "-i", "test_data/items.csv"],
    )
    with pytest.raises(SystemExit) as pytest_error:
        parse_args()

    captured = capsys.readouterr()
    assert pytest_error.type == SystemExit
    assert captured.err == "Invoice details file 'missing.json' not found\n"


def test_parse_args_items_file_missing(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["project.py", "-d" "test_data/details.json", "-i", "missing.csv"],
    )
    with pytest.raises(SystemExit) as pytest_error:
        parse_args()

    captured = capsys.readouterr()
    assert pytest_error.type == SystemExit
    assert captured.err == "Invoice items file 'missing.csv' not found\n"


"""
load_details tests
"""


def test_load_details():
    details = load_details("test_data/details.json")
    assert details.company_name == "Mario's Plumbing Co"
    assert details.company_street == "Mario Bros. House"
    assert details.company_city == "Toad Town"
    assert details.company_state == "Mushroom Kingdom"
    assert details.company_zip_code == 12345
    assert details.company_phone == "416-981-2455"
    assert details.company_email == "mario@mariosplumbco.com"
    assert details.customer_name == "Bowser"
    assert details.customer_street == "Royal Dungeon"
    assert details.customer_city == "Bowser's Castle"
    assert details.customer_state == "Koopa Kingdom"
    assert details.customer_zip_code == 67890
    assert details.invoice_number == 25
    assert details.invoice_date == "2024-03-04"
    assert details.invoice_period_start == "2024-02-01"
    assert details.invoice_period_end == "2024-02-29"
    assert details.invoice_description == "Plumbing services"
    assert details.invoice_terms == 15
    assert details.invoice_unit_cost == 100.0
    assert details.invoice_tax_label == "Sales Tax"
    assert details.invoice_tax_rate == 0.13


def test_details_missing_company_attributes(capsys):
    assert_missing_details(capsys, att="company.name", error="Missing company name")
    assert_missing_details(capsys, att="company.street", error="Missing company street")
    assert_missing_details(capsys, att="company.city", error="Missing company city")
    assert_missing_details(capsys, att="company.state", error="Missing company state")
    assert_missing_details(
        capsys, att="company.zip_code", error="Missing company zip code"
    )
    assert_missing_details(capsys, att="company.phone", error="Missing company phone")
    assert_missing_details(capsys, att="company.email", error="Missing company email")


def test_details_missing_customer_attributes(capsys):
    assert_missing_details(capsys, att="customer.name", error="Missing customer name")
    assert_missing_details(
        capsys, att="customer.street", error="Missing customer street"
    )
    assert_missing_details(capsys, att="customer.city", error="Missing customer city")
    assert_missing_details(capsys, att="customer.state", error="Missing customer state")
    assert_missing_details(
        capsys, att="customer.zip_code", error="Missing customer zip code"
    )


def test_details_missing_invoice_attributes(capsys):
    assert_missing_details(capsys, att="invoice.number", error="Missing invoice number")
    assert_missing_details(capsys, att="invoice.date", error="Missing invoice date")
    assert_missing_details(
        capsys, att="invoice.period_start", error="Missing invoice period start"
    )
    assert_missing_details(
        capsys, att="invoice.period_end", error="Missing invoice period end"
    )
    assert_missing_details(
        capsys, att="invoice.description", error="Missing invoice description"
    )
    assert_missing_details(capsys, att="invoice.terms", error="Missing invoice terms")
    assert_missing_details(
        capsys, att="invoice.unit_cost", error="Missing invoice unit cost"
    )


def test_details_with_invalid_unit_cost(capsys):
    details = load_test_details("")
    details["invoice"]["unit_cost"] = "one-hundred"
    with pytest.raises(ValueError) as pytest_error:
        Details(details)

    assert pytest_error.value.args[0] == "Invalid unit cost: 'one-hundred'"


def test_details_with_missing_tax_label():
    details = load_test_details(excluding="invoice.tax_label")
    assert Details(details).invoice_tax_label == None


def test_details_with_missing_tax_rate():
    details = load_test_details(excluding="invoice.tax_rate")
    assert Details(details).invoice_tax_rate == None


"""
load_items tests
"""


def test_load_items():
    items = load_items("test_data/items.csv")
    assert len(items) == 5
    assert "Feb 05, 2024" == items[1].date
    assert 3.0 == items[1].hours
    assert "Tested pipeline fixes, looked for leaks" == items[1].description


def test_item_missing_date(capsys):
    assert_incomplete_item(capsys, att="Date", error="Missing item date")


def test_item_with_invalid_date():
    with pytest.raises(ValueError) as pytest_error:
        Item({"Date": "bad"})

    assert pytest_error.value.args[0] == "Invalid item date 'bad'"


def test_item_missing_hours(capsys):
    assert_incomplete_item(capsys, att="Hours", error="Missing item hours")


def test_item_with_invalid_hours():
    with pytest.raises(ValueError) as pytest_error:
        Item({"Date": "2024-02-01", "Hours": "five"})

    assert pytest_error.value.args[0] == "Invalid number of hours: 'five'"


def test_item_missing_description(capsys):
    assert_incomplete_item(capsys, att="Description", error="Missing item description")


def test_item_with_empty_description():
    with pytest.raises(ValueError) as pytest_error:
        Item({"Date": "2024-02-01", "Hours": "5", "Description": ""})

    assert pytest_error.value.args[0] == "Missing item description"


"""
create_invoice tests
"""


def test_create_invoice():
    invoice = create_invoice(
        "test_data/smp.png", "test_data/details.json", "test_data/items.csv"
    )
    assert invoice.issuer == "Mario's Plumbing Co"
    assert invoice.contact[0] == "Mario Bros. House"
    assert invoice.contact[1] == "Toad Town, Mushroom Kingdom, 12345"
    assert invoice.contact[2] == "416-981-2455 \u2022 mario@mariosplumbco.com"
    assert invoice.customer[0] == "Bowser"
    assert invoice.customer[1] == "Royal Dungeon"
    assert invoice.customer[2] == "Bowser's Castle, Koopa Kingdom, 67890"
    assert str(invoice) == "Invoice # 25"
    assert invoice.date == "March 04, 2024"
    assert invoice.description == "Plumbing services"
    assert invoice.terms == "Terms: 15 days net"
    assert invoice.payable_to == "Please make funds payable to: Mario's Plumbing Co"
    assert len(invoice) == 5
    assert invoice.items[3].date == "Feb 13, 2024"
    assert invoice.items[3].hours == 3.5
    assert invoice.items[3].description == "Replaced faucet on Kamek's workshop"
    assert invoice.period_start == "From: February 01, 2024"
    assert invoice.period_end == "To: February 29, 2024"
    assert invoice.total_hours == 21
    assert invoice.unit_cost == 100.0
    assert invoice.total_cost == 2100.0
    assert invoice.tax_label == "Sales Tax:"
    assert invoice.tax_rate == 0.13
    assert invoice.tax_amount == 273.0
    assert invoice.amount_due == 2373.0


def assert_missing_details(capsys, att, error):
    data = load_test_details(excluding=att)
    # with capsys.disabled():
    #     print(f"\n{data}")
    with pytest.raises(ValueError) as pytest_error:
        Details(data)

    assert pytest_error.value.args[0] == error


def load_test_details(excluding):
    with open("test_data/details.json") as file:
        data = json.load(file)

    atts = excluding.split(".")
    if len(atts) == 2:
        del data[atts[0]][atts[1]]

    return data


def assert_incomplete_item(capsys, att, error):
    data = load_test_items(excluding=att)
    # with capsys.disabled():
    #     print(f"\n{data}")
    with pytest.raises(ValueError) as pytest_error:
        Item(data[0])

    assert pytest_error.value.args[0] == error


def load_test_items(excluding=""):
    data = []
    with open("test_data/items.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            del row[excluding]
            data.append(row)

    return data
