#import necessary libraries
from lxml import html, etree
import requests
import pandas as pd
from preprocess import Preprocess

class Scrapping():

    """Initial function"""
    def __init__(self):
    	self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    	self.headers = {'User-Agent': self.user_agent}
 

    """function to start scrapping"""
    def scrapping(self, url):
    	#create user agent
    	page = requests.get(url, headers= self.headers)
    	parser = html.fromstring(page.content)
    	xpath_reviews = '//div[@data-hook="review"]'
    	reviews = parser.xpath(xpath_reviews)


    	#extracting attributes we need
    	xpath_rating  = './/i[@data-hook="review-star-rating"]//text()' 
    	xpath_title   = './/a[@data-hook="review-title"]//text()'
    	xpath_color   = './/a[@data-hook="format-strip"]//text()'
    	xpath_author  = './/span[@class="a-profile-name"]/text()'
    	xpath_date    = './/span[@data-hook="review-date"]//text()'
    	xpath_body    = './/span[@data-hook="review-body"]//text()'
    	xpath_verified = './/span[@data-hook="avp-badge"]//text()'

    	for review in reviews:
    		author, date, color, verified, rating, title, desc = [], [], [], [], [], [], []
    		rating = review.xpath(xpath_rating)
    		title = review.xpath(xpath_title)
    		author = review.xpath(xpath_author)
    		color = review.xpath(xpath_color)
    		date = review.xpath(xpath_date)
    		body = review.xpath(xpath_body)
    		verification = review.xpath(xpath_verified)

    		author.append(author)
    		date.append(date)
    		color.append(color)
    		verified.append(verification)
    		rating.append(rating)
    		title.append(title)
    		desc.append(body)

    		json_dump.append([author, date, color, verified, rating, title, desc])
    	

if __name__ == '__main__':
	
	#create an object
	scrap = Scrapping()
	#process = Preprocess()

	#base url
	baseUrl = 'https://www.amazon.in/Apple-iPhone-Silver-Storage-Display/product-reviews/B0711T2L8K/ref=cm_cr_getr_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews&pageNumber='
	totalPage = 104

	json_dump = []

	for pn in range(1, 104):
		url = baseUrl + str(pn)
		scrap.scrapping(url)

		if pn % 50 == 0:
			print("finished scrapping for {} pages".format(pn))

	df = pd.DataFrame(json_dump, columns=['Author', 'Date', 'Colour', 'Verification', 'Rating', 'Title', 'Desc'])
	df.to_csv("df.csv", sep=",", index=False)
	process.preprocess(df)
