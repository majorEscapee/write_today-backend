from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Member(models.Model):
    name = models.CharField(max_length = 100, null = False)
    password = models.CharField(max_length = 100, null = False)
    phone_number = PhoneNumberField(region = 'KR', unique = True)
    email = models.EmailField(max_length = 254)
    is_public = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now_add = True)

    def __str__(self) :
        return self.name + " / " + self.email
    

class Friend(models.Model):
    sender = models.ForeignKey(Member, related_name = 'sent_friend_requests', on_delete = models.CASCADE)
    receiver = models.ForeignKey(Member, related_name = 'received_friend_requests', on_delete = models.CASCADE)
    friended = models.BooleanField(default = False)
    
    def __str__(self) :
        return self.sender.name + " + " + self.receiver.name
    

class Diary(models.Model):
    writer = models.ForeignKey(Member, on_delete = models.CASCADE)
    contents = models.TextField(null = False)
    created_date = models.DateTimeField(auto_now = True)

    def __str__(self) :
        return self.writer.name + " / " + self.created_date.strftime("%Y년 %m월 %d일 %H시 %M분")


class Emotion(models.Model):
    name = models.CharField(max_length = 100, null = False)
    rate = models.IntegerField()
    
    def __str__(self) :
        return self.name + str(self.rate)


class Color(models.Model):
    name = models.CharField(max_length = 100, null = False)
    hex = models.CharField(max_length = 100, null = False)
    
    def __str__(self) :
        return self.name


class Statistic(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) :
        return str(self.start_date) + " ~ " + str(self.end_date)


class Result(models.Model):
    diary = models.OneToOneField(Diary, on_delete = models.CASCADE)
    emotions = models.ManyToManyField(Emotion) # 다대다로 변경
    color = models.OneToOneField(Color, on_delete = models.SET_NULL, null=True)
    answer = models.TextField(null = False)
    statistic = models.ForeignKey(Statistic, on_delete = models.CASCADE, related_name="results")

    def __str__(self) :
        return self.diary.writer.name + " / " +  self.diary.created_date.strftime("%Y년 %m월 %d일 %H시 %M분") + " / 결과"


class Achivement(models.Model):
    requirement = models.IntegerField()
    name = models.CharField(max_length = 100, null = False)
    summary = models.TextField(null = False)

    #def __str__(self) :
    #    return self
    

class Collection(models.Model):
    member = models.ForeignKey(Member, on_delete = models.CASCADE)
    achivement = models.ForeignKey(Achivement, on_delete = models.CASCADE)
    collect_date = models.DateField()
    end_date = models.DateField()

    #def __str__(self) :
    #    return self
    

class Alert(models.Model):
    member = models.ForeignKey(Member, on_delete = models.CASCADE)
    alert_contents = models.TextField(null = False)
    alert_date = models.DateField(auto_now_add = True)