# Generated by Django 2.1 on 2023-05-15 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train_manage', '0002_auto_20230514_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='train',
            name='number',
            field=models.CharField(max_length=10),
        ),
    ]
