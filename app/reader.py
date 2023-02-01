"""This is the data reader class. this class will read data from the csv and turn it into a format that the
Database model can use to feed it into the database. First, we need to find out how many columns of data there are before
we can create the database model.

I also want this class to send a reader object that contains a dictionary of values to enter into the database
Each object is to represent one vulnerability"""
import pandas
import pandas as panda
import numpy as np


class Reader:
    def __init__(self):
        self.file = None

    def __repr__(self):
        return f'Reader: file={self.file}'

    @property
    def file(self):

        return self._file

    @file.setter
    def file(self, filename):
        self._file = filename

    def read_file(self):
        ...


class CsvReader(Reader):

    def __init__(self):
        self.data = None
        Reader.__init__(self)

    def read_file(self):
        self.data = pandas.read_csv(self._file, encoding="ISO-8859-1", low_memory=False)
        return self.data

    def __str__(self):
        return f"{self.data.columns},Reader: file={self.file}"


if __name__ == '__main__':
    reader = CsvReader()
    reader.file = "../data/allitems.csv"
    data = reader.read_file()
    print(reader)
    data.iloc[[4]][['Name']]
