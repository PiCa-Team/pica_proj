# Generated by Django 2.1 on 2023-05-15 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('train_manage', '0004_auto_20230515_1656'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='train',
            unique_together={('number', 'status', 'direction', 'station')},
        ),
    ]