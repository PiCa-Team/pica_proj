import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pica.settings")

import django
django.setup()

from train_manage.seoul_subway_congestion_data_upload import insert_subway_congestion_data_to_database
from train_manage.seoul_subway_realtime_congestion_info import get_seoul_subway_realtime_congestion
from train_manage.seoul_subway_realtime_location_info import get_seoul_subway_realtime_location
from train_manage import models
from datetime import datetime


def cron_job():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'현재시간: {current_time}')
    try:
        subway_line = "2호선"
        train_live_infos = get_seoul_subway_realtime_location("0", "50", subway_line)
        print(f"실시간 {subway_line} 지하철 수: "
              f"{len(train_live_infos)}")
        subway_realtime_congestion_data, not_data = get_seoul_subway_realtime_congestion(train_live_infos)
        print(f"SK에 있는 {subway_line} 열차번호 수: "
              f"{len(subway_realtime_congestion_data)}")
        print(f"SK에 없는 {subway_line} 열차번호 수: "
              f"{len(not_data)}")
        print(f"실시간 {subway_line} 지하철 수 확인: "
              f"{len(train_live_infos)==(len(subway_realtime_congestion_data)+len(not_data))}")
        insert_subway_congestion_data_to_database(models.TrainCongestion, subway_realtime_congestion_data)
        print(f"작업을 성공적으로 완료했습니다.: \n {subway_realtime_congestion_data}\n")
        print()
        print(f"SK에 없는 열차번호 입니다.: \n {not_data}")
    except Exception as e:
        print(f'작업을 실패하였습니다. 에러문을 확인하세요.: {e}\n')


def crontab_every_minute():
    print('hello crontab')


if __name__ == '__main__':
    cron_job()
