from django.shortcuts import render

# Create your views here.
from tutor.models import *
from tutor.serializers import TutorSerializer

from rest_framework import viewsets
class TutorViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = TutorSerializer