# Register your models here. - allow admin page to edit polls' questions data
from django.contrib import admin
from .models import Question, Choice

class ChoiceAdmin(admin.TabularInline):
    model = Choice
    extra = 3

    def save_model(self, request, obj, form, change):
        obj._request_user = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj._request_user = request.user
        super().delete_model(request, obj)

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceAdmin]
    list_display = ["question_text", "pub_date", "was_published_recently"]

    list_filter = ["pub_date"]

    def save_model(self, request, obj, form, change):
        obj._request_user = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj._request_user = request.user
        super().delete_model(request, obj)



admin.site.register(Question, QuestionAdmin)