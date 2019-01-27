import datetime
import pandas as pd

class Preprocess():

    def __init__(self):
        print("Started Preprocessing the Dataset")

    def preprocess(self, df):
        """Have to preprocess the data"""
        usefulColumns = ['Author', 'Date', 'Colour', 'Verification', 'Rating', 'Title', 'Desc']
        colsWithoutDesc = ['Author', 'Colour', 'Verification', 'size']


        #get copy of the dataframe
        copydf = df.copy()

        for columns in usefulColumns:
            tempdf = copydf[columns] #hold temporary data
            strplit = [x.replace("[", "") for x in tempdf]
            strplit = [x.replace(']', '') for x in strplit]
            strplit = [x.replace("'", '') for x in strplit]
            strplit = [x.replace("..", '') for x in strplit]

            copydf[columns] = strplit

        #now separate color and split
        appearance = [attr.split(",") for attr in copydf['Colour']]
        color = [attr[0].split(":")[1] for attr in appearance]
        size = [attr[1].split(":")[1] for attr in appearance]

        copydf['Colour'] = color
        copydf['size'] = size

        """separate out the rating star"""
        rating = [int(x.split(".")[0]) for x in copydf['Rating']]
        copydf['Rating'] = rating
        copydf['Verification'] = copydf['Verification'].apply(lambda x: 'True' if x == 'Verified Purchase' else 'False')

        for columns in colsWithoutDesc:
            tempdf = copydf[columns]
            strplit = [x.replace(',','') for x in tempdf]
            strplit = [x.replace(' ', '') for x in strplit]
            strplit = [x.replace('.', '') for x in strplit]

            copydf[columns] = strplit

        preprocessDate = [x.replace(",", '') for x in copydf['Date']]
        preprocessDate = [x.replace(".", '') for x in preprocessDate]

        """Create an dictionary"""
        dateDict = {
            "January": "Jan",
            "February": "Feb",
            "March": "Mar",
            "April": "Apr",
            "May": "May",
            "June": "Jun",
            "July": "Jul",
            "August": "Aug",
            "September": "Sep",
            "October": "Oct",
            "November": "Nov",
            "December": "Dec"
        }

        splitBySpace = []
        for date in preprocessDate:
            month = date.split(" ")[1]
            fulldate = date.replace(month, dateDict[month])
            splitBySpace.append(fulldate)

        fullweek, fullyear, fulldate, fullmonth = [], [], [], []

        for date in splitBySpace:
            """convert into datetime"""
            date = date.strip()
            nmd = datetime.datetime.strptime(date, '%d %b %Y')
            nm = pd.to_datetime(nmd)
            fullweek.append(nm.week)
            fullyear.append(nm.year)
            fulldate.append(nm.date)
            fullmonth.append(nm.month)

        """add all above data into a dataframe"""
        print([len(fullmonth), len(fullyear), len(fullweek), len(fulldate)])

        copydf['Rating'] =  pd.to_numeric(copydf['Rating'], downcast='integer')
        copydf['size'] = [x.replace("GB","") for x in pd.Series(copydf['size'])]
        copydf['size'] = pd.to_numeric(copydf['size'], downcast='integer')
        copydf['month'] = fullmonth
        copydf['year'] = fullyear
        copydf['week'] = fullweek
        copydf['date'] = fulldate

        return copydf