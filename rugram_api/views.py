from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from posts.models import Post, Tag
from rugram_api.serializers import PostSerializer, PostDetailSerializer
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthorOrReadonly
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (IsAuthorOrReadonly, )

    def get_serializer_class(self):
        if self.request.method in ['GET', 'POST']:
            return PostSerializer
        return PostDetailSerializer

    @action(detail=True, methods=['get'])
    def by_tags(self, request, pk=None):
        tag = get_object_or_404(Tag, pk=pk)
        posts = Post.objects.filter(tags__pk=tag.pk)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
