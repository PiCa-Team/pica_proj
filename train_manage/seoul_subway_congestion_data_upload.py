import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pica.settings")

import django
django.setup()

from core.db_handler import bulk_insert_data_to_database


def insert_subway_congestion_data_to_database(model, data):
    bulk_insert_data_to_database(model, data)
