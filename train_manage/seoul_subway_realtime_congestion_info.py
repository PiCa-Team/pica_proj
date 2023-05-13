import os
import requests as req

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pica.settings")

import django

django.setup()

from config.environ import Environ
from train_manage.models import SubwayName, TrainCongestion
from django.db import IntegrityError
from train_manage.seoul_subway_realtime_location_info import get_seoul_subway_realtime_location


def get_seoul_subway_realtime_congestion(train_live_infos, insert_count):

    train_congestion_list = []

    for train_live_info in train_live_infos[:insert_count]:
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

        except SubwayName.DoesNotExist:
            print(f"SubwayName matching {statnNm} does not exist")
        except req.exceptions.RequestException as e:
            print(f"An error occurred while making a request: {e}")
        except KeyError:
            print(f"Failed to extract required fields from JSON response")
        except IntegrityError as e:
            print(f"An error occurred while inserting data: {e}")

#    print(train_congestion_list)
    return train_congestion_list


if __name__ == '__main__':
    train_live_infos = get_seoul_subway_realtime_location("0", "50", "2호선")
    get_seoul_subway_realtime_congestion(train_live_infos, 3)
