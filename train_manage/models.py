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
    congestion = models.IntegerField(default=0)
    no1 = models.IntegerField(default=0)
    no2 = models.IntegerField(default=0)
    no3 = models.IntegerField(default=0)
    no4 = models.IntegerField(default=0)
    no5 = models.IntegerField(default=0)
    no6 = models.IntegerField(default=0)
    no7 = models.IntegerField(default=0)
    no8 = models.IntegerField(default=0)
    no9 = models.IntegerField(default=0)
    no10 = models.IntegerField(default=0)
    info_delivery_deadline = models.DateTimeField()
    train = models.ForeignKey(Train, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'pica_congestion'

    def __str__(self):
        return f"{self.train.number} - {self.congestion} - {self.train.station.name}"


class CCTV(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    video_url = models.CharField(max_length=255, unique=True)
    subway_line = models.ForeignKey(SubwayLine, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pica_cctv'
        indexes = [
            models.Index(fields=['name', 'video_url'])
        ]

    def __str__(self):
        return f"{self.subway_line.name} - {self.station.name} " \
               f"- {self.name} - {self.created_at.now()}"


class Polygon(models.Model):
    polygon = models.CharField(max_length=100)
    line_start = models.CharField(max_length=50)
    line_end = models.CharField(max_length=50)
    cctv = models.OneToOneField(CCTV, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'pica_polygon'

    def __str__(self):
        return f"{self.cctv.video_url} - {self.polygon} - {self.line_start} " \
               f"- {self.line_start} - {self.created_at}"


class DetectedCCTV(models.Model):
    name = models.CharField(max_length=255, unique=True)
    video_url = models.CharField(max_length=255, unique=True)
    cctv = models.OneToOneField(CCTV, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pica_detected_cctv'
        indexes = [
            models.Index(fields=['name', 'video_url'])
        ]

    def __str__(self):
        return f"{self.cctv.subway_line.name} - {self.cctv.station.name} " \
               f"- {self.name} - {self.created_at}"


class HeadCount(models.Model):
    in_train = models.IntegerField()
    out_train = models.IntegerField()
    max_count = models.IntegerField()
    density = models.FloatField()
    density_degree = models.CharField(max_length=255)
    detected_cctv = models.OneToOneField(DetectedCCTV, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'pica_headcount'
        indexes = [
            models.Index(fields=['density_degree', 'detected_cctv'])
        ]

    def __str__(self):
        return f"{self.detected_cctv.cctv.subway_line.name} - {self.detected_cctv.cctv.station.name} " \
               f"- {self.detected_cctv.cctv.name} - {self.created_at}"
