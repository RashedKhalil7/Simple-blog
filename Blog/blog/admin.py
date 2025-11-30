from django.contrib import admin
from .models import Post , Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title' , 'slug' , 'author' , 'created' , 'status']
    list_filter = ['status' , 'created' , 'updated']
    search_fields = ['title' , 'author' , 'body']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name' , 'email' , 'post' , 'created' , 'active']
    list_filter = ['active' , 'created' , 'updated']
    search_fields = ['name' , 'email' , 'body']