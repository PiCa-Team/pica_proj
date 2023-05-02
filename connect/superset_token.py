import requests
from pica import settings


def get_superset_auth_token():
    url = f"{settings.SUPERSET_URL}/api/v1/security/login"
    data = {
        "username": settings.SUPERSET_USERNAME,
        "password": settings.SUPERSET_PASSWORD,
        "provider": "db",
        "refresh": True
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return Exception("Error getting Superset token")