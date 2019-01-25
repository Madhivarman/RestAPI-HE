import pandas as pd


class Preprocess():

    def __init__(self):
        print("Started Preprocessing the Dataset")

    def preprocess(self, df):
        """Have to preprocess the data"""
        usefulColumns = ['Author', 'Date', 'Colour', 'Verification', 'Rating', 'Title', 'Desc']

        #get copy of the dataframe
        copydf = df.copy()

        for columns in usefulColumns:
            tempdf = copydf[columns] #hold temporary data
            strplit = [x.replace("[", "") for x in tempdf]
            strplit = [x.replace(']', '') for x in strplit]
            strplit = [x.replace("'", '') for x in strplit]

            copydf[columns] = strplit

        #now separate color and split
        appearance = [attr.split(",") for attr in copydf['Colour']]
        color = [attr[0].split(":")[1] for attr in appearance]
        size = [attr[1].split(":")[1] for attr in appearance]

        copydf['Colour'] = color
        copydf['size'] = size

        return copydf