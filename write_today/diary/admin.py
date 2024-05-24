from django.contrib import admin
from diary.models import Member, Friend, Diary, Emotion, Result, Statistic, Achievement, Collection, Alert

# Register your models here.
admin.site.register(Member)
admin.site.register(Friend)
admin.site.register(Diary)
admin.site.register(Emotion)
# admin.site.register(Color)
admin.site.register(Result)
admin.site.register(Statistic)
admin.site.register(Achievement)
admin.site.register(Collection)
admin.site.register(Alert)

admin.ModelAdmin.search_fields = ('email',)