# Generated by Django 3.1.4 on 2020-12-26 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0006_auto_20201226_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='target_audience',
            field=models.CharField(choices=[('S', '20-30'), ('M', '30-40'), ('B', '40-50')], max_length=1, null=True),
        ),
    ]
