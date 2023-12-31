import datetime
from django.test import Client, TestCase
from django.utils import timezone
from posts.tests.factories import CommentFactory, PostFactory
from members.tests.factories import CustomUserFactory
from django.urls import reverse
from posts.models import Post, Comment


class TestPostsAppViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.main_client = Client()
        cls.visitor_client = Client()
        cls.anonymous_client = Client()
        # Set up users
        cls.main_user = CustomUserFactory()
        cls.visitor_user = CustomUserFactory()
        cls.anonymous_user = CustomUserFactory()
        cls.main_client.force_login(cls.main_user)
        cls.visitor_client.force_login(cls.visitor_user)
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
        cls.post_to_delete = PostFactory(
                author = cls.main_user,
                status=1)
        cls.drafted_post= PostFactory(
                author = cls.main_user,
                creation_date=timezone.now() - datetime.timedelta(days=2), 
                publication_date=timezone.now() - datetime.timedelta(days=1), 
                updated_on = timezone.now() + datetime.timedelta(days=3)
                )
        cls.other_drafted_post = PostFactory(
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
        cls.old_comment = CommentFactory(
                author=cls.visitor_user,
                post=cls.old_published_post
                )
        cls.random_comment = CommentFactory(
                author=cls.visitor_user,
                post=cls.published_post
                )
        # Get querysets
        cls.qs_published_posts = Post.objects.filter(status=1).order_by('-publication_date')
        cls.qs_drafted_posts = Post.objects.filter(author=cls.main_user, status=0)

class TestPostListView(TestPostsAppViews):
    
    def test_only_published_posts_are_shown_for_authenticated_user(self):
        response = self.main_client.get(reverse('posts:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["post_list"], self.qs_published_posts)
        response = self.visitor_client.get(reverse('posts:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["post_list"], self.qs_published_posts)

    def test_only_published_posts_are_shown_for_anonymous_user(self):
        response = self.anonymous_client.get(reverse('posts:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["post_list"], self.qs_published_posts)

    def test_post_author_can_see_drafted_posts(self):
        response = self.main_client.get(reverse('posts:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["draft_posts"], self.qs_drafted_posts)

    def test_not_post_author_cant_see_drafted_posts(self):
        response = self.visitor_client.get(reverse('posts:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["draft_posts"].count(), 0)

    def test_posts_ordered_from_newest_to_oldest(self):
        response = self.main_client.get(reverse('posts:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['post_list'], self.qs_published_posts)

    def test_authenticated_user_has_create_post_button(self):
        response = self.main_client.post(reverse('posts:post_list'))
        self.assertRedirects(response, reverse('posts:post_creation'))

    def test_anonymous_user_hasnt_create_post_button(self):
        response = self.anonymous_client.post(reverse('posts:post_list'))
        self.assertTrue(response.status_code, 401)

    def test_authenticated_author_has_delete_post_button(self):
        response = self.main_client.post(reverse('posts:post_list'), {'post_id': self.post_to_delete.pk})
        self.assertRedirects(response, reverse('posts:post_list'))
        self.assertFalse(Post.objects.filter(pk=self.post_to_delete.pk).exists())

    def test_authenticated_user_has_not_delete_post_button(self):
        response = self.visitor_client.post(reverse('posts:post_list'), {'post_id': self.old_published_post.pk})
        self.assertTrue(response.status_code, 403)
        self.assertTrue(Post.objects.filter(pk=self.old_published_post.pk).exists())

    def test_anonymous_user_has_not_delete_post_button(self):
        response = self.anonymous_client.post(reverse('posts:post_list'), {'post_id': self.old_published_post.pk})
        self.assertTrue(response.status_code, 401)

    def test_authenticated_author_has_edit_drafted_post_button(self):
        response = self.main_client.post(reverse('posts:post_list'), {'post_id': self.drafted_post.pk})
        self.assertRedirects(response, reverse('posts:post_edition', kwargs={'slug': self.drafted_post.slug}))

    def test_authenticated_user_hasnt_edit_drafted_post_button(self):
        response = self.visitor_client.post(reverse('posts:post_list'), {'post_id': self.drafted_post.pk})
        self.assertTrue(response.status_code, 403)

    def test_anonymous_user_hasnt_edit_drafted_post_button(self):
        response = self.anonymous_client.post(reverse('posts:post_list'), {'post_id': self.drafted_post.pk})
        self.assertTrue(response.status_code, 401)


class TestPostDetailView(TestPostsAppViews):
    
    def test_published_post_has_detail_for_authenticated_user(self):
        response = self.main_client.get(self.published_post.get_absolute_url())
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.context['post'], self.published_post)

    def test_published_post_has_detail_for_anonymous_user(self):
        response = self.anonymous_client.get(self.published_post.get_absolute_url())
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.context['post'], self.published_post)

    def test_authenticated_user_can_comment(self):
        comment_content = "this is my comment content."
        response = self.visitor_client.post(
                self.published_post.get_absolute_url(),
                {'content': comment_content}
                )
        self.assertEqual(response.status_code, 302)
        post_comments = Comment.objects.filter(post=self.published_post, content=comment_content)
        self.assertTrue(post_comments.exists()) 

    def test_anonymous_user_cant_comment(self):
        comment_content = "this is my anonymous comment content."
        with self.assertRaises(ValueError):
            response = self.anonymous_client.post(
                    self.published_post.get_absolute_url(),
                    {'content': comment_content}
                    )
            self.assertEqual(response.status_code, 302)
            post_comments = Comment.objects.filter(post=self.published_post, content=comment_content)
            self.assertFalse(post_comments.exists()) 

    def test_author_of_post_can_delete_all_comments(self):
        others_post_comments = Comment.objects.filter(post__pk=self.published_post.pk).exclude(author=self.main_user)[0]
        response = self.main_client.post(self.published_post.get_absolute_url(), {'comment_id': others_post_comments.pk})
        self.assertTrue(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(post__pk=self.published_post.pk, pk=others_post_comments.pk).exists())

    def test_not_author_of_post_cant_delete_all_comments(self):
        others_post_comments = Comment.objects.filter(post__pk=self.published_post.pk).exclude(author=self.visitor_user)
        response = self.visitor_client.post(self.published_post.get_absolute_url(), {'comment_id': others_post_comments[0].pk})
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.get(pk=others_post_comments[0].pk)) 

    def test_non_author_of_post_can_delete_his_comments(self):
        own_comment = Comment.objects.filter(post__pk=self.published_post.pk, author__pk=self.visitor_user.pk)[0]
        response = self.visitor_client.post(self.published_post.get_absolute_url(), {'comment_id': own_comment.pk})
        self.assertTrue(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=own_comment.pk).exists())

    def test_anonymous_user_cant_delete_comments(self):
        comment_id = Comment.objects.all()[0].pk
        previous_comments = Comment.objects.filter(post__pk=self.published_post.pk).count()
        with self.assertRaises(ValueError):
            response = self.anonymous_client.post(
                    self.published_post.get_absolute_url(),
                    {'comment_id': comment_id}
                    )
            self.assertEqual(response.status_code, 403)
            posterior_comments = Comment.objects.filter(post__pk=self.published_post.pk).count()
            self.assertEqual(previous_comments, posterior_comments)

class TestPostCreationView(TestPostsAppViews):

    def test_authenticated_user_can_access_create_post(self):
        response = self.visitor_client.get(reverse('posts:post_creation'))
        self.assertTrue(response.status_code, 200)

    def test_anonymous_user_cant_access_create_post(self):
        response = self.anonymous_client.post(reverse('posts:post_creation'))
        self.assertTrue(response.status_code, 403)

    def test_authenticated_user_can_create_post(self):
        post_data = {
            'title': 'Test Post',
            'content': 'This is a test post content.',
            'status': 1  
        }
        response = self.visitor_client.post(reverse('posts:post_creation'), post_data)
        self.assertEqual(response.status_code, 302)
        created_post = Post.objects.filter(author=self.visitor_user, title='Test Post', content='This is a test post content.')
        self.assertTrue(created_post.exists())

    def test_author_automatically_added_to_post_on_creation(self):
        post_data = {
            'title': 'Test Post',
            'content': 'This is a test post content.',
            'status': 1  
        }
        response = self.visitor_client.post(reverse('posts:post_creation'), post_data)
        self.assertEqual(response.status_code, 302)
        created_post = Post.objects.get(author=self.visitor_user, title='Test Post', content='This is a test post content.')
        self.assertTrue(created_post)
        self.assertEqual(created_post.author, self.visitor_user)

class TestPostUpdateView(TestPostsAppViews):

    def test_author_can_update_post(self):
        response =  self.main_client.get(reverse('posts:post_edition', kwargs={'slug': self.published_post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_not_author_cant_update_post(self):
        response = self.visitor_client.get(reverse('posts:post_edition', kwargs={'slug': self.published_post.slug}))
        self.assertEqual(response.status_code, 403)
            
    def test_update_from_draft_to_published(self):
       updated_post_data = {
            'title': self.drafted_post.title,
            'content': self.drafted_post.content,
            'status': 1
       }
       response = self.main_client.post(reverse('posts:post_edition', kwargs={'slug': self.drafted_post.slug}), updated_post_data)
       self.drafted_post.refresh_from_db()
       self.assertEqual(response.status_code, 302)
       self.assertTrue(self.drafted_post.status, 1)

    def test_cant_update_from_published_to_draft(self):
       updated_post_data = {
            'title': self.drafted_post.title,
            'content': self.drafted_post.content,
            'status': 0 
       }
       response = self.main_client.post(reverse('posts:post_edition', kwargs={'slug': self.drafted_post.slug}), updated_post_data)
       self.drafted_post.refresh_from_db()
       self.assertEqual(response.status_code, 302)
       self.assertFalse(self.drafted_post.status, 0)

    def test_title_can_change_in_drafted_post(self):
       updated_post_data = {
            'title': 'Updated post title',
            'content': self.other_drafted_post.content,
            'status': self.other_drafted_post.status 
       }
       response = self.main_client.post(reverse('posts:post_edition', kwargs={'slug': self.other_drafted_post.slug}), updated_post_data)
       self.other_drafted_post.refresh_from_db()
       self.assertEqual(response.status_code, 302)
       self.assertEqual(self.other_drafted_post.title, updated_post_data['title'])

    def test_title_cant_change_in_published_post(self):
       updated_post_data = {
            'title': 'Updated post title',
            'content': self.old_published_post.content,
            'status': self.old_published_post.status 
       }
       response = self.main_client.post(reverse('posts:post_edition', kwargs={'slug': self.old_published_post.slug}), updated_post_data)
       self.old_published_post.refresh_from_db()
       self.assertEqual(response.status_code, 302)
       self.assertNotEqual(self.old_published_post.title, updated_post_data['title'])

    def test_content_can_change_in_drafted_post(self):
       updated_post_data = {
            'title': self.other_drafted_post.title,
            'content': "The new content of the post",
            'status': self.other_drafted_post.status 
       }
       response = self.main_client.post(reverse('posts:post_edition', kwargs={'slug': self.other_drafted_post.slug}), updated_post_data)
       self.other_drafted_post.refresh_from_db()
       self.assertEqual(response.status_code, 302)
       self.assertEqual(self.other_drafted_post.content, updated_post_data['content'])

    def test_content_can_change_in_published_post(self):
       updated_post_data = {
            'title': self.published_post.title,
            'content': "The new content of the post",
            'status': self.published_post.status 
       }
       response = self.main_client.post(reverse('posts:post_edition', kwargs={'slug': self.published_post.slug}), updated_post_data)
       self.published_post.refresh_from_db()
       self.assertEqual(response.status_code, 302)
       self.assertEqual(self.published_post.content, updated_post_data['content'])








