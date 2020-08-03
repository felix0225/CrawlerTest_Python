import requests
from bs4 import BeautifulSoup
import time
# import json
import pandas as pd

pttUrl = 'https://www.ptt.cc'


def get_web_page(url):
    resp = requests.get(url, cookies={'over18': '1'})
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html5lib')

    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_link = paging_div.find_all('a')[1]['href']

    articles = []
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('div', 'date').text.strip() == date:
            push_count = 0
            push_str = d.find('div', 'nrec').text
            if push_str:
                try:
                    push_count = int(push_str)
                except ValueError:
                    if push_str == '爆':
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = -10

            # 取得文章連結及標題
            if d.find('a'):
                href = d.find('a')['href']
                title = d.find('a').text
                author = d.find('div', 'author').text if d.find('div', 'author') else ''
                articles.append({
                    'date': date,
                    'title': title,
                    'href': pttUrl + href,
                    'push_count': push_count,
                    'author': author
                })
    return articles, prev_link


if __name__ == '__main__':
    
    today = time.strftime("%m/%d").lstrip('0')

    articlesAll = []

    current_page = get_web_page(pttUrl + '/bbs/Gossiping/index.html')

    current_articles, prev_url = get_articles(current_page, today)
    while current_articles:
        articlesAll += current_articles
        current_page = get_web_page(pttUrl + prev_url)
        current_articles, prev_url = get_articles(current_page, today)

    print('今天共有', len(articlesAll), '篇文章')

    threshold = 50
    print(f'熱門文章(> {threshold} 推):')

    # # 直接用 list 處理
    # new_articlesAll = [i for i in articlesAll if i['push_count'] > threshold]
    # for a in new_articlesAll:
    #     print(a)
    # # 存成 json 檔
    # with open('gossiping.json', 'w', encoding='utf-8') as f:
    #     json.dump(new_articlesAll, f, indent=2, sort_keys=True, ensure_ascii=False)

    # 將資料轉成 DataFrame 處理
    articlesDF = pd.DataFrame(articlesAll)
    articlesResult = articlesDF[articlesDF["push_count"] > 50]
    
    # 依推的數量排序
    articlesResultSort = articlesResult.sort_values(by=['push_count'], ascending=False)
    print(articlesResultSort)
    
    articlesResult.to_excel('ppt_gossiping.xlsx', encoding='utf-8-sig', index=False)