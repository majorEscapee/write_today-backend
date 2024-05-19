from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.SignUp.as_view()),
    path('login', views.Login.as_view()),
    path('logout', views.Logout.as_view()),
    path('members', views.MemberList.as_view()),
    path('member/<email>', views.MemberDetail.as_view()),
    path('diarys/<email>', views.DiaryList.as_view()),
    path('diary/<pk>', views.DiaryDetail.as_view()),
    path('write', views.WriteDiary.as_view()),
    path('result/<pk>', views.ResultDetail.as_view()),
]