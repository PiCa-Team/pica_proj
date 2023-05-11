import requests as req
from config.environ import Environ
from train_manage.live_seoul_train_info import get_live_seoul_train_congestion


def get_live_sk_train_congestion(train_live_infos):

    result = []

    for train_live_info in train_live_infos[:3]:
        trainNo = train_live_info['trainNo']
        subwayNm = train_live_info['subwayNm']
        url = f"https://apis.openapi.sk.com/puzzle/congestion-train/rltm/trains/" \
              f"{subwayNm.replace('호선','')}/" \
              f"{trainNo}"

        headers = {"accept": "application/json",
                   "appkey": Environ.SK_API_KEY}

        response = req.get(url, headers=headers)
        json_sk = response.json()
        confirm_json = json_sk.get('data', None)
        if confirm_json is not None:
            sk_data = response.json()['data']
            data = {
                'train_number': sk_data['trainY'],
                'train_status': train_live_info['trainSttus'],
                'train_up_down': train_live_info['updnLine'],
                'train_congestion': sk_data['congestionResult']['congestionTrain'],
                'train_car_congestion': sk_data['congestionResult']['congestionCar'],
                'train_info_delivery_deadline.': train_live_info['recptnDt'],
                'statnNm': train_live_info['statnNm']
            }
            result.append(data)

    print(result, len(result))
    return result


if __name__ == '__main__':
    train_live_infos = get_live_seoul_train_congestion("0", "50", "2호선")
    get_live_sk_train_congestion(train_live_infos)
