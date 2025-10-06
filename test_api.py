import requests
from config import SECRET_KEY

BASE_URL = "http://localhost:5000/api"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": SECRET_KEY
}

# 1. Create project
project_data = {
    "title": "Task Manager App8",
    "subtitle": "A simple task tracking application",
    "extract": "Built with Flask and PostgreSQL",
    "slug": "task-manager-8",
    "features": [
        {"title": "User authentication", "status": "completed", "order": 0},
        {"title": "Task CRUD", "status": "in_progress", "order": 1},
        {"title": "Categories", "status": "planned", "order": 2}
    ],
    "sections": [
        {
            "type": "overview",
            "title": "About",
            "body": "A task management app...",
            "order": 0
        }
    ]
}

response = requests.post(f"{BASE_URL}/projects", json=project_data, headers=headers)
print(response.json())
project_id = response.json()['id']
print(f"Created project {project_id}")

# 2. Add another feature
new_feature = {
    "title": "Due dates",
    "status": "planned",
    "order": 3
}
response = requests.post(
    f"{BASE_URL}/projects/{project_id}/features",
    json=new_feature,
    headers=headers
)
print(response.json())
feature_id = response.json()['id']
print(f"Added feature {feature_id}")

# 3. Mark a feature as completed
requests.patch(
    f"{BASE_URL}/projects/{project_id}/features/2",
    json={"status": "completed"},
    headers=headers
)
print("Updated feature status")

# 4. Add a new section
new_section = {
    "type": "implementation_details",
    "title": None,  # No title needed
    "body": "Technical details about the implementation...",
    "icon": None,
    "order": 1
}
requests.post(
    f"{BASE_URL}/projects/{project_id}/sections",
    json=new_section,
    headers=headers
)
print("Added section")

