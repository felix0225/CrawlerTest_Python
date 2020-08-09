import requests
from bs4 import BeautifulSoup


def main():
    print('自由時報即時')
    dom = requests.get('https://news.ltn.com.tw/').text
    soup = BeautifulSoup(dom, 'html5lib')
    for ele in soup.find('ul', 'list').find_all('li'):
        if ele.find('a', 'tit'):
            tit = ele.find('a', 'tit')
            print(tit.find('span','time').text.strip(),tit.find('span','title').text.strip())


if __name__ == '__main__':
    main()
