from django.db import models

# Create your models here.
class Member(models.model):
    name = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    phone_number = models.PhoneNumberField(region = 'KR', unique = True)
    email = models.EmailField(max_length=254)
    is_public = models.BooleanField(default = True)

    def __str__(self) :
        return self