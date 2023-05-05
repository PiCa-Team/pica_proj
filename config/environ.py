import os
from dotenv import load_dotenv

load_dotenv()


class Environ:

    # 장고 시크릿 키
    SECRET_KEY = os.environ.get('SECRET_KEY')

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
    SUPERSET_URL = os.environ.get("SUPERSET_URL")

    # SSH 터널링 정보
    SSH_TUNNEL_USERNAME = os.environ.get('SSH_TUNNEL_USERNAME')
    SSH_TUNNEL_PKEY = os.environ.get('SSH_TUNNEL_PKEY')
    SSH_TUNNEL_HOST = os.environ.get('SSH_TUNNEL_HOST')
    SSH_TUNNEL_PORT = int(os.environ.get('SSH_TUNNEL_PORT', 22))

    # RDS 정보
    RDS_USERNAME = os.environ.get('RDS_USERNAME')
    RDS_PASSWORD = os.environ.get('RDS_PASSWORD')
    RDS_HOST = os.environ.get('RDS_HOST')
    RDS_PORT = int(os.environ.get('RDS_PORT', 3306))
    RDS_DB_NAME = os.environ.get('RDS_DB_NAME')

