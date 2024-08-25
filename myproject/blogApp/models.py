from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user =  models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.TextField(max_length=100)
    profile_picture=models.ImageField(blank=True,null=True,upload_to="profile/images")
    bio=models.TextField(blank=True,null=True)
    information=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title=models.CharField(max_length=100)
    def __str__(self):
        return self.title

    

class Posts(models.Model):
    title=models.CharField(max_length=200)
    short_description=models.CharField(max_length=200)
    description=models.TextField()
    time_to_read = models.CharField(max_length=20)
    featured_image=models.ImageField(upload_to="blog/images")
    author=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    categories=models.ManyToManyField(Category)
    published_date=models.DateField(auto_now_add=True)
    is_draft=models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False)
    likes = models.ManyToManyField(User,related_name='post_likes')
    save_post = models.ManyToManyField(User,related_name="saved_posts")

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    blog=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    comment=models.TextField()

    def __str__(self):
        return str(self.id)
    


