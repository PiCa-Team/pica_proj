from connect.aws_session import AWSSession
from pica import settings

# AWS_INFO
s3 = AWSSession.connector_cl('s3')
bucket_name = settings.AWS_STORAGE_BUCKET_NAME
prefix = settings.AWS_LOCATION


def get_videos_from_s3(bucket_name, prefix):
    videos = []
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    for content in response.get('Contents', []):
        if content['Key'].endswith('.mp4'):
            videos.append(content['Key'])

    return videos


if __name__ == '__main__':
    get_videos_from_s3(bucket_name, prefix)