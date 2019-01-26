import flask
from people import People
from flask import request, jsonify
from flask import render_template

import os
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


@app.route('/', methods=['POST'])
def getValue():
    prod_color = request.form['color']
    prod_rating = request.form['rating']
    prod_size = request.form['size']
    prod_veri = request.form['verification']

    print([prod_color, prod_rating, prod_size, prod_veri])

    return render_template('home.html')

@app.route('/api/customer/all', methods=['GET'])
def api_all():
    return jsonify(inputFile)


if __name__ == '__main__':
    peopleobj = People()
    inputFile = peopleobj.readJsonFile()

    app.run()