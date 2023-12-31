# Generated by Django 5.0 on 2023-12-23 16:55

import django.db.models.deletion
import django.utils.timezone
import djangoProject.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(help_text='Student ID', max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('division', models.CharField(help_text='front or back or admin', max_length=100)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('week_id', models.IntegerField(default=0, help_text='Week ID')),
                ('assignment_id', models.IntegerField(default=0, help_text='Assignment ID')),
                ('notice_id', models.IntegerField(default=0, help_text='Notice ID')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.IntegerField(unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('notice_id', models.AutoField(primary_key=True, serialize=False)),
                ('notice_title', models.CharField(help_text='notice_title', max_length=100)),
                ('notice_comment', models.TextField(help_text='notice_comment')),
                ('notice_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('file', models.FileField(upload_to='notice/')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='notices', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=255, unique=True)),
                ('student', models.ForeignKey(db_column='username', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('week_id', models.AutoField(primary_key=True, serialize=False)),
                ('weeks', models.IntegerField(help_text='Weeks')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='weeks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('weeks', models.IntegerField(help_text='Weeks')),
                ('assignment_id', models.AutoField(primary_key=True, serialize=False)),
                ('assignment_title', models.CharField(help_text='assignment_title', max_length=100)),
                ('submission_status', models.CharField(choices=[('T', 'Submitted'), ('F', 'Not Submitted'), ('L', 'Late')], max_length=1)),
                ('file', models.FileField(upload_to=djangoProject.models.upload_to_assignments)),
                ('submission_time', models.DateTimeField()),
                ('week_id', models.ForeignKey(db_column='week_id', on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='djangoProject.week')),
            ],
        ),
    ]
