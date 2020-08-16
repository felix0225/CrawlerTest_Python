import requests
from bs4 import BeautifulSoup


def get_station_id():
    URL = 'https://www.thsrc.com.tw/ArticleContent/a3b630bb-1066-4352-a1ef-58c7b4e8ef7c'
    station_to_id = {}
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.text, 'html5lib')
    for opt in soup.find('select', id='select_location01').find_all('option'):
        if opt['value']:
            station_to_id[opt.text.strip()] = opt['value']
    return station_to_id


def get_times(start_station, end_station, search_date, search_time):
    URL = 'https://www.thsrc.com.tw/TimeTable/Search'
    form_data = {
        'SearchType': 'S',
        'Lang': 'TW',
        'StartStation': station_to_id[start_station],
        'EndStation': station_to_id[end_station],
        'OutWardSearchDate': search_date,
        'OutWardSearchTime': search_time,
        'ReturnSearchDate': search_date,
        'ReturnSearchTime': search_time
    }
    resp = requests.post(URL, data=form_data)
    data = resp.json()
    # 回傳資料也包含其他車次詳細資訊, 此處僅取出其中四項作為範例
    columns = ['TrainNumber', 'DepartureTime', 'DestinationTime', 'Duration']
    times = []
    for d in data['data']['DepartureTable']['TrainItem']:
        times.append([d[c] for c in columns])
    return times


if __name__ == '__main__':
    station_to_id = get_station_id()
    times = get_times('台北', '嘉義', '2020/08/16', '18:30')
    print('車次, 出發時間, 抵達時間, 行車時間')
    for t in times:
        print(t)