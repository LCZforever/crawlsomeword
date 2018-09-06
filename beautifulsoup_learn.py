from bs4 import BeautifulSoup
from urllib.request import urlopen


filename = 'html_file.txt'
with open(filename, 'r', encoding='utf-8') as f:   #打开存放html的txt文件
    contens=f.read()              #读取文件

soup = BeautifulSoup(contens)   #创建beautifulsoup对象
print(soup.prettify())             #打印观察一下


print(soup.title.string)
print("hello")



















def save_as_txt(soup):    #存被beautifulsoup解析过的html.soup是beautifulsoup对象
     filename_write = 'soupfile.txt'    #弄个txt文件来存beautifulsoup处理后的html文件
     content = soup.prettify()            #弄到字符串里去
     print(type(content))              #打印观察一下
     with open(filename_write,'w', encoding='utf-8') as f:   #打开存beautifulsoup对象的txt文件
         f.write(content)                #写入文件
