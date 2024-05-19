from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

from .models import Member, Friend, Diary, Emotion, Color, Result, Statistic, Achivement, Collection, Alert
from .serializers import MemberSerializer, MemberTestSerializer, DiarySerializer, ResultSerializer


class SignUp(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberTestSerializer
    # 이메일 인증, 소셜 회원가입 등 추가 필요

    # def post(self, request, format=None):
    #     serializer = MemberDataSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=201)

class Login(generics.CreateAPIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalid credentials"}, status=400)

class Logout(generics.GenericAPIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"})

class MemberList(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberDetail(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = "email"

class DiaryList(generics.ListAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    lookup_field = "email"
    # 추후에 pk로 변경 가능

class DiaryDetail(generics.RetrieveUpdateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer

class WriteDiary(generics.CreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    # + 결과 추가 관련

class ResultDetail(generics.RetrieveAPIView):
    queryset = Result.objects.select_related("diary").all()
    serializer_class = ResultSerializer
    # 일기 상세 조회 = 결과도 조회