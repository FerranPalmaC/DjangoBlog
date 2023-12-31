from django.http import HttpResponseForbidden
from django.http.response import Http404, HttpResponse, HttpResponseNotAllowed
from django.views import View, generic
from django.views.generic.detail import SingleObjectMixin
from .models import Comment, Post
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateCommentForm, CreatePostForm, UpdatePostForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

class PostListView(generic.ListView):
    model = Post
    template_name = 'posts/post_list.html'
    queryset = Post.objects.filter(status=1).order_by('-publication_date')
   
    # A post request in this view means: create, delete or edit a post 
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)  
        post_id = self.request.POST.get("post_id")
        
        # User wants to create a post 
        if not post_id:
            return redirect(reverse('posts:post_creation'))
       
        
        blog_post = Post.objects.get(pk=post_id)
        if blog_post:
            # User wants to delete a post
            if blog_post.status == 1 and blog_post.author == request.user:
                blog_post.delete()
                return redirect(reverse('posts:post_list'))
            # User wants to edit a post
            if blog_post.status == 0 and blog_post.author == request.user:
                return redirect(reverse('posts:post_edition', kwargs={'slug': blog_post.slug}))
        
        return HttpResponse('Forbidden', status=403) 

    # If the user has drafted posts, he can also see them in the post list view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_drafted_posts = Post.objects.filter(author=self.request.user, status=0)
            context['draft_posts'] = user_drafted_posts
        return context


class PostView(View):
    # Wrap the detail view and the comment view in a single view
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentCreationView.as_view()
        form = CreateCommentForm(request.POST)
        form.instance.author = request.user
        form.instance.post = Post.objects.get(slug=kwargs['slug'])
        if form.is_valid():
            form.save()
        return view(request, *args, **kwargs)


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_queryset(self):
        # Non published posts don't show detail unless you are the author
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        if self.request.user == post.author or post.status == 1:
            return Post.objects.filter(slug=self.kwargs['slug']) 
        return Post.objects.none() 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # When creating a drafted post, it can't be commented
        if context['post'].status == 1:
            context['comment_form'] = CreateCommentForm()
        return context

class CommentCreationView(SingleObjectMixin, generic.FormView):
    form_class = CreateCommentForm
    model = Comment
    # So the form stays in the same page
    success_url = '#'

    # Only a logged in user can comment 
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden
        
        if comment_id := self.request.POST.get("comment_id"):
            comment = Comment.objects.get(pk=comment_id)
            post = Post.objects.get(comments__id=comment_id)
            if request.user == comment.author or request.user == post.author:
                comment.delete()
                return redirect(reverse('posts:post_detail', kwargs={'slug': post.slug}))
            else:
                return HttpResponseForbidden()
        return super().post(request, *args, **kwargs)

class PostCreationView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'posts/post_creation.html'
    form_class = CreatePostForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return super().post(request, *args, **kwargs)


    # Auto assign the user creating the post as the author of the post
    def form_valid(self, form):
        if not Post.objects.filter(pk = form.instance.pk).exists():
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

        return HttpResponseForbidden() 
