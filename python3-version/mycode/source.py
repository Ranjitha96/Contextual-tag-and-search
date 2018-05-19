import csv
import operator
import nltk
import os
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import math
import pandas as pd
import random
import re
from related_graph import cluster
from sklearn.naive_bayes import MultinomialNB 
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split

ps = PorterStemmer()
features_df = pd.DataFrame()
wordList = []

def tf(word, word_list):
    return word_list.count(word)

def positionScore(word, word_list):
    value = 0.0
    indices = [i for i, x in enumerate(word_list) if x == word]
    for index in indices:
        if index > math.ceil(len(word_list)/2):
            value += index/float(len(word_list)) - 0.5
        else:
            value += 0.5 - index/float(len(word_list))
    return value

def getFeatures(fileHandle):
    text = fileHandle.read().decode('utf-8')
    text=re.sub(r'[^a-zA-Z0-9\']',' ',text)
    tokensList = nltk.word_tokenize(text)
    posTagList = nltk.pos_tag(tokensList)
    global wordList
    wordList = [w for w,s in posTagList if w not in stopword and s in REQ]
    stemmedWords = [ps.stem(w) for w,s in posTagList if w not in stopword and s in REQ]
    # print stemmedWords

    #stemmedWordsTF = {stemmedWord : tf(stemmedWord, tokensList) for stemmedWord in stemmedWords}
    #stemmedWordsPositionScore = {stemmedWord : positionScore(stemmedWord, tokensList) for stemmedWord in stemmedWords}

    freq_count = {word: tf(word, tokensList) for word in wordList}
    position_score = {word: positionScore(word, tokensList) for word in wordList}

    '''filtered_wordsToTags = {w: s for w, s in posTagList if w not in stopword and s in REQ}
    stemmedWords = [ps.stem(w) for w in filtered_wordsToTags.keys()]
    wordsToStemmed = {w : ps.stem(w) for w in filtered_wordsToTags.keys()}
    synonymToStemmedWord = {}
    relatedWordSet = {}
    freq_count = {word: tf(word, tokensList) for word in filtered_wordsToTags.keys()}
    position_score = {word: positionScore(word, tokensList) for word in filtered_wordsToTags.keys()}'''

    '''posString = ''
    for word,tag in posTagList:
        if tag in posToWN.keys():
            posString += posToWN[tag]
        else:
            posString += '.'
    j=[]
    i = posString.find('n')
    j.append(i)
    str =""
    ind = []
    nouns = [""]
    while i < len(posString) and i != -1:
        #print(str(i) + ' ' + str(j))
        # comment : consider more than 2 nouns together... Chandler Muriel Bing +ve, -ve ??
        if j[-1] == i - 1:
            nouns[-1] = " ".join(ind)
            relatedWordSet[token[i]] = [token[j[-1]]]
        else:
            nouns[-1] = " ".join(ind)
            str = ""
            ind =[]
            j=[]
            nouns.append("")
        j.append(i)
        ind.append(token[i])
        i = posString.find('n',i + 1)
    nouns.append(" ".join(ind))
    nouns = [x for x in nouns if x!='']
    for word in wordsToStemmed.keys():
        if filtered_wordsToTags[word] not in PRONOUNS:
            synset = wn.synsets(word, pos=posToWN[filtered_wordsToTags[word]])
            flag = False
            for entry in synset:
                for synonym in entry.lemma_names():
                    if synonym not in synonymToStemmedWord:
                        synonymToStemmedWord[synonym] = wordsToStemmed[word]
                        if wordsToStemmed[word] not in relatedWordSet:
                            relatedWordSet[wordsToStemmed[word]] = [word]
                    else:
                        if synonymToStemmedWord[synonym] != wordsToStemmed[word]:
                            relatedWordSet[synonymToStemmedWord[synonym]].append(word)
                        flag = True
                        break
                if flag:
                    break'''

    wordToRoot = {w: ps.stem(w) for w in wordList}
    synonymToStemmedWord = {}
    relatedWordSet = {}

    for word, pos in posTagList:
        if word not in stopword and pos in REQ:
            synset = wn.synsets(word, pos=posToWN[pos])
            flag = False
            if len(synset) is 0:
                relatedWordSet[ps.stem(word)] = [word]
                synonymToStemmedWord[word] = ps.stem(word)
                wordToRoot[word] = synonymToStemmedWord[word]
                # print word
            for entry in synset:
                # print entry
                for synonym in entry.lemma_names():
                    if synonym not in synonymToStemmedWord:
                        synonymToStemmedWord[synonym] = ps.stem(word)
                        if ps.stem(word) not in relatedWordSet:
                            relatedWordSet[ps.stem(word)] = [word]
                    else:
                        relatedWordSet[synonymToStemmedWord[synonym]].append(word)
                        wordToRoot[word] = synonymToStemmedWord[synonym]
                        flag = True
                        break
                if flag:
                    break
    # print wordToRoot

    # print(wordToRoot)
    rootWordFrequency = {}
    rootWordWeight = {}

    for root, wordli in relatedWordSet.items():
        rootWordFrequency[root] = 0
        rootWordWeight[root] = 0
        for word in wordli:
            rootWordFrequency[root] += freq_count[word]
            rootWordWeight[root] += position_score[word]
    for w,s in posTagList:
        # print w,s
        if w not in stopword and s in REQ:
            if s in NOUNS:
                pos = 1
            elif s in VERBS:
                pos = 2
            elif s in ADVS:
                pos = 3
            elif s in ADJS:
                pos = 4
            else:
                pos = 5
            # print wordToRoot[w]
            if wordToRoot[w] in rootWordFrequency:
            	features[w] = [tf(w,tokensList), positionScore(w,tokensList), rootWordFrequency[wordToRoot[w]], rootWordWeight[wordToRoot[w]], pos]
    # for w,s in posTagList:
    #     # print w
    #     if w not in stopword and s in REQ:
    #         if s in NOUNS:
    #             pos = 1
    #         elif s in VERBS:
    #             pos = 2
    #         elif s in ADVS:
    #             pos = 3
    #         elif s in ADJS:
    #             return 4
    #         else:
    #             return 5
    #         print wordToRoot[w]
    #         print(w)
    #         if wordToRoot[w] in rootWordFrequency:
    #             features[w] = [tf(w,tokensList), positionScore(w,tokensList), rootWordFrequency[wordToRoot[w]], rootWordWeight[wordToRoot[w]], pos]


stopword = stopwords.words('english')
NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']
VERBS = ['VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ']
ADJS = ['JJ', 'JJR', 'JJS']
ADVS = ['RB', 'RBR', 'RBS', 'WRB']
PRONOUNS = ['PRP', 'PRP$', 'WP', 'WP$']
REQ = NOUNS + VERBS+ADJS+ADVS
#handle named entities...

posToWN = {}
#print(wn.NOUN + ' ' + wn.VERB)
for noun in NOUNS:
    posToWN[noun] = wn.NOUN
for verb in VERBS:
    posToWN[verb] = wn.VERB
for adj in ADJS:
    posToWN[adj] = wn.ADJ
for adv in ADVS:
    posToWN[adv] = wn.ADV

isTraining = int(input('Enter 1 for training, 2 for testing :'))
path=raw_input('Enter path:')
#folder=os.listdir(path)
#print folder

if isTraining == 1:
    keysPath = path + '/Keys'
    docPath = path + '/Docs'
    allFileFeatures = {}
    files = os.listdir(keysPath)
    # print files
    for file in files:
        #print file
        docfileHandle = open(docPath+"/"+file)
        keyfileHandle = open(keysPath + '/' + file)

        features = {}

        getFeatures(docfileHandle)
        # cluster(list(set(wordList)))

        allFileFeatures[file] = features

        #keys is list of unique stemmed words from keys file
        keys = keyfileHandle.read().decode('utf-8')
        keys = keys.split()
        features_list = []
        #print features
        #print keys
        for key in keys:
            # print key 
            if key in features:
                wordList.remove(key)
                features_list.append([key,features[key][0],features[key][2],features[key][1],features[key][3],features[key][4],1])
        #append to training set
        #remove from filteredWords / stemmed words
        count = 0
        while count < len(keys) and len(wordList) != 0:
            word = wordList[random.randint(0,len(wordList))%len(wordList)]
            if word in features:
                features_list.append([word,features[word][0],features[word][2],features[word][1],features[word][3],features[word][4],0])
                count+=1
    features_df = pd.DataFrame(features_list, columns = ["word","tf","rootWordFrequency","positionScore","rootWordWeight","pos","keyword"])

    #then take same number or as many non-keywords as possible, which are now present in filteredwords, whichever is lesser
    #train
    # print(features_df)
    classifier = MultinomialNB(alpha=.8)
    X = features_df.drop(["word","keyword"],axis=1)
    y = features_df["keyword"]
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3)
    classifier.fit(X_train,y_train)
    joblib.dump(classifier,"classifier.xml")
    predictions=classifier.predict(X_test)
    print(classifier.score(X_train,y_train))
    features_df = features_df.drop_duplicates()
    features_file = open("features.csv",'w')
    features_df.to_csv(features_file)
else:
    f1 = open("results.csv","w")
    f1_writer = csv.writer(f1)
    keyword_heading = []
    for i in range(0,30):
        keyword_heading.append("keywords%d"%(i+1))
    f1_writer.writerow(["file_name"]+keyword_heading)
    # print os.listdir(path)
    for file in os.listdir(path):
	    if file.endswith(".txt"):
		    fileHandle = open(os.path.join(path,file))
		    features = {}
		    getFeatures(fileHandle)
		    classifier = joblib.load("classifier.xml")
		    predicted_words = []
            for word in list(features.keys()):
                y = classifier.predict([features[word]])
                if y[0] == 1:
		    		# f1_writer.writerow([word,features[word][0],features[word][2],features[word][1],features[word][3],features[word][4],ps.stem(word)])
                    predicted_words.append([word,features[word][2]+features[word][1]+features[word][3],ps.stem(word)])
		    predicted_df = pd.DataFrame(predicted_words,columns=["Word","sorting_values","stemmed_words"])
		    unique_values = predicted_df["stemmed_words"].unique()
		    keyword_list = []
		    count=0
		    for unique_word in unique_values:
		    	count+=1
		    	if count==31:
		    		break
		    	temp_df = predicted_df[predicted_df["stemmed_words"]==unique_word].sort_values("sorting_values",ascending = False).head(1)
		    	keyword_list.append(temp_df.iloc[0]["Word"])
            # print keyword_list
            f1_writer.writerow([file]+keyword_list)
	    #cluster(wordList)

# print features_df


'''sortedroot = sorted(features.items(), key = list(operator.itemgetter(1)).itemgetter(3),reverse=True)

    count = 0
    for (word,scores) in sortedroot:
        count+=1
        print ("%s - %f"%(word,scores))
        if count >10:
            break''' 
    #load classifier, pass features to get results   

#print(rootWordFrequency)
#print ("hello\n")
#print(rootWordWeight)

# zts = zip(tags,stemmed)
# print zts
# mapped_words = dict(zts)
# print(mapped_words)
# for stem in stemmed:
# 	if tags[stemmed.index(stem)]
# count = {}

# def mapper(wn_pos, nltk_pos):


# list_pos = NOUNS + VERBS + ADJS + ADVS
# print
# list_pos

#
# for stem in stemmed:
# 	wn.synsets(stem,pos= wn)
