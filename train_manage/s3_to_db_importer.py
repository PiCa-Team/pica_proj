from config.environ import Environ
from pica import settings
from django.core.files.storage import default_storage
from .models import *

bucket_name = settings.AWS_STORAGE_BUCKET_NAME
prefix = settings.AWS_LOCATION
insert_db = OriginalCCTV
video_url = f"https://{bucket_name}.s3.{Environ.AWS_REGION}.amazonaws.com/{prefix}/"


def import_original_video_to_s3(video_list: list):
    for video in video_list:
        default_storage.save(video.name, video)


def import_original_video_from_s3_to_db(video_list: list, subway_line, station):
    select_subway_line = SubwayLine.objects.filter(name=subway_line).first()
    select_station = Station.objects.filter(name=station).first()

    for video in video_list:
        s3_video_url = video_url + f"{video.name}"
        new_cctv = OriginalCCTV(video_url=s3_video_url,
                                subway_line_id=select_subway_line.id,
                                station_id=select_station.id)
        new_cctv.save()


def import_detected_video_from_s3(video_list: list):
    for video in video_list:
        default_storage.save(video.name, video)
        s3_video_url = video_url + f"{video.name}"
        OriginalCCTV(video_url=s3_video_url)
        video.save()
