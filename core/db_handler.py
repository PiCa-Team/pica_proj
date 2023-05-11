import os
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pica.settings")

import django

django.setup()

from train_manage.models import SubwayName


def read_and_insert_csv_file(path, model):
    df = pd.read_csv(path)
    df_list = [model(**row) for index, row in df.iterrows()]
    model.objects.bulk_create(df_list)

    return df_list


if __name__ == '__main__':
    csv_file_path = '/Users/seok/Desktop/pica/국가철도공단_수도권2호선.csv'
    read_and_insert_csv_file(csv_file_path, SubwayName)
