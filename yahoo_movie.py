import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

MOVIE_URL = 'https://tw.movies.yahoo.com/movie_thisweek.html'


def get_web_page(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


def get_movies(dom):
    soup = BeautifulSoup(dom, 'html5lib')
    movies = []
    rows = soup.find_all('div', 'release_info')
    for row in rows:
        movie = dict()
        movie['expectation'] = int(row.find('div', 'leveltext').span.text.strip().replace('%',''))
        # print('expectation=',movie['expectation'])
        movie['ch_name'] = row.find('div', 'release_movie_name').a.text.strip()
        # print('ch_name='+movie['ch_name'])
        movie['eng_name'] = row.find('div', 'release_movie_name').find('div', 'en').a.text.strip()
        # print('eng_name='+movie['eng_name'])
        movie['movie_id'] = get_movie_id(row.find('div', 'release_movie_name').a['href'])
        # print('movie_id='+movie['movie_id'])
        movie['poster_url'] = row.find_previous_sibling('div', 'release_foto').a.img['src']
        # print('poster_url='+movie['poster_url'])
        movie['release_date'] = get_date(row.find('div', 'release_movie_time').text)
        # print('release_date='+movie['release_date'])
        movie['intro'] = row.find('div', 'release_text').text.replace(u'詳全文', '').strip()
        # print('intro='+movie['intro'])
        trailer_a = row.find('div', 'release_btn color_btnbox').find_all('a')[1]
        movie['trailer_url'] = trailer_a['href'] if 'href' in trailer_a.attrs.keys() else ''
        # print('trailer_url='+movie['trailer_url'])
        movies.append(movie)
    return movies


def get_date(date_str):
    pattern = '\d+-\d+-\d+'
    match = re.search(pattern, date_str)
    if match is None:
        return date_str
    else:
        return match.group(0)


def get_movie_id(url):
    try:
        movie_id = url.split('.html')[0].split('-')[-1]
    except:
        movie_id = url
    return movie_id


if __name__ == '__main__':
    
    moviesAll = []
    
    for i in range(1,3):
        page = get_web_page(MOVIE_URL+'?page='+str(i))
        moviesAll += get_movies(page)
     
    # 將資料轉成 DataFrame 處理
    moveResult = pd.DataFrame(moviesAll)
    
    # 依期待度的數字排序
    moveResultSort = moveResult.sort_values(by=['expectation'], ascending=False)
    print(moveResultSort)
    
    moveResultSort.to_excel('yahoo_movie.xlsx', encoding='utf-8-sig', index=False)