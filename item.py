import csv
from datetime import date


class Item:
  def __init__(self, data):
    self.__set_date(data)
    self.__set_hours(data)
    self.__set_description(data)


  def __set_date(self, data):
    try:
      self.__date = date.fromisoformat(data["Date"])
    except KeyError:
      raise ValueError("Missing item date")
    except ValueError:
      item_date = data["Date"]
      raise ValueError(f"Invalid item date '{item_date}'")



  def __set_hours(self, data):
    try:
      self.__hours = float(data["Hours"])
    except KeyError:
      raise ValueError("Missing item hours")
    except ValueError:
      hours = data["Hours"]
      raise ValueError(f"Invalid number of hours: '{hours}'")
    

  def __set_description(self, data):
    try:
      self.__description = data["Description"]
      if not self.description:
        raise ValueError("Missing item description")
    except KeyError:
      raise ValueError("Missing item description")


  @property
  def date(self):
    return self.__date.strftime("%b %d, %Y")


  @property
  def hours(self):
    return self.__hours
  

  @property
  def description(self):
    return self.__description


  @property
  def data(self):
    return [self.date, f"{self.hours}", self.description]

  @classmethod
  def load_all(cls, file):
    return [Item(i) for i in Item.__items_from(file)]


  @classmethod
  def __items_from(cls, file_name):
    data = []
    with open(file_name) as f:
      for row in csv.DictReader(f):
        data.append(row)

    return data
