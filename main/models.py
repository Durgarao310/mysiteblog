from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings



class Post(models.Model):
    title        = models.CharField(max_length=200)
    text         = models.TextField()
    date_posted  = models.DateTimeField(default=timezone.now)
    author       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


    @property
    def likes(self):
        return PostLike.objects.filter(post=self).count()

    def save(self):
        super().save()

class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.post.title} by {self.user.username}'
        
class Comment(models.Model): 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField()    
    approved = models.BooleanField(default=False)

    def approved(self):
        self.approved = True
        self.save()



    class Meta: 
        ordering = ['date']

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})



