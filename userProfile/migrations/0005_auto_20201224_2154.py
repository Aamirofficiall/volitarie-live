# Generated by Django 3.1.4 on 2020-12-24 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0004_auto_20201224_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='companyName',
            field=models.CharField(max_length=256, null=True),
        ),
    ]