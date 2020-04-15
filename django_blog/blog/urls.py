from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home , name='blog-home'),
    path('', views.PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('user/<str:username>', views.UserPostListView.as_view(), name='user-posts'),
    path('like_post/' , views.like_post, name="like_post"),
    path('about/', views.about , name='blog-about'),
]
