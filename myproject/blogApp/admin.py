from django.contrib import admin
from .models import UserProfile,Posts,Category,Comment
# Register your models here.


admin.site.register(Comment)



class PostAdmin(admin.ModelAdmin):
    list_display=["id","title"]
admin.site.register(Posts,PostAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=["id","title"]
admin.site.register(Category,CategoryAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display=["id","user"]

admin.site.register(UserProfile,ProfileAdmin)






