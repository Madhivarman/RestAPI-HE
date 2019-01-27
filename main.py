import flask
from people import People
from flask import request, jsonify
from flask import render_template

import os
import datetime
import pandas as pd

secret_Key = os.urandom(32)

app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.config['SECRET_KEY'] = secret_Key

@app.route('/')
def home():
    """Get all Filtering attributes we need"""
    c = list(set(i['Colour'] for i in inputFile))
    r = list(set(i['Rating'] for i in inputFile))
    s = list(set(i['size'] for i in inputFile))
    v = list(set(i['Verification'] for i in inputFile))

    return render_template('home.html', color=c, rating=r, size=s, verify=v)

@app.route('/api/customer/', methods=['GET'])
def doFetchMatchedDetails(asList):
    """Define a format list"""
    labelList = ['Color', 'Rating', 'Size', 'Verification', 'Sentiment', 'FromDate', 'ToDate']

    """zip the list"""
    zippedList = zip(labelList, asList)
    keyLabel = [(k, v) for k,v in zippedList]
    notEmptyLabel = {}
    for k, v in keyLabel:
        if not v:
            continue
        else:
            notEmptyLabel.update({k:v})

    """convert the date into week and year"""
    fromDate = notEmptyLabel['FromDate'].replace(",", '')
    fromDate = fromDate.replace("  "," ")

    toDate = notEmptyLabel['ToDate'].replace(",", '')
    toDate = toDate.replace("  ", ' ')

    fromDateobj = datetime.datetime.strptime(fromDate, '%b %d %Y')
    toDateobj = datetime.datetime.strptime(toDate, '%b %d %Y')

    pdFdate = pd.to_datetime(fromDateobj)
    pdTdate = pd.to_datetime(toDateobj)

    notEmptyLabel.update({'Fromweek':pdFdate.week})
    notEmptyLabel.update({'FromYear':pdFdate.year})

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
        notEmptyLabel.update({'week': [x for x in range(pdFdate.week, weekTotalDiff+1)]})

    if yearTotalDiff == pdFdate.year:
        notEmptyLabel.update({'year': pdFdate.year})
    else:
        notEmptyLabel.update({'year': [x for x in range(pdFdate.year, weekTotalDiff+1)]})

    attributesWeNeed = ['Color', 'Size', 'Rating', 'Verification', 'Sentiment', 'week', 'year']
    finalDict = {}

    for k,v in notEmptyLabel.items():

        if k in attributesWeNeed:
            finalDict.update({k: v})

    """Create an request API url to fetch the data"""
    url = 'http://127.0.0.1:5000/api/customer?'
    num = 1
    for k,v in finalDict.items():
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
            val = val.replace("[",'')
            val = val.replace(",", '')
            val = val.replace("]", '')
            dummyURL = url + k + "=" + val + "&"
            url = dummyURL

        num += 1 #increment the pointer to keep track
    print("check this URL to see the result:{} \n".format(url))


@app.route('/', methods=['POST'])
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
    doFetchMatchedDetails(asList)
    return render_template('home.html')

@app.route('/api/customer/all', methods=['GET'])
def api_all():
    return jsonify(inputFile)


if __name__ == '__main__':
    peopleobj = People()
    inputFile = peopleobj.readJsonFile()

    app.run()