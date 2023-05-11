import requests as req
from config.environ import Environ


def get_seoul_subway_realtime_location(start_index, end_index, subway_line):
    url = f"http://swopenAPI.seoul.go.kr/api/subway/{Environ.SEOUL_DATA_API_KEY}/json/realtimePosition/" \
          f"{start_index}/{end_index}/{subway_line}/"

    response = req.get(url)
    json_seoul = response.json()
    train_infos = json_seoul['realtimePositionList']

    result = []
    # print(train_infos)
    for train_info in train_infos:
        if train_info['updnLine'] == '0':
            train_info['updnLine'] = '상행/내선'
        else:
            train_info['updnLine'] = '하행/외선'

        if train_info['trainSttus'] == '1':
            train_info['trainSttus'] = '도착'
        elif train_info['trainSttus'] == '2':
            train_info['trainSttus'] = '출발'
        elif train_info['trainSttus'] == '3':
            train_info['trainSttus'] = '전역 출발'
        else:
            train_info['trainSttus'] = '진입'

        data = {
            "trainNo": train_info["trainNo"],
            "statnNm": train_info["statnNm"],
            "trainSttus": train_info['trainSttus'],
            "updnLine": train_info['updnLine'],
            "recptnDt": train_info['recptnDt'],
            "subwayNm": train_info['subwayNm']
        }

        result.append(data)

    # print(result)
    return result


if __name__ == '__main__':
    get_seoul_subway_realtime_location("0", '50', "2호선")
