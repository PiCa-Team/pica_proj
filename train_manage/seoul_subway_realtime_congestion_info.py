import os
import requests as req
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pica.settings")

import django

django.setup()

from config.environ import Environ
from train_manage.models import SubwayName, TrainCongestion
from django.db import IntegrityError
from train_manage.seoul_subway_realtime_location_info import get_seoul_subway_realtime_location


def get_seoul_subway_realtime_congestion(train_live_infos):

    train_congestion_list = []
    not_exist_train_congestion_list = []

    for train_live_info in train_live_infos:
        try:
            trainNo = train_live_info['trainNo']
            subwayNm = train_live_info['subwayNm']
            statnNm = train_live_info['statnNm']

            subway_name = SubwayName.objects.get(subway_name=statnNm)

            url = f"https://apis.openapi.sk.com/puzzle/congestion-train/rltm/trains/" \
                  f"{subwayNm.replace('호선','')}/" \
                  f"{trainNo}"

            headers = {"accept": "application/json",
                       "appkey": Environ.SK_API_KEY}

            response = req.get(url, headers=headers)
            json_sk = response.json()
            # print(json_sk)
            confirm_json = json_sk.get('data', None)
            if confirm_json is not None:
                sk_data = response.json()['data']
                train_congestion = TrainCongestion(
                    train_number=sk_data['trainY'],
                    train_status=train_live_info['trainSttus'],
                    train_up_down=train_live_info['updnLine'],
                    train_congestion=sk_data['congestionResult']['congestionTrain'],
                    train_car_congestion=sk_data['congestionResult']['congestionCar'],
                    train_info_delivery_deadline=train_live_info['recptnDt'],
                    subway_name=subway_name
                )
                train_congestion_list.append(train_congestion)
            else:
                not_train_congestion = {
                    'trainNo': train_live_info['trainNo'],
                    'statnNm': train_live_info['statnNm']
                }
                not_exist_train_congestion_list.append(not_train_congestion)

    #
        # SubwayName 객체를 찾지 못했을 때 발생
        except SubwayName.DoesNotExist:
            print(f"SubwayName matching {statnNm} does not exist")
        # requests 라이브러리에서 HTTP 요청을 수행하는 동안 문제가 발생
        except req.exceptions.RequestException as e:
            print(f"An error occurred while making a request: {e}")
        except KeyError:
            print(f"Failed to extract required fields from JSON response")
        # Django ORM에서 데이터베이스 작업을 수행하는 동안 데이터 무결성을 위반하려고 할 때 발생
        except IntegrityError as e:
            print(f"An error occurred while inserting data: {e}")

    return train_congestion_list, not_exist_train_congestion_list


if __name__ == '__main__':
    train_live_infos = get_seoul_subway_realtime_location("0", "50", "2호선")
    get_seoul_subway_realtime_congestion(train_live_infos)
