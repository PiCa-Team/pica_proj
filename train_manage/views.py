from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .s3_to_db_importer import *
from config.environ import Environ
from core.aws_handler import get_videos_from_s3
from core.superset_handler import get_superset_detail_info
from pica import settings

# Create your views here.
sk = Environ.SK_API_KEY
seoul = Environ.SEOUL_DATA_API_KEY

# AWS_INFO
bucket_name = settings.AWS_STORAGE_BUCKET_NAME
prefix = settings.AWS_LOCATION
sub_prefix_1 = settings.AWS_SUB_PREFIX_1
video_url = f"https://{bucket_name}.s3.{Environ.AWS_REGION}.amazonaws.com/{prefix}/"


@login_required
def home(request):
    if request.method == 'POST':
        subway_line = request.POST.get('subway_line')
        station = request.POST.get('station')
        video_list = request.FILES.getlist('videos')

        import_original_video_to_s3(video_list)
        import_original_video_from_s3_to_db(video_list, subway_line, station)

        return redirect('home')

    subway_lines = SubwayLine.objects.all().order_by('-id')
    stations = Station.objects.all()
    s3_original_videos = get_videos_from_s3(bucket_name, prefix)
    s3_detected_videos = get_videos_from_s3(bucket_name, sub_prefix_1)
    original_video_urls = [video_url + original_video.replace("video/","") for original_video in s3_original_videos]
    detected_video_urls = [video_url + detected_video.replace("video/","") for detected_video in s3_detected_videos]

    context = {
        "subway_lines": subway_lines,
        "stations": stations,
        "original_video_urls": original_video_urls,
        "detected_video_urls": detected_video_urls
    }
    print(context)
    return render(request, 'cctv.html', context)


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

    # print(context)

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
    s3_video_url = video_url + f"{video_name}"
    context = {
        'video_name': video_name,
        'video_url': s3_video_url
    }

    return render(request, 'recorded_videos_detail.html', context)
