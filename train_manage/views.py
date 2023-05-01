from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from config.aws_session import AWSSession
from config.environ import Environ
import random

# Create your views here.
sk = Environ.SK_API_KEY
seoul = Environ.SEOUL_DATA_API_KEY

# AWS_INFO
s3 = AWSSession.connector_cl('s3')
bucket_name = 'pica-team'
prefix = "video"


@login_required
def home(request):
    videos = []
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    for content in response.get('Contents', []):
        if content['Key'].endswith('.mp4'):
            videos.append(content['Key'])

    # random_video = random.choice(videos)
    video_url = f"https://{bucket_name}.s3.{Environ.AWS_REGION}.amazonaws.com/{videos[1]}"
    context = {
        "video_url": video_url,
    }
    return render(request, 'cctv.html', context=context)


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def get_videos_from_s3():
    videos = []
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    for content in response.get('Contents', []):
        if content['Key'].endswith('.mp4'):
            videos.append(content['Key'].replace("video/",""))
    return videos


@login_required
def recorded_videos(request):
    videos = get_videos_from_s3()
    return render(request, 'recorded_videos.html', {'videos': videos})


@login_required
def recorded_videos_detail(request, video_name):
    video_url = f"https://{bucket_name}.s3.{Environ.AWS_REGION}.amazonaws.com/{prefix}/{video_name}"
    return render(request, 'recorded_videos_detail.html', {'video_name': video_name, "video_url": video_url})
