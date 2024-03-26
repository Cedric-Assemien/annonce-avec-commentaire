from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class ContactForm(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=20)
    message = models.TextField()
    def __str__(self):
        return self.subject 
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, default="")
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        formatted_date = self.created_at.strftime("%Y-%m-%dT%H:%M:%S")
        return  f"{self.title} / {formatted_date}"

class PostApproved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        formatted_date = self.created_at.strftime("%Y-%m-%dT%H:%M:%S")
        return  f"{self.title} / {formatted_date}"
    

class Comment(models.Model):
    post = models.ForeignKey(PostApproved, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Commenté par {self.name} sur {self.post.title}"


