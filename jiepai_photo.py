import json
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
from multiprocessing import Pool
from jiepai_config import *
import os
import pymongo


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_page_index(offset, keyword):  # 获取索引页HTML
    data = {'offset': offset,
            'format': 'json',
            'keyword': keyword,
            'autoload': 'true',
            'count': '20',
            'cur_tab': '1',
            'from': 'search_tab'}
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求索引出错")
        return None


def get_detail_page(url):   # 获取详情页HTML
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                             ' (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("成功加载详情页")
            print(url)
            return response.text
        return None
    except RequestException:
        print("请求详情页出错")
        return None

def get_image_content(url):     # 获取图片
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("正在从: "+url+" 下载图片")
            return response.content
        print("网站进去了，照片飞了")
        return None
    except RequestException:
        print("请求图片出错")
        return None


def parse_page_index(html):      # 从索引页获取详情页链接
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            if item.get('article_url'):
                yield item.get('article_url')


def get_photo_page(html):           # 获取详情页中图片的链接
    soup = BeautifulSoup(html, 'lxml')
    if soup:
        if not soup.title:
            print("网站请求到了，里面的HTML飞了")
            return None, None
        title = soup.title.text
        print(title)
        # print(soup.prettify())
        image_pattern = re.compile('gallery: JSON.parse\\(\\"(.*?)\\"\\)', re.S)    # 通过正则表达式找出大致位置
        result = re.search(image_pattern, html)
        data = None
        if result:
            result_data = re.sub('\\\\', '', result.group(1))   # 2个'\'字符转义，剩下2个'\'，一个对另一个进行正则转义，最终剩一个'\'
#            print(result_data)
            data = json.loads(result_data)

            # 通过json方法得到图片链接
            if data and 'sub_images' in data.keys():
                sub_images = data.get('sub_images')
                photo_url = [item.get('url') for item in sub_images]      # 用此方法没有重复的网址
                for url in photo_url:
                    print(url)
                    yield title, url
                print('-' * 30)
            # 通过进一步正则表达式得到
'''         more_pattern = re.compile('url.*?:\\"(.*?)\\"', re.S)
            result_photo = re.findall(more_pattern, result_data)
            print(type(result_photo))
            result_photo = list(set(result_photo))     # 虽然用了去重函数，但有的图片有两个不同的网址，所以仍存在重复
            if result_photo:
                for url in result_photo:
                    print(url)
                    print('-'*40)'''


def get_title_url_dict(detail_urls):      # 生成图片信息字典
    title_and_image_url = {}  # 标题与图片链接的字典
    for url in detail_urls:
        html = get_detail_page(url)
        for title, image_url in get_photo_page(html):
            if title:
                if title not in title_and_image_url:
                    title_and_image_url[title] = []
                title_and_image_url[title].append(image_url)
# print(title_and_image_url)
    return title_and_image_url


def download_photo(images_inf):     # 保存并命名图片
    if not images_inf:
        return
    path = mkdir('街拍美女图片')
    for title in images_inf.keys():
        i = 0
#        print(images_inf[title])
        if type(images_inf[title]) == list:
            for url in images_inf[title]:
                with open(path+'\\'+title+str(i)+'.jpg', 'wb') as f:
                    data = get_image_content(url)
                    if data:
                        f.write(data)
                    f.close()
                i += 1


def mkdir(dir_name):
    path = os.getcwd() + '\\'+dir_name
    foder = os.path.exists(path)
    if not foder:
        os.mkdir(path)
        print("正在创建文件夹: " + dir_name)
    return path


def save_to_mongo(result):     # 储存到MONGODB数据库里
    if result:
        try:
            if db[MONGO_TABLE].insert(result):
                print("存储到MONGODB成功")
                return True
        except:
            print("你的文件名有奇怪的符号，比如'.',':','(', 请把它们去掉后重试")

    return False


def main(offset=0):
    html = get_page_index(offset, KEYWORD)   # 获取索引页
    page = parse_page_index(html)      # 获取详情页
    images_inf = get_title_url_dict(page)   # 获取图片信息，并整合成字典

    download_photo(images_inf)
    save_to_mongo(images_inf)
    print('-'*35)
 #   print(images_inf)


 # 使用多进程，别提有多牛逼了！！！
if __name__ == "__main__":
    groups = [x * 20 for x in range(GROUP_START, GROUP_STOP+1)]
    pool = Pool()
    pool.map(main, groups)
