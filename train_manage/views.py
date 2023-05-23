from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .s3_to_db_importer import *
from config.environ import Environ
from core.superset_handler import get_superset_detail_info
from pica import settings
from django.db import transaction, IntegrityError

# Create your views here.
sk = Environ.SK_API_KEY
seoul = Environ.SEOUL_DATA_API_KEY

# AWS_INFO
bucket_name = settings.AWS_STORAGE_BUCKET_NAME
prefix = settings.AWS_VIDEO_PREFIX
detected_prefix = settings.AWS_DETECTED_PREFIX
video_url = f"https://{bucket_name}.s3.{Environ.AWS_REGION}.amazonaws.com"


@login_required
def home(request):
    if request.method == 'POST':
        subway_line = request.POST.get('subway_line')
        station = request.POST.get('station')
        video_info_folder = request.FILES.getlist('folder')
        video_info_folder.sort(key=lambda x: x.name)

        with transaction.atomic():
            try:
                import_cctv_and_polygon_to_s3(video_info_folder)
                print("S3에 CCTV 업로드 완료")
                import_cctv_from_s3_to_db(video_info_folder, subway_line, station)
                print("DB에 CCTV 삽입 작업 완료")
                import_cctv_polygon_from_s3_to_db(video_info_folder)
                print("DB에 POLYGON 삽입 완료")
                print("------------------")
                print("영상 디텍션 시작")
                import_detected_cctv_and_headcount_to_s3(video_info_folder)
                print("S3에 Detected CCTV 업로드 완료")
                import_detected_cctv_from_s3_to_db(video_info_folder)
                print("DB에 Detected CCTV 삽입 완료")
                import_headcount_from_s3_to_db(video_info_folder)
                print("DB에 인원 계수 삽입 완료")
                update_headcount_from_db()
                print("DB density_degree 컬럼 오타 업데이트")
                print("------------------")
                print("CCTV 전체 작업완료")
            except IntegrityError as e:
                error = "An error occurred: ", e
                raise error

        return redirect('home')

    subway_lines = SubwayLine.objects.all().order_by('-id')
    stations = Station.objects.all()
    cctvs = CCTV.objects.all()
    detected_cctvs = DetectedCCTV.objects.all()

    context = {
        "subway_lines": subway_lines,
        "stations": stations,
        "cctvs": cctvs,
        "detected_cctvs": detected_cctvs
    }
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

    return render(request, 'dashboard.html', context)


@login_required
def recorded_videos(request):
    cctvs = CCTV.objects.all().order_by('name')
    context = {
        'cctvs': cctvs,
    }
    return render(request, 'recorded_videos.html', context)


@login_required
def recorded_videos_detail(request, video_name):
    cctv = CCTV.objects.filter(name=video_name).first()
    context = {
        'video_name': video_name,
        'video_url': cctv.video_url
    }
    return render(request, 'recorded_videos_detail.html', context)
