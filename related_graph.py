import requests
from bs4 import BeautifulSoup as bs

'''https://www.dictionaryapi.com/api/v1/references/thesaurus/xml/umpire?key=047c40b8-6aa2-447d-b408-e61019be5239'''


def cluster(keywords):
	url = "https://www.dictionaryapi.com/api/v1/references/thesaurus/xml/"
	key = "?key=957cd0c7-99bf-45a3-9e75-b81164f2328e"


	response_list=[]
	relatedWordDict={}
	for keyword in keywords:
		print keyword
		query = url+keyword+key
		response = requests.request("GET",query)
		soup=bs(response.content,"lxml-xml")
		for i in soup.find_all("rel"):
			response_list.append(i.text)
		response_string = " ".join(response_list)
		relatedWordDict[keyword]=[keyword]
		response_string=response_string.replace(';','').replace(',','')
		relwordslist=list(set(response_string.split(' ')))
		relatedWordDict[keyword] +=relwordslist
	#print (relatedWordDict)
	unvisitedKeywords = keywords

	counter = 0
	cluster = {}
	clusterCount = []
	with open("cluster_current_topic.txt",'w') as f:
		for unvisitedkey in unvisitedKeywords:
			unvisitedKeywords.remove(unvisitedkey)
			print unvisitedkey, counter
			clusterCount.append(1)
			cluster[unvisitedkey] = counter
			currentTopic = relatedWordDict[unvisitedkey]
			f.write(str(currentTopic)+"\n")
			flag = True
			while flag and len(unvisitedKeywords) > 0:
				flag = False
				for node in unvisitedKeywords:
					if len(set(currentTopic) & set(relatedWordDict[node])) > 0:
						flag = True
						unvisitedKeywords.remove(node)
						print node,counter
						currentTopic += relatedWordDict[node]
						currentTopic = list(set(currentTopic))
						print(currentTopic)
						f.write(str(currentTopic)+" "+str(counter)+"\n")
						clusterCount[counter] += 1
						cluster[node] = counter
			counter += 1

	print(cluster)

	# for i in range(1,len(relatedWordDict)):
	# 	nextNode=relatedWordDict.items()[i]
	# 	if startNode[1]
