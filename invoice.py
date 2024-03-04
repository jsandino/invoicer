from fpdf import FPDF


class Invoice(FPDF):
    def __init__(self, logo, details):
        super().__init__()
        self.__logo = logo
        self.__number = details.invoice_number
        self.__issuer = details.company_name
        self.__street = details.company_street
        self.__city = details.company_city
        self.__state = details.company_state
        self.__zip = details.company_zip_code
        self.__phone = details.company_phone
        self.__email = details.company_email

    @property
    def issuer(self):
        return self.__issuer

    @property
    def contact(self):
        return [
            self.__street,
            f"{self.__city}, {self.__state}, {self.__zip}",
            f"{self.__phone} \u2022 {self.__email}",
        ]

    def header(self):
      has_logo = self.add_logo()
      left_padding = 20 if has_logo else 2

      self.add_font('Anta', '', 'fonts/Anta-Regular.ttf', uni=True)
      self.add_font('Courier', '', 'fonts/CourierPrime-Regular.ttf', uni=True)

      self.set_font("Anta", "", 14)
      self.cell(left_padding) # move to the right
      self.cell(30, 10, self.issuer)

      self.set_font("Courier", "", 10)
      self.ln(5)
      self.cell(left_padding) # move to the right
      self.cell(30, 10, self.contact[0])

      self.ln(5)
      self.cell(left_padding) # move to the right
      self.cell(30, 10, self.contact[1])

      self.ln(5)
      self.cell(left_padding) # move to the right
      self.cell(30, 10, self.contact[2])

    def add_logo(self):
        if self.__logo:
          self.image(self.__logo, x=10, y=12, w=15)
          return True
        
        return False

    def print(self):
        self.add_page()
        self.add_customer_panel()
        self.output(f"invoice-{self.__number}.pdf")          


    def add_customer_panel(self):
      self.ln(10)
      
