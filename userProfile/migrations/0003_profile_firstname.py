# Generated by Django 3.1.4 on 2020-12-24 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0002_remove_profile_firstname'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='firstName',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
