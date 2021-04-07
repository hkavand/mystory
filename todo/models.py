from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='data/story_pics',default='pic1.jpg')
    important = models.BooleanField(default=False)
    numberofcomments = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class AboutUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    slogan = models.CharField(max_length = 75 , blank=True)
    pic = models.ImageField(upload_to='data/profile_pics/',default='profile.png')
    def __str__(self):
        return 'About ' + self.user.username

class Comment(models.Model):
    authoruser = models.ForeignKey(User,on_delete=models.CASCADE)
    postid = models.IntegerField()
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    commentuser = models.CharField(max_length=150,blank=True)
    


