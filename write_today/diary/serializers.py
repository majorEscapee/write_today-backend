from rest_framework import serializers
from .models import Member, Friend, Diary, Emotion, Result, Statistic, Achievement, Collection, Alert, MixedEmotion

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

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = '__all__'

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['name', 'hex']

# class ColorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Color
#         fields = '__all__'

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

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
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
    emotion = EmotionSerializer()

    class Meta:
        model = MixedEmotion
        fields = ['emotion', 'rate']

class ResultSerializer(serializers.ModelSerializer):
    diary = DiarySerializer()
    emotions = EmotionSerializer(many = True)
    
    class Meta:
        model = Result
        fields = '__all__'

""" custom serializer """

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['email', 'password']

class ResultDataSerializer(serializers.ModelSerializer):
    mixed_emotion = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = ['id', 'mixed_emotion', 'answer']

    def get_mixed_emotion(self, obj):
        mixed_emotions = MixedEmotion.objects.filter(result=obj)
        return MixedEmotionSerializer(mixed_emotions, many=True).data

class DiaryResultSerializer(serializers.ModelSerializer):
    result = ResultDataSerializer()
    
    class Meta:
        model = Diary
        fields = '__all__'


class DiaryListSerializer(serializers.ModelSerializer):
    hex = serializers.SerializerMethodField()

    class Meta:
        model = Diary
        fields = ['id', 'created_date', 'hex']

    def get_hex(self, obj):
        result = Result.objects.filter(diary=obj).first()
        if result:
            mixed_emotion = MixedEmotion.objects.filter(result=result).order_by('-rate').first()
            if mixed_emotion:
                return mixed_emotion.emotion.hex
        return None



""" Swagger Test Serializer """


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