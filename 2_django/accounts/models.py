from django.db import models
from django.contrib.auth.models import AbstractUser
# from django_resized import ResizedImageField

# Create your models here.
class User(AbstractUser):
    SEX_CHOICES = (('여성', '여성'), ('남성', '남성'))
    sex=models.CharField(max_length=10, choices = SEX_CHOICES, verbose_name='성별', default=None, null=True)
    age=models.IntegerField(default=None, null=True)

