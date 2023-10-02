import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.test import TestCase
from django.utils import timezone
from posts.models import Post
from freezegun import freeze_time
class PostTestClass(TestCase):

    def setUp(self):
        user = User.objects.create(username='test_user', password='123')
        # Create a default post
        Post.objects.create(
                title="Test post",
                author=user,
            )

    def test_has_been_edited(self):
        Post.objects.create(
                title = "My post",
                author=User.objects.first()
                )
        with freeze_time(timezone.now() + datetime.timedelta(minutes=45)):
            edited_post = Post.objects.filter(title="My post").first()
            original_post = Post.objects.create(
                    title="Original post", 
                    author=User.objects.first(),
                    )
            setattr(edited_post, 'content', "Let's update the content")
            edited_post.save()
            self.assertTrue(edited_post.has_been_edited())
            self.assertFalse(original_post.has_been_edited())

    def test_two_posts_with_same_title_fails(self):
        with self.assertRaises(ValidationError):
            Post.objects.create(
                    title="Test post",
                    author=User.objects.first(),
                )

    def test_slug_automatically_created(self):
        title = "This is a title for a test post" 
        post = Post.objects.create(
                title=title,
                author=User.objects.first(),
                )
        self.assertEqual(slugify(title), post.slug)
