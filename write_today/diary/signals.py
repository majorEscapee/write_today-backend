from django.dispatch import receiver
from .models import Achievement, Collection, Member
from django.db.models.signals import post_save

@receiver(post_save, sender = Member)
def achv_join(sender, instance, created, **kwargs):
    if created:
        achievement = Achievement.objects.get('')
        Collection.objects.create(user=instance, achievement=achievement)