from connect.aws_session import AWSSession

# AWS_INFO
s3 = AWSSession.connector_cl('s3')
bucket_name = 'pica-team'
prefix = "video"


def get_videos_from_s3():
    videos = []
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    for content in response.get('Contents', []):
        if content['Key'].endswith('.mp4'):
            videos.append(content['Key'])

    return videos
