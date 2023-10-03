from django.views import generic
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreatePostForm

class PostListView(generic.ListView):
    model = Post
    template_name = 'posts/post_list.html'
    queryset = Post.objects.filter(status=1).order_by('-publication_date')

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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
