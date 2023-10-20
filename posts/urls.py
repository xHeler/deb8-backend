from django.urls import path

from .views import PostList, PostDetail, PostCreateView, PostDeleteView


urlpatterns = [
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("delete/", PostDeleteView.as_view(), name="comment_delete"),
    path("<uuid:pk>/", PostDetail.as_view(), name="post_detail"),
    path("", PostList.as_view(), name="post_list"),
]
