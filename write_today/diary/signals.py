from django.dispatch import receiver
from .models import Achievement, Collection, Member, Diary
from django.db.models.signals import post_save

@receiver(post_save, sender = Member)
def achv_join(sender, instance, created, **kwargs):
    if created:
        achievement = Achievement.objects.get('')
        Collection.objects.create(user=instance, achievement=achievement)

@receiver(post_save, sender = Diary)
def create_result(sender, instance, created, **kwargs):
    if created:
        # 결과 세팅하기
        Achievement.objects.create()