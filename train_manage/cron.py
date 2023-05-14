import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pica.settings")

import django

django.setup()

from train_manage.seoul_subway_realtime_congestion_info import get_and_save_train_congestion
from train_manage.seoul_subway_realtime_location_info import get_seoul_subway_realtime_location
from datetime import datetime


def cron_job():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'현재시간: {current_time}')
    print("-----------------------------------------------------------")
    try:
        subway_line = "2호선"
        train_live_infos = get_seoul_subway_realtime_location("0", "50", subway_line)
        get_and_save_train_congestion(train_live_infos)

        print(f"작업을 성공적으로 완료했습니다.:")
    except Exception as e:
        print(f'작업을 실패하였습니다. 에러문을 확인하세요.: {e}\n')


if __name__ == '__main__':
    cron_job()
