from connect.superset_token import get_superset_auth_token
import requests
from pica import settings


def get_superset_dashboards():
    access_token = get_superset_auth_token()
    if not access_token:
        return []

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    superset_dashboards_url = f"{settings.SUPERSET_URL}/api/v1/dashboard/"
    response = requests.get(superset_dashboards_url, headers=headers)

    if response.status_code != 200:
        return []

    dashboards = response.json()["result"]
    return dashboards


def get_superset_detail_info():
    dashboard_detail = []
    dashboards = get_superset_dashboards()
    for dashboard in dashboards:
        data = {
            'dashboard_id': dashboard['id'],
            'dashboard_title': dashboard['dashboard_title'],
            'dashboard_url': dashboard['url'],
            'dashboard_changed': dashboard['changed_on_delta_humanized']
        }
        dashboard_detail.append(data)
    return dashboard_detail


if __name__ == '__main__':
    a = get_superset_detail_info()
    print(a)
