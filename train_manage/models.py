from django.db import models
from django.utils import timezone


class SubwayLine(models.Model):
    subway_line = models.CharField(max_length=10)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'pica_subwayline'


class SubwayName(models.Model):
    subway_name = models.CharField(max_length=10)
    subway_line = models.ForeignKey(SubwayLine, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'pica_subwayname'


class TrainCongestion(models.Model):
    train_number = models.CharField(max_length=10)
    train_status = models.CharField(max_length=10)
    train_up_down = models.CharField(max_length=10)
    train_congestion = models.IntegerField()
    train_car_congestion = models.CharField(max_length=30)
    train_info_delivery_deadline = models.DateTimeField(default=timezone.now)
    subway_name = models.OneToOneField(SubwayName, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pica_train_congestion'
