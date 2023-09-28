import datetime 
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from posts.models import Post

class PostTestViews(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test_user', password='123')
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
                author=User.objects.all()[0],
                status=1
                )
        response = self.client.get(reverse('posts:post_list'))
        published_ordered_posts = Post.objects.filter(status=1).order_by('-publication_date')
        self.assertEqual(list(published_ordered_posts), list(response.context['post_list']))
       
