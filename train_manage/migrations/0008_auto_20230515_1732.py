# Generated by Django 2.1 on 2023-05-15 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train_manage', '0007_auto_20230515_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='congestion',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='congestion',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='train',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='train',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
