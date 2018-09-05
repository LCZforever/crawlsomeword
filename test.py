from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError

def getTitle(url):
	try:
		html=urlopen(url)
	except HTTPError as e:
		return None
	try:
		bsObj=BeautifulSoup(html.read())
		title=bsObj.body.h1
	except AttributeError as e:
		return None
	return title

def getName(url):
	try:
		html=urlopen(url)
	except HTTPError as e:
		return None
	try:
		bsObj=BeautifulSoup(html)
		namelist=bsObj.findAll("span",{"class":"green"})
	except AttributeError as e:
		return None
	return namelist
	
								
url="http://www.pythonscraping.com/pages/page1.html"
url2="http://www.pythonscraping.com/pages/warandpeace.html"
title=getTitle(url)
nameList=getName(url2)
if title==None:
	print("Title could not be found")
else:
	print(title)	
if nameList==None:
	print("Namelist could not be found")
else:
	for name in nameList:
		print(name.get_text())					

