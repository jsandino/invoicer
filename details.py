import json


class Details:
    def __init__(self, data):
        self.__set_company(data)
        self.__set_customer(data)
        self.__set_invoice(data)

    def __set_company(self, data):
        try:
          company = data["company"]
          self.company_name = company["name"]
          self.company_street = company["street"]
          self.company_city = company["city"]
          self.company_state = company["state"]
          self.company_zip_code = company["zip_code"]
          self.company_phone = company["phone"]
          self.company_email = company["email"]
        except KeyError as ke:
            raise ValueError(f"Missing company {self.att(ke)}")

    def __set_customer(self, data):
        try:
          customer = data["customer"]
          self.customer_name = customer["name"]
          self.customer_street = customer["street"]
          self.customer_city = customer["city"]
          self.customer_state = customer["state"]
          self.customer_zip_code = customer["zip_code"]
        except KeyError as ke:
            raise ValueError(f"Missing customer {self.att(ke)}")

    def __set_invoice(self, data):
        try:
          invoice = data["invoice"]
          self.invoice_number = invoice["number"]
          self.invoice_date = invoice["date"]
          self.invoice_period_start = invoice["period_start"]
          self.invoice_period_end = invoice["period_end"]
          self.invoice_description = invoice["description"]
          self.invoice_terms = invoice["terms"]
        except KeyError as ke:
            raise ValueError(f"Missing invoice {self.att(ke)}")

    def att(self, error):
        return error.args[0].replace("_", " ")

    @classmethod
    def load(cls, file):
        return Details(Details.__data_from(file))

    @classmethod
    def __data_from(cls, file_name):
        with open(file_name) as f:
            return json.load(f)
