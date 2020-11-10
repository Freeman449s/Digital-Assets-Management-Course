from django.db import models
from datetime import datetime
# Create your models here.


class People(models.Model):
    name = models.CharField(default="", max_length=30, verbose_name="姓名", help_text="姓名")
    dateofbirth = models.FloatField(default=1900, null=True,verbose_name="出生年")
    dateofdeath = models.FloatField(default=2020, null=True,verbose_name="逝世年")
    birthplace =  models.CharField(default="", max_length=40, verbose_name="出生地点")
    longitude = models.FloatField(default=0, null=True,verbose_name="出生地经度")
    latitude =  models.FloatField(default=0, null=True,verbose_name="出生地维度")
    major = models.CharField(default="", max_length=30, verbose_name="专业领域", help_text="专业领域")
    gender = models.CharField(max_length=6,  default="男", verbose_name="性别")
    introduction = models.CharField(default="",max_length=300,verbose_name="个人介绍")
    nationality = models.CharField(default="", max_length=20, verbose_name="国籍")
    academy = models.CharField(default="", max_length=50, verbose_name="毕业院校")
    headimage = models.ImageField(upload_to="people/images/", null=True, blank=True, verbose_name="人物头像图")
    repwork = models.CharField(default="", max_length=100, verbose_name="代表作品")
    majorAchv =  models.CharField(default="", max_length=300, verbose_name="主要成就")

    class Meta:
        verbose_name = '文化人物'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PeopleWorks(models.Model):
    author = models.ForeignKey("People", null=True, blank=True, verbose_name="作品作者", help_text="作品作者")
    title =  models.CharField(default="", max_length=100, verbose_name="作品名", help_text="作品名")
    image = models.ImageField(upload_to="peopleworks/images/", null=True, blank=True, verbose_name="作品图片")


    class Meta:
        verbose_name = '作品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title