from posts.models import Post
from rugram_api.serializers import PostSerializer, PostDetailSerializer
from rest_framework.viewsets import ModelViewSet


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET', 'POST']:
            return PostSerializer
        return PostDetailSerializer
