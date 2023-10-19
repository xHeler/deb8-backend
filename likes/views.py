
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

from drf_yasg.utils import swagger_auto_schema

from .serializers import LikeCreateSerializer
from .models import Like


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LikeCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=LikeCreateSerializer, operation_description="Add a new like",)
    def post(self, request, *args, **kwargs):
        like_instance = Like.objects.filter(post=request.data.get('post'), author=request.user).first()
        if like_instance:
            return Response({"detail": "Like already exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        like_serializer = LikeCreateSerializer(data=request.data)

        if like_serializer.is_valid():
            like = like_serializer.save(author=request.user)
            return Response(like_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(like_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LikeDeleteView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=LikeCreateSerializer, operation_description="Delete a existing like",)
    def delete(self, request, *args, **kwargs):
        like_instance = Like.objects.filter(post=request.data.get('post'), author=request.user).first()
        
        if like_instance:
            like_instance.delete()
            return Response({"detail": "Like removed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Like not exist."}, status=status.HTTP_404_NOT_FOUND)
