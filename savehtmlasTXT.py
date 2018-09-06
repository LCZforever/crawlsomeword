import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
filename = 'html_file2.txt'
url1="http://en.wikipedia.org/wiki/Comparison_of_text_editors" #网址1
url2="http://www.pythonscraping.com/pages/page3.html" #网址2
def gethtml(url):     #打开网址并返回html信息
    f=urlopen(url)
    data=f.read()
    f.close
    return data

content=gethtml(url1)
print(content)
#print(type(content))
print('\n\n\n')
print(content.decode())
html = content.decode()
with open(filename,'w', encoding='utf-8') as f:
    f.write(str(content))
