from django.test import TestCase

from config.environ import Environ
from train_manage.get_live_seoul_train_info import get_live_seoul_train_congestion
import requests as req


class GetLiveSeoulTrainCongestionTest(TestCase):
    def test_train_sttus_zero_exclusion(self):
        start_index = 1
        end_index = 50
        subway_line = '2호선'

        url = f"http://swopenAPI.seoul.go.kr/api/subway/{Environ.SEOUL_DATA_API_KEY}/json/realtimePosition/" \
              f"{start_index}/{end_index}/{subway_line}/"
        response = req.get(url)
        json_seoul = response.json()
        train_infos = json_seoul['realtimePositionList']

        result = get_live_seoul_train_congestion(start_index, end_index, subway_line)

        self.assertEqual(len(result), train_infos[0]['totalCount'],
                            f"현재 {subway_line}의 실시간 열차 정보가 수집 되지 않았습니다.")
