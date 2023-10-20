from django.urls import path

from .views import CommentCreateView, CommentDeleteView

urlpatterns = [
    path("create/", CommentCreateView.as_view(), name="comment_create"),
    path("delete/", CommentDeleteView.as_view(), name="comment_delete"),
]