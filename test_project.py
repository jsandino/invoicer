from project import parse_args
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
