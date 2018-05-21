"""Register your models here."""
from django.contrib import admin
from .models import Tag, Profile, Question, Answer, QTag

admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(QTag)
admin.site.register(Answer)
