from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Member(models.Model):
    name = models.CharField(max_length = 100, null = False)
    password = models.CharField(max_length = 100, null = False)
    phone_number = PhoneNumberField(region = 'KR', unique = True)
    email = models.EmailField(max_length = 254)
    is_public = models.BooleanField(default = True)

    def __str__(self) :
        return self.name
    

class Friend(models.Model):
    sender = models.ForeignKey(Member, related_name = 'sent_friend_requests', on_delete = models.CASCADE)
    receiver = models.ForeignKey(Member, related_name = 'received_friend_requests', on_delete = models.CASCADE)
    friended = models.BooleanField(default = False)
    
    #def __str__(self) :
    #    return self
    

class Diary(models.Model):
    writer = models.ForeignKey(Member, on_delete = models.CASCADE)
    contents = models.TextField(null = False)
    created_date = models.DateTimeField(auto_now = True)

    def __str__(self) :
        return self


class Emotion(models.Model):
    name = models.CharField(max_length = 100, null = False)
    rate = models.IntegerField()
    
    def __str__(self) :
        return self


class Color(models.Model):
    name = models.CharField(max_length = 100, null = False)
    hex = models.CharField(max_length = 100, null = False)
    
    def __str__(self) :
        return self


class Result(models.Model):
    diary = models.ForeignKey(Diary, on_delete = models.CASCADE)
    emotions = models.ForeignKey(Emotion, on_delete = models.CASCADE)
    # emotions는 list로 받아야 하는데 고려해야 하는 사항임
    color = models.ForeignKey(Color, on_delete = models.CASCADE)
    answer = models.TextField(null = False)

    def __str__(self) :
        return self


class Statistic(models.Model):
    results = models.ForeignKey(Emotion, on_delete = models.CASCADE)
    # results는 list로 받아야 하는데 고려해야 하는 사항임
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) :
        return self
    

class Achivement(models.Model):
    requirement = models.IntegerField()
    name = models.CharField(max_length = 100, null = False)
    summary = models.TextField(null = False)

    def __str__(self) :
        return self
    

class Collection(models.Model):
    member = models.ForeignKey(Member, on_delete = models.CASCADE)
    achivement = models.ForeignKey(Achivement, on_delete = models.CASCADE)
    collect_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) :
        return self
    

class Alert(models.Model):
    member = models.ForeignKey(Member, on_delete = models.CASCADE)
    alert_contents = models.TextField(null = False)
    alert_date = models.DateField(auto_now_add = True)