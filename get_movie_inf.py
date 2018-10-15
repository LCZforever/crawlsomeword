import requests
import re
from requests.exceptions import RequestException


def get_html(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        print(response.status_code)
        return None
    except RequestException:
        return None

def get_movie_inf(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title':  item[2],
            'actor':  item[3].strip()[3:],
            'time':  item[4].strip()[5:],
            'score': item[5]+item[6]
        }




url = 'http://maoyan.com/board/4'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' }

html = get_html(url, headers)
#print(html)
for item in get_movie_inf(html):
    print(item)

