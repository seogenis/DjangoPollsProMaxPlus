import datetime
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class ObjectLog(models.Model):
    action_choices = [
        ("CR", "Create"),
        ("M", "Modify"),
        ("D", "Delete"),
    ]
    
    timestamp = models.DateTimeField(auto_now_add=True)
    model_name = models.CharField(max_length=50)
    object_id = models.IntegerField()
    field_name = models.CharField(max_length=50, null=True, default=None)
    action = models.CharField(max_length=32, choices=action_choices)
    previous_value = models.TextField(blank=True, null=True, default=None)
    new_value = models.TextField(blank=True, null=True, default=None)

    def __str__(self):
        return self.action


@receiver(models.signals.post_delete, sender=None)
def _log_model_deletion(sender, instance, using, **kwargs):
    if sender == ObjectLog:
        # Skip if the model is itself an ObjectLog
        return

    ObjectLog.objects.create(
        model_name=instance.__class__.__name__,
        object_id=instance.pk,
        field_name=None,
        action="D",
        new_value=None,
        previous_value=None,
    )