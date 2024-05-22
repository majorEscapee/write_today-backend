from rest_framework import serializers
from .models import Member, Friend, Diary, Emotion, Color, Result, Statistic, Achivement, Collection, Alert, MixedEmotion

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

    # fields = [''] = 포함할 필드 기입
    # fields = '__all__' = 전체 필드 포함
    # exclude = [''] = 제외할 필드 기입

class MemberDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name', 'email', 'is_public']

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['email', 'password']

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = '__all__'

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = '__all__'

class FriendSerializer(serializers.ModelSerializer):
    sender = MemberSerializer()
    receiver = MemberSerializer()

    class Meta:
        model = Friend
        fields = '__all__'

class AchivementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achivement
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'

class MixedEmotionSerializer(serializers.ModelSerializer):
    emotions = EmotionSerializer(many = True)

    class Meta:
        model = MixedEmotion
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    diary = DiarySerializer()
    color = ColorSerializer()
    mixed_emotion = MixedEmotionSerializer(many = True)
    
    class Meta:
        model = Result
        fields = '__all__'


# Swagger Test Serializer

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['email', 'password']

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(help_text="비밀번호")
    new_password = serializers.CharField(help_text="새 비밀번호")

class FriendRequestSerializer(serializers.Serializer):
    receiver_email = serializers.CharField(help_text="상대방 이메일")

class FriendAcceptSerializer(serializers.Serializer):
    friend_id = serializers.CharField(help_text="친구 id")