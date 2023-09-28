from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
# Create your models here.

STATUS = (
    (0, "Draft"),
    (1, "Published"),
)

class Post(models.Model):
    title = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=200, unique=True, null=False)
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'slug': self.slug})

    def has_been_edited(self):
        return self.publication_date != self.updated_on

    def save(self, *args, **kwargs):
        # Only generate a new slug if the post doesn't already exist 
        if not self.pk:
            # If there is a Post with the same title, an error must be thrown
            # because elseway two identical urls will be generated
            if Post.objects.filter(title=self.title).count() != 0:
                raise ValidationError("A post with the same title already exists", code="duplicated")
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-publication_date']
