from unittest.mock import patch

from django.test import TestCase
from config.environ import Environ
import requests as req
from train_manage.seoul_subway_realtime_location_info import get_seoul_subway_realtime_location


class GetLiveSeoulTrainCongestionTest(TestCase):

    @patch("train_manage.req")
    def test_train_sttus_zero_exclusion(self, mock_request):
        start_index = 1
        end_index = 50
        subway_line = '2호선'
        mock_request.return_value.json = {
            'realtimePositionList': 1
        }

        url = f"http://swopenAPI.seoul.go.kr/api/subway/{Environ.SEOUL_DATA_API_KEY}/json/realtimePosition/" \
              f"{start_index}/{end_index}/{subway_line}/"
        response = req.get(url)
        json_seoul = response.json()
        train_infos = json_seoul['realtimePositionList']

        result = get_seoul_subway_realtime_location(start_index, end_index, subway_line)

        self.assertEqual(len(result), train_infos[0]['totalCount'],
                            f"현재 {subway_line}의 실시간 열차 정보가 수집 되지 않았습니다.")
