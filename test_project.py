import json
from project import parse_args, load_details
from details import Details
import pytest
import sys


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


def test_details_missing_company_attributes(capsys):
    assert_missing_attribute(capsys, att="company.name", error="Missing company name")
    assert_missing_attribute(capsys, att="company.street", error="Missing company street")
    assert_missing_attribute(capsys, att="company.city", error="Missing company city")
    assert_missing_attribute(capsys, att="company.state", error="Missing company state")
    assert_missing_attribute(capsys, att="company.zip_code", error="Missing company zip code")
    assert_missing_attribute(capsys, att="company.phone", error="Missing company phone")
    assert_missing_attribute(capsys, att="company.email", error="Missing company email")


def test_details_missing_customer_attributes(capsys):
    assert_missing_attribute(capsys, att="customer.name", error="Missing customer name")
    assert_missing_attribute(capsys, att="customer.street", error="Missing customer street")
    assert_missing_attribute(capsys, att="customer.city", error="Missing customer city")
    assert_missing_attribute(capsys, att="customer.state", error="Missing customer state")
    assert_missing_attribute(capsys, att="customer.zip_code", error="Missing customer zip code")


def test_details_missing_invoice_attributes(capsys):
    assert_missing_attribute(capsys, att="invoice.number", error="Missing invoice number")
    assert_missing_attribute(capsys, att="invoice.date", error="Missing invoice date")
    assert_missing_attribute(capsys, att="invoice.period_start", error="Missing invoice period start")
    assert_missing_attribute(capsys, att="invoice.period_end", error="Missing invoice period end")
    assert_missing_attribute(capsys, att="invoice.description", error="Missing invoice description")
    assert_missing_attribute(capsys, att="invoice.terms", error="Missing invoice terms")


def assert_missing_attribute(capsys, att, error):
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
