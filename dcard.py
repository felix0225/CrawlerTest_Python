import requests
import re
from bs4 import BeautifulSoup


def main():
    base_url = 'https://www.dcard.tw'
    url = base_url + '/f'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.105 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html5lib')

    articles = []
    # 找出所有 role="article" 的 <article> tag
    for div in soup.find_all('article', {"role": "article"}):
        title = div.find("h2").text.strip()
        lower_divs = div.find_all('div', recursive=False)
        excerpt = lower_divs[2].text.strip()
        actions = lower_divs[3].text.strip()
        nums = re.findall(r"\d+", actions)
        href = div.h2.a['href']
        articles.append({
            'title': title,
            'excerpt': excerpt,
            'bookmark': nums[0],
            'response': nums[1],
            'href': base_url + href
        })
    print('共 %d 篇' % (len(articles)))
    for a in articles[:3]:
        print(a)


if __name__ == '__main__':
    main()
