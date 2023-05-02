import os
from dotenv import load_dotenv

load_dotenv()


class Environ:

    # 장고 시크릿 키
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # rootDB
    DB_HOST = os.environ.get('DB_HOST')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_NAME = os.environ.get('DB_NAME')
    DB_PORT = os.environ.get('DB_PORT')

    # SK-api 키
    SK_API_KEY = os.environ.get("SK_API_KEY")

    # Seoul-data-api 키
    SEOUL_DATA_API_KEY = os.environ.get("SEOUL_DATA_API_KEY")

    # AWS 키
    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.environ.get("AWS_REGION")

    # Superset 정보
    SUPERSET_USERNAME = os.environ.get("SUPERSET_USERNAME")
    SUPERSET_PASSWORD = os.environ.get("SUPERSET_PASSWORD")

