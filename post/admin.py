from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ['user', 'created', 'is_edited', 'edited']
    list_filter = ['created', 'edited']
    search_fields = ['id']
    
