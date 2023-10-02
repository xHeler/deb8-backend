from django.urls import path

from .views import PostList, PostDetail, PostCreateView


urlpatterns = [
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("<uuid:pk>/", PostDetail.as_view(), name="post_detail"),
    path("", PostList.as_view(), name="post_list"),
]
