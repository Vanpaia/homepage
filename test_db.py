from app import create_app, db
from config import Config

from app.models import ContentType, SectionType, TechnologyType, DevelopmentStatus 
from app.models import Category, Tag, Technology, Project


app = create_app(config_class=Config)

with app.app_context():
    deployed_projects = Project.get_deployed()
    for x in deployed_projects:
        print(x.title)
