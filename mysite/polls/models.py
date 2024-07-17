import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
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
    
    def delete(self, using=None, keep_parents=False):
        # Pass the user context to each related Choice instance before deleting them
        for choice in self.choice_set.all():
            choice._request_user = self._request_user
            choice.delete()
        super().delete(using, keep_parents)

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
    object_id = models.CharField(max_length=50)
    field_name = models.CharField(max_length=50, null=True, default=None)
    action = models.CharField(max_length=32, choices=action_choices)
    previous_value = models.TextField(blank=True, null=True, default=None)
    new_value = models.TextField(blank=True, null=True, default=None)
    username = models.CharField(max_length=150, null=True, default=None)  # Add this field


    def __str__(self):
        return (self.username if self.username != None else "No Username") + " " + self.action + " " + str(self.timestamp)


@receiver(post_delete, sender=Choice)
@receiver(post_delete, sender=Question)
def log_model_deletion(sender, instance, using, **kwargs):
    user = instance._request_user if hasattr(instance, '_request_user') else None
    ObjectLog.objects.create(
        model_name=instance.__class__.__name__,
        object_id=str(instance.pk),
        field_name=None,
        action="D",
        new_value=None,
        previous_value=None,
        username=user.username if user and user.is_authenticated else 'Anonymous'
    )