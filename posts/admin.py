from django.contrib import admin
from .models import Post
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date', 'updated_on', 'status')
    list_filter = ('status', )

admin.site.register(Post, PostAdmin)

