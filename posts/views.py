from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Post
from .serializers import PostCreateSerializer, PostReadSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostReadSerializer

    page_param = openapi.Parameter(
        'page', openapi.IN_QUERY, description="Page number for pagination", type=openapi.TYPE_INTEGER
    )
    
    page_size_param = openapi.Parameter(
        'page_size', openapi.IN_QUERY, description="Number of items per page", type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(manual_parameters=[page_param, page_size_param])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostReadSerializer


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PostCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PostCreateSerializer, operation_description="Add a new post with an image",
                         manual_parameters=[openapi.Parameter('image', in_=openapi.IN_FORM, type=openapi.TYPE_FILE)])
    def post(self, request, *args, **kwargs):
        post_serializer = PostCreateSerializer(data=request.data)

        if post_serializer.is_valid():
            post = post_serializer.save(author=request.user)
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PostDeleteView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='post_id',
                in_=openapi.IN_FORM,
                description='UUID of the post to delete',
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        operation_description="Delete an existing post",
    )
    def delete(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        
        if not post_id:
            return Response({"detail": "Post ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        post_instance = Post.objects.filter(post_id=post_id, author=request.user).first()
        
        if post_instance:
            post_instance.delete()
            return Response({"detail": "Post removed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Post not found or you don't have permission to delete it."}, status=status.HTTP_404_NOT_FOUND)