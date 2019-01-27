# RestAPI-HE

Python Flask REST-API Application. Building REST-API over all the JSON objects and exposing HTTP URL that can be used for querying.

### REQUIREMENTS ###

1. Flask
2. Pandas
3. Urllib2(for scrapping website)
4. Json

### Running the script ###

To make HTTP request for all JSON objects we need a Scrapped data as a JSON format. To scrap the website and store the data as JSON Format run this script.

Change the Python directory to `apps` and run the following command

> python scrapping.py

this script will automatically scrap all the data from web and stored the file as a JSON format under the directory `dataSrc`. At first this file check if already `scrapped.csv` is located in local file or not. If file is already present, the script starts preprocessing and store as a JSON format. Else, it will scrap the website and store the JSON file under the directory **dataSrc**

Once the data is present, next is to fetch results via Web API. Run the following command to activate the flask application

> python main.py

This file will create a local host provides a local host link http:127.0.0.1:5000. Click this link it will redirect to small UI webpage which has all form to filter the data attributes.

![alt text](https://github.com/Madhivarman/RestAPI-HR-/blob/master/images/frontWebUI.png)

if you query the data by Sentiment level. Use **below** or **above** in the form. For example: **below 0.6** or **above 0.6**.

The result will be served in separate webpage called http://127.0.0.1:5000/api/results

![alt text](https://github.com/Madhivarman/RestAPI-HR-/blob/master/images/resultDisplay.png)


If you find this repository helpful please mention in your project. Feel free to open the issues if you face any while running the scripts.

Make sure that you have mentioned the path correctly. If all paths are clear and correct then you won't face any problem running this application.

### Citations ###
```
  @author{
    'Name': 'Madhivarman',
    'Project': 'Python Flask Application',
    'email': 'madhivarman451@gmail.com',
    'Version': 1.0
  }
```
