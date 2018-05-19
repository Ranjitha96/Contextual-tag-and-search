import nltk,os
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import pandas as pd
from nltk.corpus import wordnet as wn


wnPOS = [wn.NOUN,wn.ADJ,wn.ADV,wn.VERB]
ps = PorterStemmer()
flag = True
df = pd.read_csv('results.csv')
while flag:
	results = set()
	query = raw_input('Enter search string (0 to quit) : ')
	if query == '0':
		exit()
	synonym_set = set()
	for pos in wnPOS:
		synsets = wn.synsets(query, pos=pos)
		for synset in synsets:
			for synonym in synset.lemma_names():
				synonym_set.add(synonym)
	for word in synonym_set:
		# print(ps.stem(word))
		result =  df[df.apply(lambda row:row.str.contains(ps.stem(word.lower()),case = False).any(),axis = 1)]["file_name"].to_string(index=False)
		# print (len(result))
		if len(result) is not 12:
			results.add(result)
	for i in results:
		print(i)