# Generated by Django 2.1 on 2023-05-06 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubwayLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subway_line', models.CharField(max_length=10)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'pica_subwayline',
            },
        ),
        migrations.CreateModel(
            name='SubwayName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subway_name', models.CharField(max_length=10)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('subway_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train_manage.SubwayLine')),
            ],
            options={
                'db_table': 'pica_subwayname',
            },
        ),
        migrations.CreateModel(
            name='TrainCongestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_number', models.CharField(max_length=10)),
                ('train_status', models.CharField(max_length=10)),
                ('train_up_down', models.CharField(max_length=10)),
                ('train_congestion', models.CharField(max_length=10)),
                ('train_car_congestion', models.CharField(max_length=30)),
                ('subway_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train_manage.SubwayName')),
            ],
            options={
                'db_table': 'pica_train_congestion',
            },
        ),
    ]