# Generated by Django 3.1.7 on 2021-06-13 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testresult',
            name='schema_name',
        ),
    ]
