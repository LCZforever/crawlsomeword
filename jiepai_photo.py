import json
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
from multiprocessing import Pool
from jiepai_config import *

def get_page_index(offset,keyword):  # 获取索引页HTML
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

def get_image_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("正在从: "+url+" 下载图片")
            return response.content
        return None
    except RequestException:
        print("请求图片出错")
        return None



def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            if item.get('article_url'):
                yield item.get('article_url')


def get_photo_page(html):           # 获取详情页中图片的链接
    soup = BeautifulSoup(html, 'lxml')
    if soup:
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
                    yield title,url
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


def get_title_url_dict(detail_urls):
    title_and_image_url = {}  # 标题与图片链接的字典
    for url in detail_urls:
        html = get_detail_page(url)
        for title, image_url in get_photo_page(html):
            if title not in title_and_image_url:
                title_and_image_url[title] = []
            title_and_image_url[title].append(image_url)
    return title_and_image_url


def download_photo(images_inf):
    for title in images_inf.keys():
        i = 0
        for url in images_inf[title]:
            with open(title+str(i)+'.jpg', 'wb') as f:
                f.write(get_image_content(url))
                f.close()
            i += 1





def main(offset):
    html = get_page_index(offset, KEYWORD)   # 获取索引页
    page = parse_page_index(html)      # 获取详情页
    images_inf = get_title_url_dict(page)   # 获取图片信息，并整合成字典
 #   print(images_inf)
    download_photo(images_inf)




if __name__ == "__main__":    #使用多进程，别提有多牛逼了！！！
    group = [x * 20 for x in range(GROUP_START,GROUP_STOP+1)]
    pool = Pool()
    pool.map(main, group)
