from django.contrib import admin
from .models import Survey, Question, Recipient, Response


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ("title", "created_at")


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "survey", "sent_at")
    readonly_fields = ("token",)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("recipient", "question", "rating", "created_at")
