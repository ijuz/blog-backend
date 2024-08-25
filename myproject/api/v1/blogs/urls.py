from django.urls import path
from  . import views

urlpatterns = [
   
    path('',views.blog_list),
    path('view/<int:pk>/',views.retrive_blog),
    path('create/',views.create),
    path('edit/<int:pk>/',views.update_blog),
    path('mypost/',views.my_post),
    path('search/',views.Search_Post),
    path('like/<int:pk>/',views.likes),
    path('save-post/<int:pk>/',views.save_posts),
    path('saved-posts/',views.saved_posts),
    path('create-comment/<int:pk>/',views.create_comment),
    path('comments/view/<int:pk>/',views.view_comments),
    path('view-profile /',views.user_profile)
] 