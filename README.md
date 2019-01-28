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

       python scrapping.py

this script will automatically scrap all the data from web and stored the file as a JSON format under the directory `dataSrc`. At first this file check if already `scrapped.csv` is located in local file or not. If file is already present, the script starts preprocessing and store as a JSON format. Else, it will scrap the website and store the JSON file under the directory **dataSrc**

Once the data is present, next is to fetch results via Web API. Run the following command to activate the flask application

      python main.py

This file will create a local host provides a local host link http://127.0.0.1:5000. Click this link it will redirect to small UI webpage which has all form to filter the data attributes.

![alt text](https://github.com/Madhivarman/RestAPI-HR-/blob/master/images/frontWebUI.png)

if you query the data by Sentiment level. Use **below** or **above** in the form. For example: **below 0.6** or **above 0.6**.

The result will be served in separate webpage called http://127.0.0.1:5000/api/results

To view all customer data go to http://127.0.0.1:5000/api/customer/all

![alt text](https://github.com/Madhivarman/RestAPI-HR-/blob/master/images/resultDisplay.png)


If you find this repository helpful please mention in your project. Feel free to open the issues if you face any while running the scripts.

Make sure that you have mentioned the path correctly. If all paths are clear and correct then you won't face any problem running this application.

### NOTE ###

       1. This application can query **Multiple combinations of attributes** or **single attributes**.
       2. Please make sure that you don't want to filter by Date Attribute set the toDate as large as possible. Say,Dec 31 2018
       3. Ignore other tabs in the browser ;)
       
### The Major Challenge ###

One of the use case of this problem statement is that API should able to get GET products based on Date Range. Traversing through Date Range(string) object is impossible. So, to GET attributes within the date Range I did the following things

  1. Convert the Date Range into TimeStamp. Convert into pandas DateTime Timestamp
  2. Get Week, month, Date respect to the year. Adding this field to main JSON File which makes us to traverse through the Date Range too easy.
  3. IMPORTANT NOTE: This is my first time try building REST API. If you find any error, or  not optimized way please notify me. I will try to rectify it and resend it to you. So far, the application will works all case. :)

The Original link has only 6 reviews. I taught it's too small to the challenging problem. That's why I scrapped all the reviews for IPhone X which has total 1030 customer reviews.

### Citations ###
```
  @author{
    'Name': 'Madhivarman',
    'Project': 'Python Flask Application',
    'email': 'madhivarman451@gmail.com',
    'Version': 1.0
  }
```
