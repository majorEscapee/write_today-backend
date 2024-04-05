from django.shortcuts import render
from rest_framework import generics
from .models import Member, Friend, Diary, Emotion, Color, Result, Statistic, Achivement, Collection, Alert
from .serializers import MemberSerializer

# Create your views here.

class ListMember(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer