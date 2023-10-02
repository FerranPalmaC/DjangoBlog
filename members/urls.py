from django.urls import path
from . import views

app_name = "members"

urlpatterns = [
    path('login/', views.login_view, name='signup'),
    path('logout/', views.logout_view, name='signout'),
    path('signin/', views.signup, name='signup'),
]