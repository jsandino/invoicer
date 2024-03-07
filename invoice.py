from datetime import date
from fpdf import FPDF, FontFace
from fpdf.enums import TableCellFillMode
import functools


class Invoice(FPDF):
    SECTION_SPACING = 20

    def __init__(self, logo, details, items):
        super().__init__()
        self.__add_fonts()
        self.__logo = logo
        self.__items = items
        self.__number = details.invoice_number
        self.__date = details.invoice_date
        self.__description = details.invoice_description
        self.__terms = details.invoice_terms
        self.__issuer = details.company_name
        self.__street = details.company_street
        self.__city = details.company_city
        self.__state = details.company_state
        self.__zip = details.company_zip_code
        self.__phone = details.company_phone
        self.__email = details.company_email
        self.__customer = details.customer_name
        self.__customer_street = details.customer_street
        self.__customer_city = details.customer_city
        self.__customer_state = details.customer_state
        self.__customer_zip = details.customer_zip_code
        self.__period_start = details.invoice_period_start
        self.__period_end = details.invoice_period_end
        self.__unit_cost = details.invoice_unit_cost
        self.__tax_label = details.invoice_tax_label
        self.__tax_rate = details.invoice_tax_rate

    def __add_fonts(self):
        self.add_font("Anta", "", "fonts/Anta-Regular.ttf")
        self.add_font("CourierPrime", "", "fonts/CourierPrime-Regular.ttf")
        self.add_font("CourierPrime", "B", "fonts/CourierPrime-Regular.ttf")
        self.add_font("CourierPrimeBold", "B", "fonts/CourierPrime-Bold.ttf")
        self.add_font("CourierPrimeItalic", "I", "fonts/CourierPrime-Italic.ttf")

    def __len__(self):
        return len(self.items)

    @property
    def items(self):
        return self.__items

    @property
    def issuer(self):
        return self.__issuer

    @property
    def date(self):
        invoice_date = date.fromisoformat(self.__date)
        return invoice_date.strftime("%B %d, %Y")

    @property
    def contact(self):
        return [
            self.__street,
            f"{self.__city}, {self.__state}, {self.__zip}",
            f"{self.__phone} \u2022 {self.__email}",
        ]

    @property
    def customer(self):
        return [
            self.__customer,
            self.__customer_street,
            f"{self.__customer_city}, {self.__customer_state}, {self.__customer_zip}",
        ]

    @property
    def description(self):
        return self.__description

    @property
    def terms(self):
        return f"Terms: {self.__terms} days net"

    @property
    def payable_to(self):
        return f"Please make funds payable to: {self.__issuer}"

    @property
    def period_start(self):
        start_date = date.fromisoformat(self.__period_start)
        return f"From: {start_date.strftime('%B %d, %Y')}"

    @property
    def period_end(self):
        end_date = date.fromisoformat(self.__period_end)
        return f"To: {end_date.strftime('%B %d, %Y')}"

    @property
    def total_hours(self):
        return functools.reduce(lambda total, item: total + item.hours, self.__items, 0)

    def __str__(self):
        return self.invoice_number

    @property
    def invoice_number(self):
        return f"Invoice # {self.__number}"

    @property
    def unit_cost(self):
        return self.__unit_cost

    @property
    def total_cost(self):
        return self.total_hours * self.unit_cost

    @property
    def tax_label(self):
        return f"{self.__tax_label}:"

    @property
    def tax_rate(self):
        return self.__tax_rate

    @property
    def tax_amount(self):
        return round(self.total_cost * self.tax_rate, 2)

    @property
    def amount_due(self):
        return round(self.total_cost + self.tax_amount, 2)

    def header(self):
        self.add_logo()
        left_padding = self.left_margin

        self.set_font("Anta", "", 14)
        self.cell(left_padding)  # move to the right
        self.cell(30, 10, self.issuer)

        self.set_font("CourierPrime", "", 9)
        for contact_info in self.contact:
            self.ln(5)
            self.cell(left_padding)  # move to the right
            self.cell(30, 10, contact_info)

        self.__set_content_top_margin()

    def __set_content_top_margin(self):
        top_margin = Invoice.SECTION_SPACING if self.page_no() < 3 else 40
        self.set_y(top_margin)

    def footer(self):
        self.set_y(-15)
        self.set_font("CourierPrimeItalic", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, self.invoice_number, align="L")
        self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align="R")

    def add_logo(self):
        if self.__logo:
            self.image(self.__logo, x=6, y=10, w=15)

    @property
    def left_margin(self):
        return 15 if self.__logo else 2

    def print(self):
        self.add_page()
        self.add_top_panel()
        self.add_customer_info()
        self.add_invoice_info()
        self.add_summary()
        self.add_terms_info()

        self.add_page()
        self.add_timesheet_period()
        self.add_description()
        self.add_items()

        self.output(f"invoice-{self.__number}.pdf")

    def add_top_panel(self):
        self.ln(Invoice.SECTION_SPACING)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        self.cell(0, 25, "", 1, 1, "")

    def add_customer_info(self):
        top = -40
        for i, customer_info in enumerate(self.customer):
            offset = 10 * i
            self.set_x(12)
            self.cell(10, top + offset, customer_info)

    def add_invoice_info(self):
        top = -40

        self.set_font("CourierPrimeBold", "B", 12)
        self.set_x(-44)
        self.cell(30, top, self.invoice_number, align="R")

        self.set_font("CourierPrime", "", 10)
        self.set_x(-44)
        self.cell(30, top + 12, self.date, align="R")

    def add_summary(self):
        self.ln(Invoice.SECTION_SPACING)
        self.set_draw_color(150, 150, 150)
        self.set_line_width(0.3)
        headings_style = FontFace(emphasis="", color=0)
        with self.table(
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_color=(232, 251, 255),
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=(60, 15, 30, 30),
            headings_style=headings_style,
            line_height=10,
            text_align=("CENTER", "CENTER", "CENTER", "RIGHT"),
            width=190,
            padding=[0, 1, 0, 0],
        ) as table:
            for data_row in self.summary_data:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

            self.set_font("CourierPrimeBold", "B", 11)
            row = table.row()
            row.cell("")
            row.cell("")
            row.cell("Total :", padding=[0, 1, 0, 6])
            row.cell(f"${self.amount_due:6,.2f}")

    @property
    def summary_data(self):
        return [
            ["Description", "Hours", "Unit Cost", "Amount"],
            [
                self.description,
                f"{self.total_hours}",
                f"${self.unit_cost:6,.2f} / hr.",
                f"${self.total_cost:6,.2f}",
            ],
            ["", "", "", ""],
            ["", "", "", ""],
            ["", "", "Subtotal:", f"${self.total_cost:6,.2f}"],
            ["", "", self.tax_label, f"${self.tax_amount:6,.2f}"],
        ]

    def add_terms_info(self):
        self.set_font("CourierPrime", "", 10)
        self.ln(Invoice.SECTION_SPACING)
        self.cell(30, 10, self.payable_to)
        self.ln(5)
        self.cell(30, 10, self.terms)

    def add_timesheet_period(self):
        self.set_font("CourierPrimeBold", "B", 10)
        self.cell(0, -25, "Detailed Timesheet", align="R")
        self.ln(10)

        self.set_font("CourierPrime", "", 9)
        self.cell(0, -25, self.period_start, align="R")
        self.ln(5)
        self.cell(0, -25, self.period_end, align="R")

    def add_description(self):
        self.ln(5)
        self.set_font("CourierPrimeBold", "B", 12)
        self.cell(30, 10, self.description)

    def add_items(self):
        self.ln(Invoice.SECTION_SPACING - 5)
        self.set_draw_color(150, 150, 150)
        self.set_line_width(0.3)
        headings_style = FontFace(fill_color=(220, 220, 220))
        with self.table(
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_color=(232, 251, 255),
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=(25, 15, 90),
            headings_style=headings_style,
            line_height=6,
            text_align=("LEFT", "LEFT", "LEFT"),
            width=190,
        ) as table:
            self.set_font("CourierPrimeBold", "B", 10)
            table.row(cells=["Date", "Hours", "Description"])

            self.set_font("CourierPrime", "", 9)
            for item in self.items:
                row = table.row()
                for datum in item.data:
                    row.cell(datum, padding=[0, 0, 0, 3])

            self.set_font("CourierPrimeBold", "B", 9)
            row = table.row()
            row.cell("Total Hours:", padding=[0, 0, 0, 3])
            row.cell(f"{self.total_hours}", padding=[0, 0, 0, 3])
            row.cell("")
