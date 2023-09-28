from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'), 
    path('create_post/', views.PostCreationView.as_view(), name='post_creation'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
