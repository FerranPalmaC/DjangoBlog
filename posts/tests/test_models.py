from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.test import TestCase
from posts.models import Post

class PostTestClass(TestCase):

    def setUp(self):
        user = User.objects.create(username='test_user', password='123')
        # Create a default post
        Post.objects.create(
                title="Test post",
                author=user,
            )

    def test_has_been_edited(self):
        post = Post.objects.get(pk=1)
        setattr(post, post.content, "Test content updated")
        post.save()
        self.assertTrue(post.has_been_edited())

    # User.objects.get(pk=1) does not work, altough setUp user has pk=1
    def test_two_posts_with_same_title_fails(self):
        with self.assertRaises(ValidationError):
            Post.objects.create(
                    title="Test post",
                    author=User.objects.all()[0],
                )

    def test_slug_automatically_created(self):
        title = "This is a title for a test post" 
        post = Post.objects.create(
                title=title,
                author=User.objects.all()[0],
                )
        self.assertEqual(slugify(title), post.slug)
