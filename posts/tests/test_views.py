import datetime
from django.test import Client, TestCase
from django.utils import timezone
from posts.tests.factories import CommentFactory, PostFactory
from members.tests.factories import CustomUserFactory

class TestPostsAppViews(TestCase):
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
        cls.old_published_post = PostFactory(
                author = cls.main_user,
                creation_date = timezone.now() - datetime.timedelta(days=-3),
                publication_date = timezone.now()- datetime.timedelta(days=-3),
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
        cls.author_comment_post = CommentFactory(
                author=cls.main_user,
                post=cls.published_post
                )

class TestPostListView(TestPostsAppViews):
    
    def test_only_published_posts_are_shown_for_authenticated_user(self):
        pass

    def test_only_published_posts_are_shown_for_anonymous_user(self):
        pass

    def test_post_author_can_see_drafted_posts(self):
        pass

    def test_posts_ordered_from_newest_to_oldest(self):
        pass

    def test_authenticated_user_has_create_post_button(self):
        pass

    def test_anonymous_user_hasnt_create_button(self):
        pass

    def test_zero_comments_show_message(self):
        pass

    def test_one_comment_show_message(self):
        pass

    def test_multiple_comments_show_message(self):
        pass

class TestPostDetailView(TestPostsAppViews):
    
    def test_published_post_has_detail_for_authenticated_user(self):
        pass

    def test_published_post_has_detail_for_anonymous_user(self):
        pass

    def test_updated_post_have_last_updated_info(self):
        pass

    def test_non_updated_posts_have_not_last_updated_info(self):
        pass

    def test_comments_are_shown_for_authenticated_user(self):
        pass

    def test_comments_are_shown_for_anonymous_user(self):
        pass

    def test_no_comments_correctly_shown_for_authenticated_user(self):
        pass

    def test_no_comments_correctly_shown_for_anonymoys_user(self):
        pass

    def test_authenticated_user_can_comment(self):
        pass

    def test_anonymous_user_cant_comment(self):
        pass

    def test_author_of_post_can_delete_all_comments(self):
        pass

    def test_not_author_of_post_cant_delete_all_comments(self):
        pass

    def test_non_author_of_post_can_delete_his_comments(self):
        pass

    def test_anonymous_user_cant_delete_comments(self):
        pass


class TestPostCreationView(TestPostsAppViews):

    def test_authenticated_user_can_create_post(self):
        pass

    def test_anonymous_user_cant_create_post(self):
        pass

    def test_author_automatically_added_to_post_on_creation(self):
        pass

class TestPostUpdateView(TestPostsAppViews):

    def test_author_can_update_post(self):
        pass

    def test_not_author_cant_update_post(self):
        pass

    def test_update_from_draft_to_published(self):
        pass

    def test_cant_update_from_published_to_draft(self):
        pass

    def test_title_can_change_in_drafted_post(self):
        pass

    def test_title_cant_change_in_drafted_post(self):
        pass











