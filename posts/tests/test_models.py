import datetime
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from django.template.defaultfilters import slugify
from django.test import Client, TestCase
from django.utils import timezone
from posts.tests.factories import CommentFactory, PostFactory
from members.tests.factories import CustomUserFactory

class TestPostsAppModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        # Set up users
        cls.main_user = CustomUserFactory()
        cls.visitor_user = CustomUserFactory()
        cls.anonymous_user = CustomUserFactory()
        cls.client.login(username=cls.main_user.username, password=cls.main_user.password)
        cls.client.login(username=cls.visitor_user.username, password=cls.visitor_user.password)
        # Set up posts
        cls.published_post = PostFactory(
                author = cls.main_user,
                creation_date = timezone.now(),
                publication_date = timezone.now(),
                updated_on = timezone.now(),
                status=1)

        cls.drafted_post= PostFactory(
                author = cls.main_user,
                creation_date=timezone.now() - datetime.timedelta(days=2), 
                publication_date=timezone.now() - datetime.timedelta(days=1), 
                updated_on = timezone.now() + datetime.timedelta(days=3)
                )
        cls.edited_post = PostFactory(
                author = cls.main_user,
                creation_date=timezone.now() - datetime.timedelta(days=2), 
                publication_date=timezone.now() - datetime.timedelta(days=1), 
                updated_on = timezone.now() + datetime.timedelta(days=3),
                status=1
                )
        # Set up comments
        cls.comment_post = CommentFactory(
                author=cls.visitor_user,
                post=cls.published_post
                )

class TestPostModel(TestPostsAppModels):

    def test_str_method(self):
        self.assertEqual(self.published_post.title, str(self.published_post))

    def test_has_been_edited(self):
        self.assertTrue(self.edited_post.has_been_edited())
        self.assertFalse(self.published_post.has_been_edited())
        # Drafted posts cant be edited 
        self.assertFalse(self.drafted_post.has_been_edited())

    def test_two_posts_with_same_title_fail(self):
        with self.assertRaises(ValidationError):
            _ = PostFactory(title=self.published_post.title)

    def test_slug_automatically_created(self):
        title = "This is a test title"
        auto_slug_post = PostFactory(title=title)
        self.assertEqual(slugify(title), auto_slug_post.slug)

    def test_title_cant_be_longer_than_256_characters(self):
        title = "x" * 257
        with self.assertRaises(DataError):
           PostFactory(title=title) 
   
class TestCommentModel(TestPostsAppModels):
      
    def test_str_method(self):
        self.assertEqual(f"{self.comment_post.author.username} -- {self.comment_post.author.email}-{self.comment_post.post.title}", str(self.comment_post))
