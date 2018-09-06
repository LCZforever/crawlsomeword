from bs4 import BeautifulSoup
from urllib.request import urlopen


htmlfile1 = 'html_file.txt'  #用html_file.txt正常点
htmlfile2 = 'html_file2.txt'
soupfile1 = 'soupfile.txt'
soupfile2 = 'soupfile2.txt'

with open(htmlfile, 'r', encoding='utf-8') as f:   #打开存放html的txt文件
    contens=f.read()              #读取文件

soup = BeautifulSoup(contens)   #创建beautifulsoup对象
print(soup.prettify())             #打印观察一下


print(soup.title.string)
print("hello")
print(soup.body.parent)


















def save_as_txt(soup,file):    #存被beautifulsoup解析过的html.soup是beautifulsoup对象
     content = soup.prettify()            #弄到字符串里去
     print(type(content))              #打印观察一下
     with open(file,'w', encoding='utf-8') as f:   #打开存beautifulsoup对象的txt文件
         f.write(content)                #写入文件

save_as_txt(soup,soupfile1)
