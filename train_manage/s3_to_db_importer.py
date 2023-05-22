import json
import pandas as pd
from config.environ import Environ
from core.aws_handler import get_model_from_s3, get_csv_from_s3, get_ploygon_from_s3
from model.pica_file import make_result
from pica import settings
from django.core.files.storage import default_storage
from .models import *
from io import StringIO, BytesIO
from connect.aws_session import AWSSession
from ultralytics import YOLO
import os
import subprocess

s3 = AWSSession.connector_cl('s3')
bucket_name = settings.AWS_STORAGE_BUCKET_NAME
prefix = settings.AWS_VIDEO_PREFIX
polygon_prefix = settings.AWS_POLYGON_PREFIX
insert_db = CCTV
model_prefix = settings.AWS_MODEL_PREFIX
headcount_prefix = settings.AWS_HAED_COUNT_PREFIX
detected_prefix = settings.AWS_DETECTED_PREFIX
csv_prefix = settings.AWS_HAED_COUNT_PREFIX
video_url = f"https://{bucket_name}.s3.{Environ.AWS_REGION}.amazonaws.com/"


def import_cctv_and_polygon_to_s3(video_info_folder: list):
    for video_info in video_info_folder:
        if '.mp4' in str(video_info):
            file_name = f'{prefix}/{video_info.name}'
            default_storage.save(file_name, video_info)
        elif '.txt' in str(video_info):
            file_name = video_info.name
            s3_key = f"{polygon_prefix}/{file_name}"
            s3.upload_fileobj(video_info, bucket_name, s3_key)


def import_cctv_from_s3_to_db(video_info_folder: list, subway_line, station):
    select_subway_line = SubwayLine.objects.filter(name=subway_line).first()
    select_station = Station.objects.filter(name=station).first()

    for video_info in video_info_folder:
        if '.mp4' in str(video_info):
            s3_video_url = video_url + f"{prefix}/" + f"{video_info.name}"
            new_cctv = CCTV(name=video_info.name,
                            video_url=s3_video_url,
                            subway_line_id=select_subway_line.id,
                            station_id=select_station.id)
            new_cctv.save()


def import_cctv_polygon_from_s3_to_db(video_info_folder):
    for video_info in video_info_folder:
        if '.mp4' in str(video_info):
            cctv = CCTV.objects.filter(name=video_info.name).first()
            polygon = get_ploygon_from_s3(bucket_name=bucket_name,
                                          polygon_prefix=polygon_prefix,
                                          video_name=video_info.name.replace(".mp4", ".txt"))
            polygon = json.loads(polygon)
            new_polygon = Polygon(polygon=polygon['polygon'],
                                  line_start=polygon['LINE_START'],
                                  line_end=polygon['LINE_END'],
                                  cctv_id=cctv.id)
            new_polygon.save()


def import_detected_cctv_and_headcount_to_s3(video_info_folder: list):
    for video_info in video_info_folder:
        if '.mp4' in str(video_info):
            try:
                cctv = CCTV.objects.get(name=video_info.name)
            except CCTV.DoesNotExist as e:
                error = "An error occurred: ", e
                raise error

            polygon = Polygon.objects.get(cctv_id=cctv.id)

            POLYGON = [int(i.replace('[', '').replace(']', '').strip()) for i in polygon.polygon[1:-1].split(',')]
            POLYGON = [list(map(int, POLYGON[i:i + 2])) for i in range(0, len(POLYGON), 2)]
            TEST_VIDEO_PATH = cctv.video_url
            CLASS_ID = [0]
            LINE_START = [int(i.replace('[', '').replace(']', '')) for i in polygon.line_start.split(',')]
            LINE_END = [int(i.replace('[', '').replace(']', '')) for i in polygon.line_end.split(',')]
            MODEL = YOLO(get_model_from_s3(bucket_name, model_prefix))

            headcount_df = make_result(POLYGON, TEST_VIDEO_PATH, CLASS_ID,
                                       LINE_START, LINE_END, MODEL, video_info.name)

            headcount_df.rename(columns={
                "IN": "in_train",
                "OUT": "out_train",
                "MAX COUNT": "max_count",
                "DENSITY": "density",
                "DENSITY_DEGREE": "density_degree"
            }, inplace=True)

            # 비디오 저장
            try:
                target_path = '/Users/seok/Documents/tool_collection/pica_proj/model/'
                input_data = os.path.join(target_path, video_info.name)
                output_data = os.path.join(target_path, 'temp_' + video_info.name)
                # ffmpeg로 비디오 인코딩 문제 해결
                command = ['ffmpeg', '-i', input_data, '-vcodec', 'libx264', '-f', 'mp4', '-y', output_data]
                subprocess.run(command, check=True)

                s3.upload_file(
                    Filename=output_data,
                    Bucket=bucket_name,
                    Key=f'{detected_prefix}/{video_info.name}',
                    ExtraArgs={'ContentType': "video/mp4", 'ACL': "public-read", 'ContentDisposition': "inline"}
                )

                os.remove(os.path.join(target_path, video_info.name))
                os.remove(os.path.join(target_path, 'temp_' + video_info.name))
                print("#####주의 사항#####")
                print(f"로컬에 있는 디텍션 {video_info.name} 삭제 완료")
                print("#####주의 사항#####")

            except Exception as e:
                print(f"File upload failed: {e}")

            # headcount 파일 저장
            csv_buffer = StringIO()
            headcount_df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            # convert string data to bytes
            csv_buffer_bytes = BytesIO(csv_buffer.getvalue().encode())
            file_name = video_info.name.replace('.mp4', '.csv')
            s3_key = f"{headcount_prefix}/{file_name}"
            s3.upload_fileobj(csv_buffer_bytes, bucket_name, s3_key)


def import_detected_cctv_from_s3_to_db(video_info_folder: list):
    for video_info in video_info_folder:
        if '.mp4' in str(video_info):
            cctv = CCTV.objects.filter(name=video_info.name).first()
            s3_video_url = video_url + f"{detected_prefix}/" + f"{video_info.name}"
            new_detected_cctv = DetectedCCTV(name=video_info.name,
                                             video_url=s3_video_url,
                                             cctv_id=cctv.id)
            new_detected_cctv.save()


def import_headcount_from_s3_to_db(video_info_folder):
    for video_info in video_info_folder:
        if '.mp4' in str(video_info):
            detected_cctv = DetectedCCTV.objects.filter(name=video_info.name).first()
            video_headcount = get_csv_from_s3(bucket_name=bucket_name,
                                              csv_prefix=csv_prefix,
                                              video_name=video_info.name.replace(".mp4", ".csv"))
            video_headcount_df = pd.read_csv(StringIO(video_headcount))
            video_headcount_df['density_degree'] = \
                video_headcount_df['density_degree'].str.replace("0    ", "") \
                    .str.replace(" Name: density_degree, dtype: object", "")
            new_headcount = HeadCount(
                in_train=int(video_headcount_df['in_train']),
                out_train=int(video_headcount_df['out_train']),
                max_count=int(video_headcount_df['max_count']),
                density=float(video_headcount_df['density']),
                density_degree=str(video_headcount_df['density_degree']),
                detected_cctv_id=detected_cctv.id
            )

            new_headcount.save()
