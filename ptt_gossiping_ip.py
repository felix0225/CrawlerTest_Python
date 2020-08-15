import requests
import time
import re
from bs4 import BeautifulSoup

pttUrl = 'https://www.ptt.cc'
API_KEY = 'YOUR_API_KEY'


def get_web_page(url):
    resp = requests.get(url, cookies={'over18': '1'})
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html5lib')

    # 取得上一頁的連結
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_link = paging_div.find_all('a')[1]['href']

    articles = []
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        # 判斷發文日期
        if d.find('div', 'date').text.strip() == date:
            # 取得推文數
            push_count = 0
            push_str = d.find('div', 'nrec').text
            if push_str:
                try:
                    push_count = int(push_str)
                except ValueError:
                    # 若轉換失敗，可能是'爆'或 'X1', 'X2', ...
                    # 若不是, 不做任何事，push_count 保持為 0
                    if push_str == '爆':
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = -10

            # 取得文章日期、標題、連結、推數、發文者
            if d.find('a'):
                href = d.find('a')['href']
                title = d.find('a').text
                author = d.find(
                    'div', 'author').text if d.find(
                    'div', 'author') else ''
                articles.append({
                    'date': date,
                    'title': title,
                    'href': pttUrl + href,
                    'push_count': push_count,
                    'author': author
                })
    return articles, prev_link


def get_ip(dom):
    # e.g., ※ 發信站: 批踢踢實業坊(ptt.cc), 來自: 27.52.6.175
    pattern = r'來自: \d+\.\d+\.\d+\.\d+'
    match = re.search(pattern, dom)
    if match:
        return match.group(0).replace('來自: ', '')
    else:
        return None


def get_country(ip):
    if ip:
        url = f'http://api.ipstack.com/{ip}?access_key={API_KEY}'
        data = requests.get(url).json()
        country_name = data['country_name'] if data['country_name'] else None
        return country_name
    return None


if __name__ == '__main__':
    # 今天日期, 去掉開頭的 '0' 以符合 PTT 網站格式
    today = time.strftime("%m/%d").lstrip('0')

    articlesAll = []

    current_page = get_web_page(pttUrl + '/bbs/Gossiping/index.html')
    current_articles, prev_url = get_articles(current_page, today)

    # 若目前頁面有今日文章則加入 articles，並回到上一頁繼續尋找是否有今日文章
    while current_articles:
        articlesAll += current_articles
        current_page = get_web_page(pttUrl + prev_url)
        current_articles, prev_url = get_articles(current_page, today)

    print('今天共有', len(articlesAll), '篇文章')

    # 已取得文章列表，開始進入各文章尋找發文者 IP
    print('取得前 100 篇文章 IP')
    country_to_count = dict()
    for article in articlesAll[:100]:
        print('文章標題:', article['title'])
        page = get_web_page(article['href'])
        if page:
            ip = get_ip(page)
            print('查詢 IP:', ip)
            country = get_country(ip)
            if country in country_to_count.keys():
                country_to_count[country] += 1
            else:
                country_to_count[country] = 1

    # 印出各國 IP 次數資訊
    print('各國 IP 分布')
    for k, v in country_to_count.items():
        print(k, v)
