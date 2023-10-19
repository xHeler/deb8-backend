
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import CommentCreateSerializer, CommentDeleteSerializer
from .models import Comment


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CommentCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=CommentCreateSerializer, operation_description="Add a new comment",)
    def post(self, request, *args, **kwargs):
        comment_serializer = CommentCreateSerializer(data=request.data)

        if comment_serializer.is_valid():
            comment = comment_serializer.save(author=request.user)
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CommentDeleteView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='comment_id',
                in_=openapi.IN_FORM,
                description='UUID of the comment to delete',
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        operation_description="Delete an existing comment",
    )
    def delete(self, request, *args, **kwargs):
        comment_id = request.data.get('comment_id')
        
        if not comment_id:
            return Response({"detail": "Comment ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        comment_instance = Comment.objects.filter(comment_id=comment_id, author=request.user).first()
        
        if comment_instance:
            comment_instance.delete()
            return Response({"detail": "Comment removed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Comment not found or you don't have permission to delete it."}, status=status.HTTP_404_NOT_FOUND)