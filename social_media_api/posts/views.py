from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

from accounts.models import CustomUser
from notifications.models import Notification
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, post=post)

    if created and post.author != user:
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb='liked your post',
            content_type=ContentType.objects.get_for_model(post),
            object_id=post.id
        )

    return Response({'status': 'post liked'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)
    user = request.user

    Like.objects.filter(user=user, post=post).delete()

    return Response({'status': 'post unliked'}, status=status.HTTP_200_OK)

# Keep your existing viewsets below
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
