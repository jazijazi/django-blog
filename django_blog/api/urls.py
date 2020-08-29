from django.urls import path, re_path , include
from rest_framework import routers
from . import views

app_name='api'

router = routers.DefaultRouter()
router.register('posts' , views.PostView)
router.register('users' , views.UserView)

urlpatterns = [
    path("v1/" , include(router.urls)),
    path("v1/changepassword" , views.ChangePasswordView.as_view()),
    path("v1/like_post/<int:post_id>" , views.like_post_api)
]