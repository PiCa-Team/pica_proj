from django.contrib import admin

from train_manage.models import SubwayLine, Station, Train, Congestion

# Register your models here.

admin.site.register(SubwayLine)
admin.site.register(Station)
admin.site.register(Train)
admin.site.register(Congestion)
