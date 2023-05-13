import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pica.settings")

import django

django.setup()

from train_manage.seoul_subway_congestion_data_upload import insert_subway_congestion_data_to_database
from train_manage.seoul_subway_realtime_congestion_info import get_seoul_subway_realtime_congestion
from train_manage.seoul_subway_realtime_location_info import get_seoul_subway_realtime_location
from train_manage import models


def cron_job():
    try:
        train_live_infos = get_seoul_subway_realtime_location("0", "50", "2호선")
        insert_count = 3
        subway_realtime_congestion_data = get_seoul_subway_realtime_congestion(train_live_infos, insert_count)
        insert_subway_congestion_data_to_database(models.TrainCongestion, subway_realtime_congestion_data)
        print(f'작업이 성공적으로 완료되었습니다: \n {subway_realtime_congestion_data}\n')
    except Exception as e:
        print(f'작업 중 에러가 발생했습니다: {e}\n')


def crontab_every_minute():
    print('hello crontab')


if __name__ == '__main__':
    cron_job()
