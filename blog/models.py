from django.db import models
from django.contrib.auth.models import User

class Blog_view(models.Model):
    blog_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    textcontent = models.TextField(default = "This blog is under Construction !")

    def __str__(self):
        return self.blog_title

# Create your models here.
