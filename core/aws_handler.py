from config.environ import Environ
from connect.aws_session import AWSSession
from pica import settings

# AWS_INFO
s3 = AWSSession.connector_cl('s3')
bucket_name = settings.AWS_STORAGE_BUCKET_NAME
prefix = settings.AWS_VIDEO_PREFIX
model_prefix = settings.AWS_MODEL_PREFIX
csv_prefix = settings.AWS_HAED_COUNT_PREFIX
polygon_prefix = settings.AWS_POLYGON_PREFIX
s3_url = f"https://{bucket_name}.s3.{Environ.AWS_REGION}.amazonaws.com/"


def get_videos_from_s3(bucket_name, prefix):
    videos = []
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    for content in response.get('Contents', []):
        if content['Key'].endswith('.mp4'):
            videos.append(content['Key'])

    return videos


def get_model_from_s3(bucket_name, model_prefix):
    model_url = None
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=model_prefix)
    for content in response.get('Contents'):
        if content['Key'].endswith('.pt'):
            model_url = s3_url + f"{content['Key']}"

    return model_url


def get_csv_from_s3(bucket_name, csv_prefix, video_name):
    key = f'{csv_prefix}/' + video_name
    response = s3.get_object(Bucket=bucket_name, Key=key)
    data = response['Body'].read().decode('utf-8')
    return data


def get_ploygon_from_s3(bucket_name, polygon_prefix, video_name):
    key = f'{polygon_prefix}/' + video_name
    response = s3.get_object(Bucket=bucket_name, Key=key)
    data = response['Body'].read().decode('utf-8')
    return data


if __name__ == '__main__':
    df = get_ploygon_from_s3(bucket_name, polygon_prefix, 'test1.txt')
