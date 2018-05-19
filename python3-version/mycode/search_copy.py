import nltk,os
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import pandas as pd
from nltk.corpus import wordnet as wn

def search(Query):
	wnPOS = [wn.NOUN,wn.ADJ,wn.ADV,wn.VERB]
	ps = PorterStemmer()
	df = pd.read_csv('results.csv')
	results = set()
	synonym_set = set()
	for pos in wnPOS:
		synsets = wn.synsets(Query, pos=pos)
		for synset in synsets:
			for synonym in synset.lemma_names():
				synonym_set.add(synonym)
	for word in synonym_set:
		# print(ps.stem(word))
		result =  df[df.apply(lambda row:row.str.contains(ps.stem(word.lower()),case = False).any(),axis = 1)]["file_name"]
		# print(result)
		# print (len(result))
		if result.empty != True:
			for item in result:
				results.add(item)
	return results