from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from connect.aws_session import AWSSession
from config.environ import Environ
from core.aws_handler import get_videos_from_s3
from core.superset_handler import get_superset_detail_info
from pica import settings

# Create your views here.
sk = Environ.SK_API_KEY
seoul = Environ.SEOUL_DATA_API_KEY

# AWS_INFO
s3 = AWSSession.connector_cl('s3')
bucket_name = 'pica-team'
prefix = "video"


@login_required
def home(request):
    videos = get_videos_from_s3()
    print(videos)
    video_url = f"https://{bucket_name}.s3.{Environ.AWS_REGION}.amazonaws.com/{videos[1]}"
    context = {
        "video_url": video_url,
    }
    return render(request, 'cctv.html', context=context)


def dashboard(request):
    superset_dashboards = get_superset_detail_info()

    superset_dashboards.reverse()
    superset_dashboard_url = None
    selected_dashboard_id = None

    if request.method == 'POST':
        selected_dashboard_id = request.POST.get('selected_dashboard_id', '')
        for dashboard in superset_dashboards:
            if dashboard["dashboard_id"] == int(selected_dashboard_id):
                superset_dashboard_url = dashboard['dashboard_url']
                selected_dashboard_id = dashboard['dashboard_id']
                break

    if request.method == 'GET':
        if superset_dashboards:
            superset_dashboard_url = superset_dashboards[0]['dashboard_url']
            selected_dashboard_id = superset_dashboards[0]['dashboard_id']

    if superset_dashboard_url is not None:
        superset_dashboard_url = f'{settings.SUPERSET_URL}{superset_dashboard_url}?standalone=true'
    else:
        superset_dashboard_url = None

    context = {
        'superset_dashboards': superset_dashboards,
        'superset_dashboard_url': superset_dashboard_url,
        'selected_dashboard_id': selected_dashboard_id
    }

    print(context)

    return render(request, 'dashboard.html', context)


@login_required
def recorded_videos(request):
    videos = get_videos_from_s3()
    video_names = [video.replace("video/", "") for video in videos]
    context = {
        'video_names': video_names,
    }

    return render(request, 'recorded_videos.html', context)


@login_required
def recorded_videos_detail(request, video_name):
    video_url = f"https://{bucket_name}.s3.{Environ.AWS_REGION}.amazonaws.com/{prefix}/{video_name}"
    context = {
        'video_name': video_name,
        'video_url': video_url
    }

    return render(request, 'recorded_videos_detail.html', context)
