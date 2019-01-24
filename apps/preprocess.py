import pandas as pd 


class Preprocess():

	def __init__(self):
		print("Started Preprocessing the Dataset")

	def preprocess(self, df):
		"""Have to preprocess the data"""


if __name__ == '__main__':
	process = Preprocess()
	src = pd.read_csv("df.csv", sep=",")
	process.preprocess(src)