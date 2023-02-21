from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from posts.models import Group, Post
from .permissions import OwnerOrReadonly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (OwnerOrReadonly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer: PostSerializer) -> None:
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (OwnerOrReadonly,)
    serializer_class = CommentSerializer

    def perform_create(self, serializer: CommentSerializer) -> None:
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self) -> QuerySet:
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        comments_queryset = post.comments.all()
        return comments_queryset
