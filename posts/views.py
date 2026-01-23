from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Category, Comment, Post
from .serializers import CategoryReadSerializer,CommentReadSerializer,CommentWriteSerializer,PostReadSerializer,PostWriteSerializer,

from .permissions import IsAuthenticated, IsAuthorOrReadOnly

# Category is going to be read-only, so we use ReadOnlyModelViewSet

class CategoryViewset(viewsets.ReadOnlyModelViewSet):
	"""
    List and Retrieve post categories
    """

    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer
    permission_classes = (permissions.AllowAny,)


class PostViewSet(viewsets.ModelViewSet):
	# crud post

	queryset = Post.objects.all()

	""" In order to use different serializers for different 
		actions, you can override the 
	    get_serializer_class(self) method
	"""

	def get_serializer_class(self):
		if self.action in ("create","update","partial_update","destroy"):
			return PostWriteSerializer

		return PostReadSerializer


	def get_permissions(self):
		if self.action in ("create"):
			self.permission_classes = (permissions.IsAuthenticated,)
		elif self.action in ("update","partial_update","destroy"):
			self.permission_classes = (IsAuthorOrReadOnly,)
		else:
			self.permission_classes = (permissions.AllowAny,)

		return super().get_permissions()

class CommentViewSet(viewsets.ModelViewSet):
	 """
    CRUD comments for a particular post
    """
    queryset = Comment.objects.all()

    def get_queryset(self):
    	response = super().get_queryset()
    	post_id = self.kwargs.get("post_id")
    	return response.filter(post_id=post_id)

    def get_serializer_class(self):
    	if self.action in ("create","update","partial_update","destroy"):
    		return 	CommentWriteSerializer
    	return CommentReadSerializer


    def get_permissions(self):
    	if self.action in ("create"):
    		self.permission_classes = (permissions.IsAuthenticated,)

    	elif self.action in ("update","partial_update","destroy"):
    		self.permission_classes = (IsAuthorOrReadOnly)
    	else:
    		self.permission_classes = (permissions.AllowAny,)

    	return super().get_permissions()