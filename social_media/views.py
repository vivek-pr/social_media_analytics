from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer
from .tasks import analyze_post


class PostCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostAnalysisView(APIView):
    def get(self, request, id):
        result = analyze_post.delay(id)
        analysis = result.get()
        return Response(analysis)

