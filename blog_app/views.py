from django.shortcuts import render
from blog_app.serializers import UserRegistrationSerializer, BlogSerializer, UpdateUserProfileSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Blog, User
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class RgisterUserApiView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)

class UserProfileApiView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        user = request.user
        serializer = UpdateUserProfileSerializer(user, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user
        user_data = User.objects.get(id=user.id)
        serializer = UpdateUserProfileSerializer(user_data)
        return Response(serializer.data)

class BlogApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author = user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        blogs = Blog.objects.filter(author=request.user)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        user = request.user
        blog = Blog.objects.get(id=pk)
        if blog.author != user:
            return Response({'error': "You're not the author of this blog"}, status=status.HTTP_403_FORBIDDEN)
        serializer = BlogSerializer(blog,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = request.user
        blog = Blog.objects.get(id=pk)
        if blog.author != user:
            return Response({'error': "You're not the author of this blog"}, status=status.HTTP_403_FORBIDDEN)
        blog.delete()
        return Response({'msg':'Delted Successfully'}, status= status.HTTP_200_OK)


class BlogListPaginator(PageNumberPagination):
    page_size = 3

class AllBlogApiView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        blogs = Blog.objects.all()
        paginator = BlogListPaginator()
        paginated_blog = paginator.paginate_queryset(blogs, request)
        serializer = BlogSerializer(paginated_blog, many=True)
        return paginator.get_paginated_response(serializer.data)

    

            


# @api_view(['POST'])
# def register_user(request):
#     serializer = UserRegistrationSerializer(data= request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)