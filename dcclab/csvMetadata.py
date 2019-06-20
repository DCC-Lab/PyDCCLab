import os
import re


class CSVMetadata:
    def __init__(self, path, name=None):
        self.path = path
        self.name = name

    @property
    def header(self) -> list:
        with open(self.path, 'r') as file:
            return file.readlines()[:2]

    @property
    def read(self) -> list:
        with open(self.path, 'r') as file:
            return file.readlines()[2:]




if __name__ == '__main__':
    mtdt = CSVMetadata(r'C:\Users\MathieuLaptop\Documents\Ulaval\ProgPython\Projets\BigData-ImageAnalysis\suivi utilisation des animaux_2018\Data-souris.csv')

    headerLines = mtdt.header
    for line in headerLines:
        print(repr(line))

    lines = mtdt.read
    for line in lines:
        print(repr(line))