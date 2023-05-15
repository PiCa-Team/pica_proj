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
    number = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=10)
    direction = models.CharField(max_length=10)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pica_train'
        indexes = [
            models.Index(fields=['status', 'direction', 'station'])
        ]
        unique_together = (('number', 'status', 'direction'),)

    def __str__(self):
        return f"{self.number} - {self.station}"

    def created_at_without_microseconds(self):
        return self.created_at.replace(microsecond=0)

    def updated_at_without_microseconds(self):
        return self.updated_at.replace(microsecond=0)


class Congestion(models.Model):
    congestion = models.IntegerField()
    car_congestion = models.CharField(max_length=100)
    info_delivery_deadline = models.CharField(max_length=50)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pica_congestion'

    def __str__(self):
        return f"{self.train.number} - {self.car_congestion} - {self.train.station.name}"

    def created_at_without_microseconds(self):
        return self.created_at.replace(microsecond=0)

    def updated_at_without_microseconds(self):
        return self.updated_at.replace(microsecond=0)
