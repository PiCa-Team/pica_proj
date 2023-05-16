from django.db import models


class SubwayLine(models.Model):
    name = models.CharField(max_length=10, db_index=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'pica_subway_line'

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=10, db_index=True)
    subway_line = models.ForeignKey(SubwayLine, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'pica_station'

    def __str__(self):
        return f"{self.subway_line} - {self.name}"


class Train(models.Model):
    number = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    direction = models.CharField(max_length=10)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'pica_train'
        indexes = [
            models.Index(fields=['status', 'direction', 'station'])
        ]
        unique_together = (('number', 'status', 'direction', 'station'),)

    def __str__(self):
        return f"{self.number} - {self.station}"


class Congestion(models.Model):
    congestion = models.IntegerField()
    car_congestion = models.CharField(max_length=100)
    info_delivery_deadline = models.DateTimeField()
    train = models.ForeignKey(Train, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'pica_congestion'

    def __str__(self):
        return f"{self.train.number} - {self.car_congestion} - {self.train.station.name}"