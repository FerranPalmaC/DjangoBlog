from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post_list'), 
    path('create_post/', views.PostCreationView.as_view(), name='post_creation'),
    path('update_post/<slug:slug>', views.PostUpdateView.as_view(), name='post_edition'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
