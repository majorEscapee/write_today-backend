from rest_framework import serializers
from .models import Member, Friend, Diary, Emotion, Color, Result, Statistic, Achivement, Collection, Alert

# API 요청의 반환값을 JSON으로 직렬화하기 위함

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        
        #fields = [''] = 포함할 필드 기입
        # fields = '__all__' = 전체 필드 포함
        # exclude = [''] = 제외할 필드 기입
