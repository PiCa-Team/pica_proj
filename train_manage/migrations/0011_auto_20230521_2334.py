# Generated by Django 2.1 on 2023-05-21 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train_manage', '0010_auto_20230521_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headcount',
            name='density_degree',
            field=models.CharField(max_length=255),
        ),
    ]
