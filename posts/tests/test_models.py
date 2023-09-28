from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from posts.models import Post

class PostTestClass(TestCase):

    def setUp(self):
        user = User.objects.create(username='test_user', password='123')
        # Create a default post
        Post.objects.create(
                title="Test post",
                author=user,
                content="Test content",
                status=0
            )

    def test_has_been_edited(self):
        post = Post.objects.get(pk=1)
        setattr(post, post.content, "Test content updated")
        post.save()
        post.refresh_from_db()
        self.assertTrue(post.has_been_edited())

    # User.objects.get(pk=1) does not work
    def test_two_posts_with_same_title_fails(self):
        with self.assertRaises(ValidationError):
            Post.objects.create(
                    title="Test post",
                    author=User.objects.all()[0],
                    content="Test content",
                    status=0
                )
            
