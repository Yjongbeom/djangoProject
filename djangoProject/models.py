from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, username, division, password, **extra_fields):
        if not username:
            raise ValueError('학번이 있어야한다.')
        user = self.model(username=username,
                          division=division, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, division, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        return self.create_user(username, division, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(help_text="Student ID", max_length=100, unique=True)
    email = models.EmailField()
    division = models.CharField(help_text="front or back or admin", max_length=100)
    password = models.CharField(max_length=128, null=True, blank=True)
    name = models.CharField(max_length=128,  null=True, blank=True)
    week_id = models.IntegerField(help_text="Week ID", default=0)
    assignment_id = models.IntegerField(help_text="Assignment ID", default=0)
    notice_id = models.IntegerField(help_text="Notice ID",default=0)
    access = models.CharField(help_text="Access Token", max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['division', 'name']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username

class Week(models.Model):
    username = models.ForeignKey(User, related_name="weeks", on_delete=models.CASCADE, db_column="user_id")
    week_id = models.AutoField(primary_key=True)
    weeks = models.IntegerField(help_text="Weeks")

def upload_to_assignments(instance, filename):
    return f"assignments/{instance.week_id.user_id.student_id}/{instance.week_id.weeks}/{filename}"

class Assignment(models.Model):
    week_id = models.ForeignKey(Week, related_name="assignments", on_delete=models.CASCADE, db_column="week_id")
    weeks = models.IntegerField(help_text="Weeks")
    assignment_id = models.AutoField(primary_key=True)
    assignment_title = models.CharField(help_text="assignment_title", max_length=100)
    submission_status = models.CharField(max_length=1, choices=[('T', 'Submitted'), ('F', 'Not Submitted'), ('L', 'Late')])
    file = models.FileField(upload_to=upload_to_assignments)
    submission_time = models.DateTimeField()

class Notice(models.Model):
    username = models.ForeignKey(User, related_name="notices", on_delete=models.CASCADE, db_column="user_id")
    notice_id = models.AutoField(primary_key=True)
    notice_title = models.CharField(help_text="notice_title", max_length=100)
    notice_comment = models.TextField(help_text="notice_comment")
    notice_time = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='notice/')