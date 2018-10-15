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
    pattern = re.compile('<dd>.*?<p class="star">(.*?)</p>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        print(item.strip())




url = 'http://maoyan.com/board/4'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' }

text = get_html(url, headers)
print(text)
#content = re.sub()
get_movie_inf(text)

