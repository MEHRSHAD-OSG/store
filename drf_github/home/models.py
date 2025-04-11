from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=160)
    age = models.PositiveSmallIntegerField()
    email = models.EmailField()
    updated = models.DateTimeField(auto_now=True)
    creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated']  # Order by most recent updates

    def __str__(self):
        return self.name


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='q_users')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='a_user')
    # related_name = when we want to access question in answers we use related name in question query
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Answer'
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return self.body
