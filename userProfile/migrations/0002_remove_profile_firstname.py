# Generated by Django 3.1.4 on 2020-12-24 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='firstName',
        ),
    ]