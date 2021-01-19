# Generated by Django 3.1.4 on 2020-12-24 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.SlugField(max_length=100, primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=30, null=True)),
                ('lastName', models.CharField(max_length=30, null=True)),
                ('image', models.ImageField(null=True, upload_to='Profile')),
                ('dob', models.DateField(auto_now_add=True, null=True)),
                ('address', models.TextField(null=True)),
                ('companyEmail', models.EmailField(max_length=30, null=True)),
                ('companyName', models.EmailField(max_length=30, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]