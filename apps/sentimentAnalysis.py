from textblob import TextBlob

class SentimentAnalysis():

    def __init__(self):
        print("STARTED ANALYSING SENTIMENTS FOR REVIEWS")

    def doSentiment(self, reviews):
        """Iterate through the reviews"""
        sentiment = []
        for rev in reviews:
            testimonial = TextBlob(rev)
            sentiment.append(testimonial.sentiment.polarity)

        return sentiment
