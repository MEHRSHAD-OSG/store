from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'email', 'creation']


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'created']
    list_select_related = True
    list_display_links = ('user',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(models.Answer)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'question', 'body', 'created']
    raw_id_fields = ['question']
