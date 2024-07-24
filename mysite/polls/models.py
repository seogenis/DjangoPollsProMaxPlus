import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save
from django.utils import timezone
from django.contrib import admin
from .middleware import get_current_user

class LoggedModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        username = user.username if user and user.is_authenticated else 'Anonymous'
        
        # Determine if the object is new
        is_new = self.pk is None 
        if not is_new:
            old_instance = self.__class__.objects.get(pk=self.pk)

        super().save(*args, **kwargs)
        
        if is_new:
            # Create 
            ObjectLog.objects.create(
                model_name=self.__class__.__name__,
                object_id=str(self.pk),
                field_name=None,
                action="CR",
                new_value=None,
                previous_value=None,
                username=username
            )
        else:
            # Update 
            for field in self._meta.fields:
                old_value = getattr(old_instance, field.name)
                new_value = getattr(self, field.name)
                if old_value != new_value:
                    ObjectLog.objects.create(
                        model_name=self.__class__.__name__,
                        object_id=str(self.pk),
                        field_name=field.name,
                        action="M",
                        previous_value=str(old_value),
                        new_value=str(new_value),
                        username=username
                    )

    # Delete
    def delete(self, *args, **kwargs):
        user = get_current_user()
        username = user.username if user and user.is_authenticated else 'Anonymous'
        
        ObjectLog.objects.create(
            model_name=self.__class__.__name__,
            object_id=str(self.pk),
            field_name=None,
            action="D",
            new_value=None,
            previous_value=None,
            username=username
        )
        
        super().delete(*args, **kwargs)


class Question(LoggedModel):
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
    
    # Delete choices along with question
    def delete(self, using=None, keep_parents=False):
        for choice in self.choice_set.all():
            choice._request_user = self._request_user
            choice.delete()
        super().delete(using, keep_parents)

class Choice(LoggedModel):
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

