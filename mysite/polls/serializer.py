from rest_framework import serializers
from .models import Choice, Question, ObjectLog


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id','question', 'choice_text', 'votes']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','question_text', 'pub_date']

class ObjectLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectLog
        fields = ['id', 'timestamp', 'model_name', 'object_id', 'field_name', 'action', 'previous_value', 'new_value', 'username']