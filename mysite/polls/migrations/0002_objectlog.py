# Generated by Django 5.0.6 on 2024-06-28 15:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ObjectLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("model_name", models.CharField(max_length=50)),
                ("object_id", models.IntegerField()),
                (
                    "field_name",
                    models.CharField(default=None, max_length=50, null=True),
                ),
                (
                    "action",
                    models.CharField(
                        choices=[("CR", "Create"), ("M", "Modify"), ("D", "Delete")],
                        max_length=32,
                    ),
                ),
                (
                    "previous_value",
                    models.TextField(blank=True, default=None, null=True),
                ),
                ("new_value", models.TextField(blank=True, default=None, null=True)),
            ],
        ),
    ]
