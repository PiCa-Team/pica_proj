import os
from datetime import datetime

import requests as req

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pica.settings")

import django

django.setup()

from config.environ import Environ
from train_manage.models import Station, Train, Congestion
from train_manage.seoul_subway_realtime_location_info import get_seoul_subway_realtime_location
from core.db_handler import bulk_insert_data_to_database


def get_train_data(train_live_infos):
    no_data_train_list = []

    try:
        for train_live_info in train_live_infos:
            trainNo = train_live_info['trainNo']
            subwayNm = train_live_info['subwayNm']
            statnNm = train_live_info['statnNm']

            subway_name, created = Station.objects.get_or_create(name=statnNm)

            url = f"https://apis.openapi.sk.com/puzzle/congestion-train/rltm/trains/" \
                  f"{subwayNm.replace('호선', '')}/" \
                  f"{trainNo}"

            headers = {"accept": "application/json",
                       "appkey": Environ.SK_API_KEY}

            response = req.get(url, headers=headers)
            json_sk = response.json()
            confirm_json = json_sk.get('data', None)

            if confirm_json is None:
                data = {
                    "number": trainNo,
                    "station": statnNm
                }
                no_data_train_list.append(data)
            else:
                yield confirm_json, subway_name, train_live_info

        print(f"SK에 없는 {subwayNm} 열차번호 수: "
              f"{len(no_data_train_list)}")
        print(f"SK에 없는 {subwayNm} 열차번호와 역: "
              f"{no_data_train_list}")
        print("-----------------------------------------------------------")
    except Exception as e:
        print(f"{datetime.now().strftime('%Y-%m-%d')} Error: {e}")
        raise e


def get_and_save_train_congestion(train_live_infos):
    try:
        new_congestion_list = []
        new_station_list = []

        for confirm_json, subway_name, train_live_info in get_train_data(train_live_infos):
            sk_data = confirm_json

            existing_train, created = Train.objects.get_or_create(
                number=sk_data['trainY'],
                status=train_live_info['trainSttus'],
                direction=train_live_info['updnLine'],
                station_id=subway_name.id,
                defaults={'status': train_live_info['trainSttus'], 'direction': train_live_info['updnLine']}
            )
            if created:
                new_station = {
                    "number": sk_data['trainY'],
                    "status": train_live_info['trainSttus'],
                    "direction": train_live_info['updnLine']
                }
                new_station_list.append(new_station)

            new_congestion = Congestion(
                congestion=sk_data['congestionResult']['congestionTrain'],
                car_congestion=sk_data['congestionResult']['congestionCar'],
                info_delivery_deadline=train_live_info['recptnDt'],
                train_id=existing_train.id
            )

            new_congestion_list.append(new_congestion)

        bulk_insert_data_to_database(Congestion, new_congestion_list)

        print(f"{new_station_list}이 새로 추가되었습니다.")
        print("-----------------------------------------------------------")
        print(f"SK에 있는 열차번호 수: "
              f"{len(new_congestion_list)}")
        print(f"SK에 있는 열차번호와 역: "
              f"{new_congestion_list}")
        print("-----------------------------------------------------------")

    except Exception as e:
        print(f"{datetime.now().strftime('%Y-%m-%d')} 저장에 실패했습니다: {e}")
        raise e


if __name__ == '__main__':
    train_live_infos = get_seoul_subway_realtime_location("0", "50", "2호선")
    get_and_save_train_congestion(train_live_infos)
