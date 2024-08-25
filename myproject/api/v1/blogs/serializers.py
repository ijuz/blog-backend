from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from blogApp.models import Posts,Category,Comment,UserProfile
import datetime





class PostSerializers(ModelSerializer):
    likes = serializers.SerializerMethodField()
    def get_likes(self,obj):
        return obj.likes.count()
    author=serializers.SerializerMethodField()
    def get_author(self,obj):
        return obj.author.us0er.first_name
    categories=serializers.SerializerMethodField()
    def get_categories(self,obj):
        categories=obj.categories.all()
        titles=[category.title for category in categories]
        return titles
    
    class Meta:
        fields=("id","title","short_description","featured_image","author",'published_date','categories','likes',)
        model=Posts


class DetailPost(ModelSerializer):
    save_post = serializers.SerializerMethodField()
    def get_save_post(self,obj):
        request = self.context.get('request')
        if obj.save_post.filter(username=request.user.username).exists():
            return True
        else:
            return False
    author=serializers.SerializerMethodField()
    categories=serializers.SerializerMethodField()
    likes=serializers.SerializerMethodField()
    def get_likes(self,obj):
        return obj.likes.count()
    is_liked =serializers.SerializerMethodField()
    def get_is_liked(self,obj):
        request = self.context.get("request")
        if obj.likes.filter(username=request.user.username).exists():
            return True
        else:
            return False
    def get_categories(self,obj):
        return [category.title for category in obj.categories.all()]

    
    def get_author(self,obj):
        return obj.author.user.first_name
    class Meta:
        fields = ("id","title","short_description","featured_image","description","author",'published_date','is_draft','is_deleted','categories','is_liked','likes','save_post')
        model=Posts







class CreatePost(serializers.ModelSerializer):
    categories = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Posts
        fields = ("id", "title", "short_description", "featured_image", "description", "categories","is_draft")

    def create(self,obj ):
        categories_string = obj.pop('categories')[0]
        category_titles = [title.strip() for title in categories_string.split(',')]
        
        post = Posts.objects.create(**obj)
        
        for title in category_titles:
            category, created = Category.objects.get_or_create(title=title)
            post.categories.add(category)
        
        return post
    
class MyPost(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields=("id","title","short_description")



class CommentSerializer(ModelSerializer):
    username = serializers.SerializerMethodField()
    def get_username(self,obj):
        request = self.context.get('request')
        return request.user.username
    
    class Meta:
        model = Comment
        fields=("id",'comment','username','date')


class UserSerializer(ModelSerializer):
    email = serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = UserProfile
        fields = ("id","email","name","profile_picture","bio",'information')


