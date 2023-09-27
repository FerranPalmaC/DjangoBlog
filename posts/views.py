from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Post
# Create your views here.

class PostListView(generic.ListView):
    model = Post
    template_name = 'posts/post_list.html'
    queryset = Post.objects.filter(status=1).order_by('-publication_date')

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
