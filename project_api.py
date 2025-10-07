import requests
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
SECRET_KEY = os.getenv("SECRET_KEY")
BASE_URL = "https://hagen.social/api"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": SECRET_KEY
}

# 1. Create project
project_data = {
    "title": "NOS Archive",
    "subtitle": "Creating a searchable archive and API of the Dutch public broadcaster NOS",
    "extract": "The NOS has changed its search and archive as to be barely usable, so I created better search and a public accessible API.",
    "status": "completed",
    "featured_order": "0",
    "deployment_url": "https://media.insight-democracy.com/",
    "github_url": "https://github.com/Vanpaia/nos_archief",
    "slug": "NOS-archive",
    "features": [
        {"title": "Historic data until 2010", "status": "completed", "order": 0},
        {"title": "Automatic data ingestion", "status": "completed", "order": 1},
        {"title": "Categorisation & labeling", "status": "completed", "order": 2},
        {"title": "Implement search engine", "status": "completed", "order": 3},
        {"title": "Day/Week/Month archive", "status": "completed", "order": 4},
        {"title": "AI summarisations", "status": "completed", "order": 5},
        {"title": "Public rate-limited API", "status": "completed", "order": 6},
    ],
    "sections": [
        {
            "type": "overview",
            "title": "About",
            "body": "Until 2024, the NOS had a great archive. You could choose a date in a category and see what happened on that day. At the end of 2023, the NOS announced that old articles would only be accessible by their search function. The only problem is that this search function is terrible. You cannot filter by date or category. If you are looking for a topic that has several articles about it, it is like looking for a needle in a haystack.\nUsing the things I've learned in my first (failed) project, I scraped the Internet Archive's Wayback Machine until 2010 and categorised and indexed all articles I could get until 2010. Additionally, I am ingesting rich data going forward from June 2024.\nTo make it more useful than it was even before, I added variable archive windows (day/week/month) and categories, AI summarisation, search, and a public API.",
        },
        {
            "type": "project_goals",
            "title": "Learning Objectives",
            "body": "- SQL and NoSQL databases\n- Big data refinement\n- API setup",
            "order": 1
        },
        {
            "type": "project_goals",
            "title": "Practical Objectives",
            "body": "- Better search NOS articles\n- Public API to search articles\n- Recreate and improve archive function",
            "order": 2
        },
        {
            "type": "implementation_details",
            "title": "Backend Architecture",
            "body": "Built with Flask framework using blueprints for modular design. Implements SQLAlchemy ORM for database operations with migration support via Alembic.",
            "icon": "fas fa-3x fa-server",
            "order": 1
        },
        {
            "type": "implementation_details",
            "title": "Frontend Design",
            "body": "Responsive UI built with Bootstrap CSS framework. Jinja2 templates provide server-side rendering with minimal JavaScript for enhanced interactions.",
            "icon": "fas fa-3x fa-palette",
            "order": 2
        },
        {
            "type": "implementation_details",
            "title": "Deployment Infrastructure",
            "body": "Deployment on a VPS served with the Gunicorn HTTP server and routed with NGINX. Data is served throught a MySQL instance coupled with Elasticsearch.",
            "icon": "fas fa-3x fa-sitemap",
            "order": 3
        },
    ],
    "technologies": [
        {"title": "Python 3.11.x", "type": "language", "image": "img/technology/python.png", "order": 1},
        {"title": "JavaScript (ES2021)", "type": "language", "image": "img/technology/js.png", "order": 2},
        {"title": "Flask 3.1.x", "type": "backend", "image": "", "order": 1},
        {"title": "SQLAlchemy 2.0.x", "type": "backend", "image": "", "order": 3},
        {"title": "Alembic 1.16.x", "type": "backend", "image": "", "order": 4},
        {"title": "MySQL 8.0.x", "type": "backend", "image": "img/technology/mysql.png", "order": 2},
        {"title": "Elasticsearch 8.10.x", "type": "backend", "image": "img/technology/elasticsearch.png", "order": 2},
        {"title": "Bootstrap 4.0.x", "type": "frontend", "image": "img/technology/bootstrap.png", "order": 1},
        {"title": "Jinja2 3.1.x", "type": "frontend", "image": "", "order": 2},
        {"title": "nginx 1.18.x", "type": "devops", "image": "", "order": 2},
        {"title": "Gunicorn 20.1.x", "type": "devops", "image": "", "order": 3},
    ],
}

response = requests.post(f"{BASE_URL}/projects", json=project_data, headers=headers)
print(response)
project_id = response.json()['id']
print(f"Created project {project_id}")


"""
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
"""
