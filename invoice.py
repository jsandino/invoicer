from datetime import date
from fpdf import FPDF


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


    def __add_fonts(self):
      self.add_font('Anta', '', 'fonts/Anta-Regular.ttf')
      self.add_font('CourierPrime', '', 'fonts/CourierPrime-Regular.ttf')
      self.add_font('CourierPrimeBold', 'B', 'fonts/CourierPrime-Bold.ttf')
      self.add_font('CourierPrimeItalic', 'I', 'fonts/CourierPrime-Italic.ttf')


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
            f"{self.__customer_city}, {self.__customer_state}, {self.__customer_zip}"
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


    def __str__(self):
        return self.invoice_number
    

    @property
    def invoice_number(self):
        return f"Invoice # {self.__number}"


    def header(self):
      self.add_logo()
      left_padding = self.left_margin

      self.set_font("Anta", "", 14)
      self.cell(left_padding) # move to the right
      self.cell(30, 10, self.issuer)

      self.set_font("CourierPrime", "", 10)
      for contact_info in self.contact:
        self.ln(5)
        self.cell(left_padding) # move to the right
        self.cell(30, 10, contact_info)


    def footer(self):
        self.set_y(-15)
        self.set_font("CourierPrimeItalic", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, self.invoice_number, align="L")
        self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align="R")


    def add_logo(self):
        if self.__logo:
          self.image(self.__logo, x=10, y=11, w=15)

    @property
    def left_margin(self):
        return 20 if self.__logo else 2

    def print(self):
        self.add_page()
        self.add_top_panel()
        self.add_customer_info()
        self.add_invoice_info()
        self.add_terms_info()
        self.output(f"invoice-{self.__number}.pdf")          


    def add_top_panel(self):
        self.ln(Invoice.SECTION_SPACING)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        self.cell(0, 25, "", 1, 1, '')                


    def add_customer_info(self):
        top = -40
        for i, customer_info in enumerate(self.customer):
            offset = 10 * i
            self.set_x(12)      
            self.cell(10, top + offset, customer_info)


    def add_invoice_info(self):
        top = -40

        self.set_font("CourierPrimeBold", "B", 12)
        self.set_x(-45)
        self.cell(30, top, self.invoice_number)

        self.set_font("CourierPrime", "", 10)
        x_pos = self.__right_margin(self.date)
        self.set_x(x_pos)
        self.cell(30, top + 12, self.date)


    def __right_margin(self, text):
        width = self.get_string_width(text)
        return 210 - width - 14.5


    def add_terms_info(self):
        self.ln(Invoice.SECTION_SPACING)
        self.cell(30, 10, self.payable_to)
        self.ln(5)
        self.cell(30, 10, self.terms)
            

      
