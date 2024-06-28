import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from polls.models import ObjectLog

# Query all ObjectLog entries
logs = ObjectLog.objects.all()

# Print each attribute of the ObjectLog entries
for log in logs:
    print(f"ID: {log.id}")
    print(f"Timestamp: {log.timestamp}")
    print(f"Model Name: {log.model_name}")
    print(f"Object ID: {log.object_id}")
    print(f"Field Name: {log.field_name}")
    print(f"Previous Value: {log.previous_value}")
    print(f"New Value: {log.new_value}")
    print(f"Action: {log.action}")
    print("-----")
