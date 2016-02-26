from pymongo import MongoClient
from bs4 import BeautifulSoup
import urllib.request 
import os.path
import collections
import re
from json import *
import urllib.error
from operator import itemgetter  

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.indiabix

urlCollection = db.urlCollection
domains={'simple-interest':32,'profit-and-loss':21,'problems-on-trains':19,'problems-on-ages':22,'average':23,'permutation-and-combination':24,'h.c.f-and-l.c.m':25,'time-and-distance':31}
_offset=[0,31,61,91]
_pageno=[0,1,2,3]
urllist={}
'''
Root of all Domains
'''
dom=sorted(domains)
for domain in dom:
  for i in range(0,4):
    offset=_offset[i]
    pageno=_pageno[i]
    if i==0:
        temp ='http://www.knowaptitude.in/questions/dumps/aptitude/arithmetic-aptitude/'+str(domain)+'?type=latest'
    else:   
        temp='http://www.knowaptitude.in/ajax/Questions/dump_fetch/30/1/'+str(offset)+'/'+str(pageno)+'/4/'+str(domains[domain])+'/-1?type=latest'
    urllist.setdefault(domain,[]).append(temp)
'''
Getting all Domain Links
'''
domques={}
foption=[]
sdomain=sorted(urllist)
for key in sdomain:
    i=0
    for values in urllist[key]:
        r = urllib.request.urlopen(values).read()
        soup=BeautifulSoup(r,"lxml")
        for ntemp in soup.findAll("div",{"class":"dump_question"}):
            if i==0:
                hquestion=ntemp.get_text().replace("\\r","").replace("\\n","").replace("\\t","").replace("\t","").replace("\\","")
                finalquestion=re.findall('[0-9]{1,2}\)(.*)',hquestion)
                fquestion=finalquestion[0].lstrip()
            else:
                hquestion=ntemp.get_text().replace("\\r","").replace("\\n","").replace("\\t","").replace("\t","").replace("\\","")
                finalquestion=re.findall('[0-9]??\)(.+?) A\.',hquestion)
                fquestion=finalquestion[0].lstrip()
            domques.setdefault(key,[]).append(fquestion)
        i=i+1


for key,value in domques.items():
    print("\n\n\n domain is ",key,"\n questions are :",value)

for domain in domques.keys():
    #Opening a file for each domain
    domain_file_name = "corpus/aptitude/"+str(domain)+".store"
    if os.path.isfile(domain_file_name):
        print("Skipping : ",domain)
        continue
    domain_file = open(domain_file_name, 'w')
    print("Creating Files for ",domain)
    for question_div in domques[domain]:
            domain_file.write(question)
            domain_file.write('\n')
    domain_file.close()
    print(domain," is completed !")


