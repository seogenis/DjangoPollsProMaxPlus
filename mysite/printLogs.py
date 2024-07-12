import requests

response = requests.get("http://127.0.0.1:8000/polls/api/logs")
logs = response.json()

for log in logs:
    print(f"ID: {log['id']}")
    print(f"Timestamp: {log['timestamp']}")
    print(f"Model Name: {log['model_name']}")
    print(f"Object ID: {log['object_id']}")
    print(f"Field Name: {log['field_name']}")
    print(f"Previous Value: {log['previous_value']}")
    print(f"New Value: {log['new_value']}")
    print(f"Action: {log['action']}")
    print("-----")