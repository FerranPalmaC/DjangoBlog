from django.http import HttpResponseForbidden
from django.views import generic
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreatePostForm, UpdatePostForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

class PostListView(generic.ListView):
    model = Post
    template_name = 'posts/post_list.html'
    queryset = Post.objects.filter(status=1).order_by('-publication_date')
   
    # A post request in this view means a delete action
    # Only the author of the post can delete the post
    def post(self):
        post_id = self.request.POST.get("post_id")
        post = Post.objects.get(pk=post_id)
        if post and post.author == self.request.user:
            post.delete()

        return redirect(reverse('posts:post_list'))
         

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_queryset(self):
        # Non published posts don't show detail 
        return Post.objects.filter(status=1)

class PostCreationView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'posts/post_creation.html'
    form_class = CreatePostForm

    # Auto assign the user creating the post as the author of the post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    template_name = 'posts/post_edition.html'
    form_class = UpdatePostForm

    # Only the author is allowed to update the post
    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        if post.author == self.request.user:
            return super().dispatch(request, *args, **kwargs)

        return redirect(reverse('posts:post_list')) 
