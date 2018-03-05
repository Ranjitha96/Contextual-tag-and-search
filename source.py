import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

stopword = stopwords.words('english')
NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']
VERBS = ['VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ']
# ADJS = ['JJ', 'JJR', 'JJS']
# ADVS = ['RB', 'RBR', 'RBS', 'WRB']
PRONOUNS = ['PRP', 'PRP$', 'WP', 'WP$']
REQ = NOUNS + VERBS + PRONOUNS

posToWN = {}
for noun in NOUNS:
	posToWN[noun] = wn.NOUN
for verb in VERBS:
	posToWN[verb] = wn.VERB

text = raw_input()
token = nltk.word_tokenize(text)
ps = PorterStemmer()
tags = nltk.pos_tag(token)
filtered_tags = {w:s for w, s in tags if w not in stopword and s in REQ}
#print(filtered_tags)
stemmed = {ps.stem(w): w for w in filtered_tags.keys()}
#print(stemmed)

synonymToStemmedWord = {}
relatedWordSet = {}

for word in stemmed.keys():
	print(word + " Stemmed")
	if filtered_tags[stemmed[word]] not in PRONOUNS:
		print(word + " Not Pronoun")
		synset = wn.synsets(word, pos=posToWN[filtered_tags[stemmed[word]]])
		for entry in synset:
			print(str(entry) + " synset entry")
			for synonym in entry.lemma_names():
				print(synonym + " synonym")
				if synonym not in synonymToStemmedWord:
					print(word + " " + synonym + " New entry")
					synonymToStemmedWord[synonym] = word
					relatedWordSet[word] = []
				else:
					print(word + " added to " + synonymToStemmedWord[synonym])
					relatedWordSet[synonymToStemmedWord[synonym]].append(word)

print(relatedWordSet)

# zts = zip(tags,stemmed)
# print zts
# mapped_words = dict(zts)
# print(mapped_words)
# for stem in stemmed:
# 	if tags[stemmed.index(stem)]
# count = {}

#def mapper(wn_pos, nltk_pos):


#list_pos = NOUNS + VERBS + ADJS + ADVS
#print
#list_pos

#
# for stem in stemmed:
# 	wn.synsets(stem,pos= wn)