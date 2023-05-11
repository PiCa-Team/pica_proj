import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pica.settings")

import django

django.setup()

from train_manage import models
from core.db_handler import bulk_insert_data_to_database
from train_manage.seoul_subway_realtime_congestion_info import get_seoul_subway_realtime_congestion
from train_manage.seoul_subway_realtime_location_info import get_seoul_subway_realtime_location


def insert_subway_congestion_data_to_database(model, data):
    bulk_insert_data_to_database(model, data)


if __name__ == '__main__':
    train_live_infos = get_seoul_subway_realtime_location("0", "50", "2호선")
    insert_count = 3
    subway_realtime_congestion_data = get_seoul_subway_realtime_congestion(train_live_infos, insert_count)
    # print(subway_realtime_congestion_data)
    insert_subway_congestion_data_to_database(models.TrainCongestion, subway_realtime_congestion_data)
