from django.contrib import admin

from train_manage.models import *

# Register your models here.

admin.register(SubwayLine)
admin.register(Station)
admin.register(Train)
admin.register(Congestion)
