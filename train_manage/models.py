from django.db import models


class SubwayLine(models.Model):
    subway_line = models.CharField(max_length=10)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'pica_subwayline'

    def __str__(self):
        return f"{self.subway_line}"


class SubwayName(models.Model):
    subway_name = models.CharField(max_length=10)
    subway_line = models.ForeignKey(SubwayLine, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'pica_subwayname'

    def __str__(self):
        return f"{self.subway_line} - {self.subway_name}"


class TrainCongestion(models.Model):
    train_number = models.CharField(max_length=10)
    train_status = models.CharField(max_length=10)
    train_up_down = models.CharField(max_length=10)
    train_congestion = models.IntegerField()
    train_car_congestion = models.CharField(max_length=100)
    train_info_delivery_deadline = models.CharField(max_length=50)
    subway_name = models.ForeignKey(SubwayName, on_delete=models.CASCADE, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pica_train_congestion'

    def __str__(self):
        return f"{self.train_number} - {self.subway_name}"
