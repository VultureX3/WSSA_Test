# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Organization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='employees', null=True, on_delete=models.SET_NULL)
    is_admin = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pass_date = models.DateField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Question(models.Model):
    text = models.TextField(max_length=1000)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.TextField(max_length=1000)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='answers', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.text


class TestResult(models.Model):
    test = models.ForeignKey(Test, related_name='test_results', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
