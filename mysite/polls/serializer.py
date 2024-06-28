from rest_framework import serializers
from .models import Choice, Question, ObjectLog

class LoggedModelSerializer(serializers.ModelSerializer):
    # TODO: FILL IN, TRACK ALL CHANGES THAT HAPPEN TO THE MODEL
    
    def create(self, validated_data):
        instance = super().create(validated_data)
        ObjectLog.objects.create(
            model_name=instance.__class__.__name__,
            object_id=instance.pk,
            field_name=None,
            action="CR",
            new_value=None,
            previous_value=None,
        )
        return instance

    def update(self, instance, validated_data):
        previous_instance = self.Meta.model.objects.get(pk=instance.pk)
        new_instance = super().update(instance, validated_data)
        
        for field, value in validated_data.items():
            new_value = getattr(new_instance, field)
            previous_value = getattr(previous_instance, field)
            if new_value != previous_value:
                ObjectLog.objects.create(
                    model_name=instance.__class__.__name__,
                    object_id=instance.pk,
                    field_name=field,
                    action="M",
                    previous_value=str(previous_value),
                    new_value=str(new_value),
                )

        return new_instance

class ChoiceSerializer(LoggedModelSerializer):
    class Meta:
        model = Choice
        fields = ['id','question', 'choice_text', 'votes']

class QuestionSerializer(LoggedModelSerializer):
    class Meta:
        model = Question
        fields = ['id','question_text', 'pub_date']