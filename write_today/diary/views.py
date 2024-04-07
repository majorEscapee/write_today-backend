from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from .models import Member, Friend, Diary, Emotion, Color, Result, Statistic, Achivement, Collection, Alert
from .serializers import MemberSerializer

# Create your views here.

class FindAllMember(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class FindMember(generics.CreateAPIView):
    queryset = Member.objects