from pymongo import MongoClient
from bs4 import BeautifulSoup
import urllib.request 
import os.path
import collections
import re
from json import *

doma={'simple-interest':'simple_interest','profit-and-loss-exercies':'profit_and_loss','problems-train':'problems_on_train','problems_ages':'problems_on_ages','average':'average',
	'time-and-distance':'time_and_distance','problems_numbers':'problems_on_numbers','bank-aptitude-questions-answers':'pipes-cisterns','bankexams-aptitude-questions':'ratio-proportion',
	'clock-test':'clocks','volume-surface':'volume_and_surface_area',
	'boats-streams':'boats_and_streams','bankers_test':'bankers_discount','numbers':'numbers',
	'questions-answers':'percentage','surds-and-indices':'surds_and_indices'} 
domains=sorted(doma)
'''
Getting all Domain Links and question storing them in dictionary
'''

domainquestion={}
for key,value in doma.items():
	j=0
	url='http://www.treeknox.com/general/aptitude/'+str(value)+'/#Exercies-tab'
	print("\n\n",url)
	r = urllib.request.urlopen(url).read()
	soup=BeautifulSoup(r,"lxml")
	x=soup.find("ul",{"class":"pagination paginationB paginationB05"})
	for xy in x.findAll("li"):
		j=j+1
	print(key,"is domain \n")
	for i in range(0,j-4):
		if key=='bankexams-aptitude-questions':
			if i==0:
				temp='http://www.treeknox.com/general/aptitude/'+str(value)+'/#Exercies-tab'
			else:
				temp='http://www.treeknox.com/general/aptitude/'+str(value)+'/'+str(key)+'_'+str(i+1)+'.php#Exercies-tab'
		elif key=='bank-aptitude-questions-answers':
			if i==0:
				temp='http://www.treeknox.com/general/aptitude/'+str(value)+'/#Exercies-tab'
			else:
				temp='http://www.treeknox.com/general/aptitude/'+str(value)+'/'+str(key)+'_'+str(i+1)+'.php#Exercies-tab'
		elif i==0:
		    temp='http://www.treeknox.com/general/aptitude/'+str(value)+'/#Exercies-tab'
		else:
		    temp='http://www.treeknox.com/general/aptitude/'+str(value)+'/aptitude-'+str(key)+'_'+str(i+1)+'.php#Exercies-tab'
		print(temp,"\n")
		r = urllib.request.urlopen(temp).read()
		soup=BeautifulSoup(r,"lxml")
		for ntemp in soup.findAll("table",{"class":"tech"}):
		    for values in ntemp.findAll("th",{"class":"th_1"}):
		        tempques=values.get_text().strip()
		        print(tempques,"\n")
		        domainquestion.setdefault(value,[]).append(tempques)

for key,value in domainquestion.items():
	print(key,":",value,"\n")

for domain,questions in domainquestion.items():
		domain_file_name = "project8sem/corpus/treeknox/"+domain+".store"
		if os.path.isfile(domain_file_name):
			print("Skipping : ",domain)
			continue
		domain_file = open(domain_file_name, 'w')
		print("Creating Files for ",domain)
		for question in questions:
			domain_file.write(question)
			domain_file.write('\n\n')
		domain_file.close()
		print(domain," is completed !")


