import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save
from django.utils import timezone
from django.contrib import admin
from .middleware import get_current_user


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


from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

@receiver(pre_save, sender=Choice)
@receiver(pre_save, sender=Question)
def log_model_changes(sender, instance, **kwargs):
    user = get_current_user()
    if instance.pk:
        previous_instance = sender.objects.get(pk=instance.pk)
        for field in instance._meta.fields:
            field_name = field.name
            new_value = getattr(instance, field_name)
            previous_value = getattr(previous_instance, field_name)
            if new_value != previous_value:
                ObjectLog.objects.create(
                    model_name=instance.__class__.__name__,
                    object_id=str(instance.pk),
                    field_name=field_name,
                    action="M",
                    previous_value=str(previous_value),
                    new_value=str(new_value),
                    username=user.username if user and user.is_authenticated else 'Anonymous'
                )

@receiver(post_save, sender=Choice)
@receiver(post_save, sender=Question)
def log_model_creation(sender, instance, created, **kwargs):
    user = get_current_user()
    if created:
        ObjectLog.objects.create(
            model_name=instance.__class__.__name__,
            object_id=str(instance.pk),
            field_name=None,
            action="CR",
            new_value=None,
            previous_value=None,
            username=user.username if user and user.is_authenticated else 'Anonymous'
        )

@receiver(post_delete, sender=Choice)
@receiver(post_delete, sender=Question)
def log_model_deletion(sender, instance, **kwargs):
    user = get_current_user()
    ObjectLog.objects.create(
        model_name=instance.__class__.__name__,
        object_id=str(instance.pk),
        field_name=None,
        action="D",
        new_value=None,
        previous_value=None,
        username=user.username if user and user.is_authenticated else 'Anonymous'
    )