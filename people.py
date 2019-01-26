from datetime import datetime
from flask import make_response, abort

import json

class People():

    def __init__(self):
        print("Started Filtering Accord to Conditions")

    def readJsonFile(self):
        """open and read"""
        filePath = 'apps/dataSrc/inputFile.json'
        with open(filePath) as f:
            file = json.load(f)

        inputfile = file
        return inputfile