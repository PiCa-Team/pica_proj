import os
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pica.settings")

import django

django.setup()

from django.db import transaction, IntegrityError


def read_and_insert_csv_file(path, model):
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print("An error occurred while reading the CSV file: ", e)
        return

    df_list = [model(**row) for index, row in df.iterrows()]
    try:
        with transaction.atomic():
            model.objects.bulk_create(df_list)
        print("Successfully inserted data.")
    except IntegrityError as e:
        print("An error occurred: ", e)


def bulk_insert_data_to_database(model, data: list):
    try:
        with transaction.atomic():
            model.objects.bulk_create(data)
        print("Successfully inserted data.")
    except IntegrityError as e:
        print("An error occurred: ", e)


if __name__ == '__main__':
    pass

