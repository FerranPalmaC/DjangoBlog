import datetime 
from members.models import CustomUser
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from posts.models import Post
from freezegun import freeze_time

class PostTestViews(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username='test_user', password='123')
        Post.objects.create(
                title='Test published post',
                author=user,
                status=1
                )
        Post.objects.create(
                title='Test drafted post',
                author=user,
                status=0
                )

class PostTestListView(PostTestViews):

    def test_authenticated_user_can_access(self):
        self.client.login(username='test_user', password='123') 
        response = self.client.get(reverse('posts:post_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_anonymous_user_can_access(self):
        response = self.client.get(reverse('posts:post_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_only_posted_posts_displayed(self):
        response = self.client.get(reverse('posts:post_list'))
        published_posts = Post.objects.filter(status=1)
        self.assertEqual(list(published_posts), list(response.context['post_list']))

    def test_posts_ordered_by_latest(self):
        Post.objects.create(
                title='First post',
                publication_date=timezone.now() + datetime.timedelta(days=-10),
                author=CustomUser.objects.all()[0],
                status=1
                )
        response = self.client.get(reverse('posts:post_list'))
        published_ordered_posts = Post.objects.filter(status=1).order_by('-publication_date')
        self.assertEqual(list(published_ordered_posts), list(response.context['post_list']))

    def test_authenticated_user_has_create_post_button(self):
        self.client.login(username='test_user', password='123') 
        response = self.client.get(reverse('posts:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, b'Create post')

    def test_anonymous_user_hasnt_create_post_button(self):
        response = self.client.get(reverse('posts:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, b'Create post')

class PostTestDetailView(PostTestViews):
    def test_published_post_has_detail(self):
        publihed_post = Post.objects.filter(status=1).first()
        url = reverse('posts:post_detail', kwargs={'slug':  publihed_post.slug})
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)

    def test_draft_post_has_not_detail(self):
        publihed_post = Post.objects.filter(status=0).first()
        url = reverse('posts:post_detail', kwargs={'slug':  publihed_post.slug})
        response = self.client.get(url)
        self.assertTrue(response.status_code, 404)

    def test_updated_posts_have_last_updated_info(self):
        edited_post = Post.objects.filter(status=1).first()
        with freeze_time(timezone.now() + datetime.timedelta(minutes=45)):
            setattr(edited_post, edited_post.content, "Test content updated")
            edited_post.save()
            url = reverse('posts:post_detail', kwargs={'slug': edited_post.slug})
            response = self.client.get(url)
            self.assertContains(response, b'Eddited on')

    def test_non_updated_posts_have_not_last_updated_info(self):
        non_edited_post = Post.objects.create(
                title="Hello",
                author=CustomUser.objects.first(),
                status=1
                )
        url = reverse('posts:post_detail', kwargs={'slug':  non_edited_post.slug})
        response = self.client.get(url)
        self.assertNotContains(response, b'Eddited on')

class PostTestCreationView(PostTestViews):
    def test_authenticated_user_can_create_post(self):
        self.client.login(username='test_user', password='123') 
        response = self.client.get(reverse('posts:post_creation'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cant_create_post(self):
        response = self.client.get(reverse('posts:post_creation'))
        ''' Maybe it should return a 401, but LoginRequiredMixin returns 302 by default '''
        self.assertEqual(response.status_code, 302)
