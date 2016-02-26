from pymongo import MongoClient
from bs4 import BeautifulSoup
import urllib.request
'''
Establishing a mongo connection for storing the entire collection into MongoDB for faster retrieval of URLs
'''

client = MongoClient()
db = client.indiabix
posts = db.urlCollection

'''
Root of all Domains
'''
r = urllib.request.urlopen('http://www.indiabix.com/aptitude/questions-and-answers/').read()
prefix = "http://www.indiabix.com"
soup = BeautifulSoup(r,"lxml")
nohtml = soup.get_text()

'''
Getting all Domain Links
'''
aptitude_topics = str(soup.findAll("table", { "id" : "ib-tbl-topics" }))
a = BeautifulSoup(aptitude_topics,"lxml")

'''
Iterating over each of the link and store topic_store = { DOMAIN_NAME : DOMAIN_QUESTION_URL }
'''
topic_store = {}
for link in a.find_all('a'):
	url = prefix+link.get('href')
	topic = link.get_text();
	topic_store[topic] = url

'''
Getting all pages of each Domain futhur_links = { DOMAIN NAME : [ Page1, Page2, Page3 ] }
'''
furthur_links = {}
for key,value in topic_store.items():
	print("Fetching for " + value)
	temp = urllib.request.urlopen(str(value)).read()
	soup = BeautifulSoup(temp,"lxml")
	furthur_links[key] = []
	furthur_links[key].append(value)
	next_links = (soup.findAll("p", { "class" : "ib-pager" }))[0].find_all('a')
	for link in next_links:
		href = prefix+link.get('href')
		furthur_links[key].append(href)

for key,value in furthur_links.items():
	post={"domain":key}
	post_id=posts.insert_one(post).inserted_id
	for url in value:
		print(key,":",url)
		result = db.urlCollection.update_one(
                    {"domain": key},
                      {"$push": {"tags": url}})
		 
		print("\n\n\n",result)





	
	

#print(aptitude_topics.find_all('a'));

