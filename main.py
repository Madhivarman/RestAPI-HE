import flask
from people import People
from flask import request, jsonify
from flask import render_template

import os
import datetime
import pandas as pd
import json

secret_Key = os.urandom(32)

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = secret_Key


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/results', methods=['POST'])
def getValue():
    prod_color = request.form['color']
    prod_rating = request.form['rating']
    prod_size = request.form['size']
    prod_veri = request.form['verification']
    prod_sentiment = request.form['sentimentValue']
    prod_fromDate = request.form['fromDate']
    prod_toDate = request.form['toDate']

    """All Above variable hold the form value which generates the RestAPI to see the Json Dump"""

    asList = [prod_color, prod_rating, prod_size, prod_veri, prod_sentiment, prod_fromDate, prod_toDate]

    """Define a format list"""
    labelList = ['Colour', 'Rating', 'size', 'Verification', 'sentimentValue', 'FromDate', 'ToDate']

    """zip the list"""
    zippedList = zip(labelList, asList)
    keyLabel = [(k, v) for k, v in zippedList]
    notEmptyLabel = {}
    for k, v in keyLabel:
        if not v:
            continue
        else:
            notEmptyLabel.update({k: v})

    """convert the date into week and year"""
    fromDate = notEmptyLabel['FromDate'].replace(",", '')
    fromDate = fromDate.replace("  ", " ")

    toDate = notEmptyLabel['ToDate'].replace(",", '')
    toDate = toDate.replace("  ", ' ')

    print("From Date:{}, To Date:{}".format(fromDate, toDate))

    fromDateobj = datetime.datetime.strptime(fromDate, '%b %d %Y')
    toDateobj = datetime.datetime.strptime(toDate, '%b %d %Y')

    pdFdate = pd.to_datetime(fromDateobj)
    pdTdate = pd.to_datetime(toDateobj)

    notEmptyLabel.update({'Fromweek': pdFdate.week})
    notEmptyLabel.update({'FromYear': pdFdate.year})

    notEmptyLabel.update({'Toweek': pdTdate.week})
    notEmptyLabel.update({'Toyear': pdTdate.year})

    """calculate the distance week and year"""
    weekDiff = pdTdate.week - pdFdate.week
    yearDiff = pdTdate.year - pdFdate.year

    weekTotalDiff = pdFdate.week + weekDiff
    yearTotalDiff = pdFdate.year + yearDiff

    if weekTotalDiff == pdFdate.week:
        notEmptyLabel.update({'week': pdFdate.week})
    else:
        notEmptyLabel.update({'week': [x for x in range(pdFdate.week, weekTotalDiff + 1)]})

    if yearTotalDiff == pdFdate.year:
        notEmptyLabel.update({'year': pdFdate.year})
    else:
        notEmptyLabel.update({'year': [x for x in range(pdFdate.year, weekTotalDiff + 1)]})


    attributesWeNeed = ['Colour', 'size', 'Rating', 'Verification', 'sentimentValue', 'week', 'year']
    finalDict = {}

    for k, v in notEmptyLabel.items():

        if k in attributesWeNeed:
            finalDict.update({k: v})

    """Create an request API url to fetch the data"""
    url = 'http://127.0.0.1:5000/api/customer/asList?'
    num = 1
    for k, v in finalDict.items():
        if num == len(finalDict):
            v = str(v)
            val = v.replace(" ", '%20')
            val = val.replace("[", '')
            val = val.replace(",", '')
            val = val.replace("]", '')
            dummyURL = url + k + "=" + val
            url = dummyURL
        else:
            dummyURL = url
            """replace space by %20"""
            v = str(v)
            val = v.replace(" ", '%20')
            val = val.replace("[", '')
            val = val.replace(",", '')
            val = val.replace("]", '')
            dummyURL = url + k + "=" + val + "&"
            url = dummyURL

        num += 1  # increment the pointer to keep track
    print("check this URL to see the result:{} \n".format(url))

    """Split by ?, &"""
    splitByFilter = url.split("?")[1]
    attributeFilter = splitByFilter.split("&")
    separateFilters = [x.split('=') for x in attributeFilter]

    queryDict = {}
    for i in separateFilters:
        queryDict.update({i[0]: i[1]})

    keys = list(queryDict.keys())

    for k, v in queryDict.items():
        if k == 'week' or k == 'year':
            weekasList = []
            val = finalDict[k]
            if type(val) == 'int':
                weekasList.append(val)
            else:
                val = v.split("%20")
                for num, v in enumerate(val):
                    if num == 0:
                        weekasList.append(int(v))
                    elif num % 2 == 0 and num != 0:
                        continue
                    else:
                        weekasList.append(int(v))
            queryDict[k] = weekasList

        else:
            queryDict[k] = v

    """convert rating to integer"""
    for k, v in queryDict.items():
        if k == 'Rating' or k == 'size':
            queryDict[k] = int(v)

    values = [queryDict[val] for val in keys]

    """convert the json dump to pandas dataframe to write condition easily"""
    fileDf = pd.DataFrame.from_dict(inputFile)
    tempdf = fileDf.copy()

    """Features to pop from the list"""
    features_toPop = ["week", "year"]
    onlySingleFilters = list(set(keys) - set(features_toPop))

    indexOf = [keys.index(x) for x in onlySingleFilters]
    """iterate through the list to query the filter"""
    for phaseIcols in indexOf:
        key, value = keys[phaseIcols], values[phaseIcols]
        """if key is sentimentValue do some preprocessing"""
        if key == 'sentimentValue':
            splitByspace = value.split("%20")
            print(splitByspace)
            if splitByspace[0] == 'Above' or splitByspace[0] == 'above':
                resultdf = tempdf[tempdf[key] >= float(splitByspace[1])]
                tempdf = resultdf
            else:
                resultdf = tempdf[tempdf[key] <= float(splitByspace[1])]
                tempdf = resultdf
        else:
            resultdf = tempdf[tempdf[key] == value]
            tempdf = resultdf

    phaseIresult = tempdf

    print("Phase I result Dataframe:{}".format(phaseIresult.shape))

    """fetch data between the series"""
    phaseIcopy = phaseIresult.copy()
    phaseIIindexOf = [keys.index(x) for x in features_toPop]
    """Create an empty dataframe"""
    finalResult = pd.DataFrame()

    for d in phaseIIindexOf:
        key, value = keys[d], values[d]
        print("Key:{}, Value:{}".format(key, value))
        if type(value) == list:
            if len(value) == 1:
                resultdf = phaseIcopy[phaseIcopy[key] == value[0]]
                phaseIcopy = resultdf
            else:
                weekRangeBool = pd.Series(phaseIcopy['week'])
                first, last = value[0], value[-1]
                phaseIcopy['boolCondition'] = weekRangeBool.between(first, last)
                resultdf = phaseIcopy[phaseIcopy['boolCondition'] == True]
                phaseIcopy = resultdf
                print(phaseIcopy.shape)
        else:
            resultdf = phaseIcopy[phaseIresult[key] == value]
            phaseIcopy = resultdf

    finalResult = phaseIcopy

    print("Final Dataframe Shape is:{}".format(finalResult.shape))
    d = [
        dict([
            (colname, row[i])
            for i, colname in enumerate(finalResult.columns)
        ])
        for row in finalResult.values
    ]
    return jsonify(d)

@app.route('/api/customer/all', methods=['GET'])
def api_all():
    return jsonify(inputFile)

if __name__ == '__main__':
    peopleobj = People()
    inputFile = peopleobj.readJsonFile()
    finalresultDump = {}
    app.run()