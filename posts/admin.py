from django.contrib import admin
from .models import Post, Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date', 'updated_on', 'status')
    list_filter = ('status', 'author')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'publication_date',)
    list_filter = ('author', 'post',)
    

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

