from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Member, Friend, Diary, Emotion, Result, Statistic, Achievement, Collection, Alert, UserManager
from .serializers import MemberSerializer, LoginSerializer, DiarySerializer, ResultSerializer, SignUpSerializer, FriendSerializer, FriendRequestSerializer, FriendAcceptSerializer, ChangePasswordSerializer, DiaryResultSerializer, DiaryListSerializer 

def admin_check(user):
    if not user.is_staff:
        return Response({"error": "관리자 권한 없음."}, status=403)
    
def superuser_check(user):
    if not user.is_superuser:
        return Response({"error": "관리자 권한 없음."}, status=403)
    
def validate_token(user):
    if not isinstance(user, Member):  # 유저가 인증된 경우
        return Response({"error": "회원 검증 실패."}, status=401)
    
def diary_result(diary):
    diary.contents
    emotions = 1
    result = 1
    """ LangChain 결과 받아오기 """
    return emotions, result

class ManageAchivement():
    def achivement_check(self):
        return 0

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
            return Response({"error": "비밀번호 확인이 일치하지 않음."}, status=400)

        try:
            user = Member.objects.create_user(email=email, name=name, phone_number=phone_number, password=password)
            user.save()
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        return Response({"message": "회원가입 성공.", "user": MemberSerializer(user).data}, status=201)

class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        
        if not user.is_active:
            return Response({"error": "탈퇴된 회원."}, status=401)
        
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=201)
        else:
            return Response({"error": "로그인 실패."}, status=401)

class Logout(generics.GenericAPIView):
    swagger_schema = None
    
    def post(self, request):
        logout(request)
        # 토큰 만료시키기
        token = Token.objects.filter(key = request.auth)
        token.delete()
        return Response({"message": "로그아웃 성공."}, status=200)
    
class TokenTest(generics.GenericAPIView):
    swagger_schema = None
    permission_classes = [IsAuthenticated] # 토큰 인증 필요

    def get(self, request):
        user = request.user
        validate_token(user)
        user_data = {
            "name": user.name,
            "email": user.email,
            # 필요한 다른 사용자 정보 추가 가능
        }
        return Response(user_data, status=200)

""" 임시 """   
class MemberList(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberDetailEmail(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = "email"

""" """   

class MemberDetail(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer

    def get(self, request):
        user = request.user
        validate_token(user)
        serializer = self.get_serializer(user) # JSON으로 직렬화
        return Response(serializer.data, status=200)

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
                return Response({"error": "존재하지 않는 회원."}, status=404)
        else:
            return Response({"error": "이메일 누락."}, status=400)

class ChangeMemberState(generics.GenericAPIView):
    swagger_schema = None
    permission_classes = [IsAuthenticated] # 토큰 인증 필요

    def put(self, request):
        user = request.user
        validate_token(user)
        state = user.is_public
        user.is_public = not state
        user.save()
        return Response({"message : " : "상태 변경 성공 / " + str(not state)}, status=200)

class ChangePassword(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        user = request.user
        password = request.data.get("password")
        new_password = request.data.get("new_password")
        user = authenticate(email=user.email, password=password)
        validate_token(user)
        user = Member.objects.change_password(user, new_password)
        user.save()
        return Response({"message : " : "비밀번호 변경 성공."}, status=200)


class MemberQuit(generics.GenericAPIView):
    swagger_schema = None
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user

        validate_token(user)
        user.is_active = False
        user.save()
        logout(request)
        return Response({"message": "회원 탈퇴 성공."}, status=200)
        

class RequestFriend(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def post(self, request):
        user = request.user
        validate_token(user)
        receiver_email = request.data.get("receiver_email")
        target = Member.objects.filter(email=receiver_email).first()
        if isinstance(target, Member):
            if Friend.objects.filter(sender=user, receiver=target).exists() | Friend.objects.filter(sender=target, receiver=user).exists():
                return Response({"error": "이미 친구 관계가 존재함."}, status=400)
            friend = Friend.objects.create(
                sender=user,
                receiver=target,
                friended=False
            )
            friend.save()
            return Response({"message": "친구 요청 성공."}, status=201)
        else:
            return Response({"error": "상대방 회원 정보가 존재하지 않음."}, status=400)


class AcceptFriend(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendAcceptSerializer

    def put(self, request):
        user = request.user
        validate_token(user)
        friend_id = request.data.get("friend_id")
        friend = Friend.objects.filter(id=friend_id).first()
        if isinstance(friend, Friend):
            if friend.friended:
                return Response({"error": "이미 친구 관계임."}, status=400)
            friend.friended = True
            friend.save()
            return Response({"message": "친구 요청 수락 성공."}, status=200)
        else:
            return Response({"error": "친구 신청 정보 존재하지 않음."}, status=400)


    def delete(self, request):
        user = request.user
        validate_token(user)
        friend_id = request.data.get("friend_id")
        friend = Friend.objects.filter(id=friend_id).first()
        if isinstance(friend, Friend):
            if friend.friended:
                friend.delete()
                return Response({"message": "친구 삭제 성공."}, status=200)
            else:
                friend.delete()
                return Response({"message": "친구 요청 거절 성공."}, status=200)
        else:
            return Response({"error": "친구 신청 정보 존재하지 않음."}, status=400)


class FriendList(generics.GenericAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        validate_token(user)
        friends = Friend.objects.filter(sender = user) | Friend.objects.filter(receiver = user)
        if friends:
            serializer = self.get_serializer(friends, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"error": "친구 정보 존재하지 않음."}, status=400)


class DiaryList(generics.ListAPIView):
    serializer_class = DiaryListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        validate_token(user)
        diarys = Diary.objects.filter(writer = user)
        if diarys:
            serializer = self.get_serializer(diarys, many = True)
            return Response(serializer.data, status=200)
        else:
            return Response({"error": "일기 정보 존재하지 않음."}, status=400)

class DiaryDetail(generics.GenericAPIView):
    serializer_class = DiaryResultSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        validate_token(user)
        created_date = datetime.strptime(request.query_params.get("created_date"), '%Y-%m-%d').date()
        diary = Diary.objects.filter(writer = user, created_date = created_date).first()
        if isinstance(diary, Diary):
            serializer = self.get_serializer(diary)
            return Response(serializer.data, status=200)
        else:
            return Response({"error": "일기 정보 존재하지 않음."}, status=400)
        

# class WriteDiary(generics.CreateAPIView):
#     queryset = Diary.objects.all()
#     serializer_class = DiarySerializer
#     + 결과 추가 관련

class WriteDiary(generics.CreateAPIView):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        validate_token(user)
        contents = request.data.get("contents")
        # 2024-05-24의 형식
        created_date = datetime.strptime(request.data.get("created_date"), '%Y-%m-%d').date()
        nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
        if (created_date > nowDate) :
            return Response({"error": "미래 일기 작성 불가능."}, status=400)
        diary = Diary.objects.create(writer = user, contents = contents, created_date = created_date)  
        diary.save()
        serializer = self.get_serializer(diary)
        # diary_result(1) > 결과 받아오기
        return Response(serializer.data, status=201)
    
    def put(self, request):
        user = request.user
        validate_token(user)
        contents = request.data.get("contents")
        # 2024-05-24의 형식
        created_date = datetime.strptime(request.data.get("created_date"), '%Y-%m-%d').date()
        nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
        if (created_date > nowDate) :
            return Response({"error": "미래 일기 작성 불가능."}, status=400)
        diary = Diary.objects.get_or_create(writer = user, created_date = created_date)
        diary.contents = contents
        diary.save()
        serializer = self.get_serializer(diary)
        # diary_result(1) > 결과 받아오기
        return Response(serializer.data, status=201)

class ResultDetail(generics.RetrieveAPIView):
    queryset = Result.objects.select_related("diary").all()
    serializer_class = ResultSerializer
    # 일기 상세 조회 = 결과도 조회
    """
    만약 결과를 조회하는데 같은 날짜에 일기는 존재하고 결과는 존재하지 않다면 즉시 재요청하기
    """

""" 컬렉션 관련 로직 """
""" 알림 관련 로직 """


        # user_data = {
        #     "name": user.name,
        #     "email": user.email,
        #     # 필요한 다른 사용자 정보 추가 가능
        # }