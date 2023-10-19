from django.urls import path

from .views import LikeCreateView, LikeDeleteView

urlpatterns = [
    path("create/", LikeCreateView.as_view(), name="post_create"),
    path("delete/", LikeDeleteView.as_view(), name="post_delete"),
]