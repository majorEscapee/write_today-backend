from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Member, Friend, Diary, Emotion, Color, Result, Statistic, Achivement, Collection, Alert, UserManager
from .serializers import MemberSerializer, LoginSerializer, DiarySerializer, ResultSerializer, SignUpSerializer


class SignUp(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    def post(self, request):
        email = request.data.get("email")
        name = request.data.get("name")
        password = request.data.get("password")
        password_check = request.data.get("password_check")
        phone_number = request.data.get("phone_number")

        # 휴대폰 인증 OR 이메일 인증 추가할 것?

        if password != password_check:
            return Response({"error": "password_check is not correct"}, status=400)

        try:
            user = Member.objects.create_user(email=email, name=name, phone_number=phone_number, password=password)
            user.save()
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        return Response({"msg": "User created successfully", "user": MemberSerializer(user).data}, status=201)

class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=201)
        else:
            return Response({"error": "Invalid credentials"}, status=400)

class Logout(generics.GenericAPIView):
    swagger_schema = None
    
    def post(self, request):
        logout(request)
        # 토큰 만료시키기
        token = Token.objects.filter(key = request.auth)
        token.delete()
        return Response({"message": "Successfully logged out"}, status=201)
    
class TokenTest(generics.GenericAPIView):
    permission_classes = [IsAuthenticated] # 토큰 인증 필요

    def get(self, request):
        user = request.user
        # 헤더에 Key : Authorization / Value : Token 토큰값
        if isinstance(user, Member):  # 유저가 인증된 경우
            user_data = {
                "name": user.name,
                "email": user.email,
                # 필요한 다른 사용자 정보 추가 가능
            }
            return Response(user_data, status=200)
        else:  # 익명 사용자인 경우
            return Response({"error": "User is not authenticated"}, status=401)
        
class MemberList(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberDetail(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer

    def get(self, request):
        user = request.user
        if isinstance(user, Member):
            serializer = self.get_serializer(user) # JSON으로 직렬화
            return Response(serializer.data, status=200)
        else:
            return Response({"error": "User is not authenticated"}, status=401)

class MemberDetailEmail(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = "email"

class MemberExist(generics.GenericAPIView):
    serializer_class = MemberSerializer

    def get(self, request):
        email = request.query_params.get('email')
        if email:
            user = Member.objects.filter(email=email).first()
            if user:
                serializer = self.get_serializer(user)
                return Response(serializer.data, status=200)
            else:
                return Response({"error": "Member does not exist"}, status=404)
        else:
            return Response({"error": "Email parameter is required"}, status=400)

class ChangeMemberState(generics.GenericAPIView):
    permission_classes = [IsAuthenticated] # 토큰 인증 필요

    def put(self, request):
        user = request.user
        if user:
            state = user.is_public
            user.is_public = not state
            user.save()
            return Response({"Successfully changed state : " : not state}, status=200)
        else:
            return Response({"error": "Change State Err"}, status=401)

class ChangePassword(generics.GenericAPIView):
    permission_classes = [IsAuthenticated] # 토큰 인증 필요

    def put(self, request):
        user = request.user
        password = request.data.get("password")
        new_password = request.data.get("new_password")
        user = authenticate(email=user.email, password=password)
        if user:
            user = Member.objects.change_password(user, new_password)
            user.save()
            return Response({"Successfully changed password"}, status=200)
        else:
            return Response({"error": "Change PW failed"}, status=401)


class MemberQuit(generics.GenericAPIView):
    # 회원 탈퇴
    permission_classes = [IsAuthenticated] # 토큰 인증 필요

    def put(self, request):
        logout(request)
        user = request.user

        if isinstance(user, Member):
            user.is_active = False
            user.save()
            return Response({"message": "Successfully withdrawn from membership"}, status=200)
        
        else:
            return Response({"error": "User not found"}, status=404)
        
        
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