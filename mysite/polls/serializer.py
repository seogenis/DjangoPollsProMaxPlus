from rest_framework import serializers
from .models import Choice, Question

class LoggedModelSerializer(serializers.ModelSerializer):
    # TODO: FILL IN, TRACK ALL CHANGES THAT HAPPEN TO THE MODEL
    
    def create(self, validated_data):
        # TODO: FILL IN, 
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # TODO: FILL IN, 
        return super().update(instance, validated_data)

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id','question', 'choice_text', 'votes']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','question_text', 'pub_date']