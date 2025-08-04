from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework import generics

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# BookViewSet is secured with Token Authentication.
# Only authenticated users can access CRUD operations via this view.

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # <– Restricts access to authenticated users only
