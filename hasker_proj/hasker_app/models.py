""" Create your models here."""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Tag(models.Model):
    """docstring for Tags"""
    name = models.CharField(max_length=200, blank=False)
    tag_id = models.IntegerField()

class Question(models.Model):
    """docstring for Questions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    question = models.TextField(max_length=200)
    voted = models.IntegerField(default=0)
    reg_date = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        """docstring for """
        return reverse('question_edit', kwargs={'pk': self.pk})

    def __str__(self):
        return self.question

class QTag(models.Model):
    """docstring for QTag"""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Answer(models.Model):
    """docstring for Answer"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(max_length=500)
    right = models.BooleanField(default=False)
    vote_up = models.IntegerField(default=0)
    vote_down = models.IntegerField(default=0)

    def vote_sum(self, pk):
        curent_answer = self.objects.get(pk=pk)
        return curent_answer.vote_up + curent_answer.vote_down

    def __str__(self):
        return self.answer

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'photos/' + filename

class Profile(models.Model):
    """docstring for Profile"models.Modelf __init__(self, arg):"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_directory_path)
    reg_date = models.DateField(auto_now_add=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
