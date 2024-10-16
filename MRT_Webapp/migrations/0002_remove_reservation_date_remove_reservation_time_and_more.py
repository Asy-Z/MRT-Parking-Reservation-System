# Generated by Django 5.0 on 2024-10-13 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MRT_Webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='Date',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='Time',
        ),
        migrations.AddField(
            model_name='reservation',
            name='DateTimeEnd',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='DateTimeStart',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]