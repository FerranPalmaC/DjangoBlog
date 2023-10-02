from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils import timezone
# Create your models here.

STATUS = (
    (0, "Draft"),
    (1, "Published"),
)

class Post(models.Model):
    title = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=200, unique=True, null=False)
    publication_date = models.DateTimeField(editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    updated_on = models.DateTimeField()
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'slug': self.slug})

    def has_been_edited(self):
        publication_date = self.publication_date.strftime("%Y-%m-%d %H:%M:%S")
        updated_on = self.updated_on.strftime("%Y-%m-%d %H:%M:%S")
        return publication_date != updated_on

    def save(self, *args, **kwargs):
        ''' Only generate a new slug if the post doesn't already exist and update timestamp on save '''
        if not self.pk:
            self.publication_date = timezone.now()
            ''' If there is a Post with the same title, an error must be thrown
                because elseway two identical urls will be generated '''
            if Post.objects.filter(title=self.title).count() != 0:
                raise ValidationError("A post with the same title already exists", code="duplicated")
            self.slug = slugify(self.title)

        self.updated_on = timezone.now()
        super(Post, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-publication_date']
