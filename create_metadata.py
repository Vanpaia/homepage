from app import create_app, db
from config import Config

from app.models import ContentType, SectionType, TechnologyType, DevelopmentStatus 
from app.models import Category, Tag, Technology


app = create_app(config_class=Config)

with app.app_context():
    categories = [
            Category(title="Politics", color="#40E0D0", type=ContentType.BLOG),
            Category(title="Technology", color="#E040A0", type=ContentType.BLOG),
            Category(title="Web Development", color="#50E040", type=ContentType.PROJECT),
    ]
    db.session.add_all(categories)
    tags = [
            Tag(title="Privacy"),
            Tag(title="AI"),
            Tag(title="EU"),
    ]
    db.session.add_all(tags)
    technologies = [
        Technology(title="Python 3.12.x", image="img/technology/python.png", type=TechnologyType.LANGUAGE),
        Technology(title="JavaScript 18.19.x", image="img/technology/javascript.png", type=TechnologyType.LANGUAGE),
        Technology(title="Bulma CSS 1.0.x", image="img/technology/bulma.png", type=TechnologyType.FRONTEND),
        Technology(title="Jinja2 3.1.x", image="img/technology/jinja2.png", type=TechnologyType.FRONTEND),
        Technology(title="Flask 3.1.x", image="img/technology/flask.png", type=TechnologyType.BACKEND),
        Technology(title="SQLAlchemy 2.0.x", image="img/technology/sqlalchemy.png", type=TechnologyType.BACKEND),
        Technology(title="Alembic 1.16.x", image="img/technology/alembic.png", type=TechnologyType.BACKEND),
        Technology(title="MariaDB 10.6.x", image="img/technology/mariadb.png", type=TechnologyType.BACKEND),
        Technology(title="Pyright 1.1.x", image="img/technology/pyright.png", type=TechnologyType.DEVOPS),
        Technology(title="nginx 1.18.x", image="img/technology/nginx.png", type=TechnologyType.DEVOPS),
        Technology(title="Gunicorn 20.1.x", image="img/technology/gunicorn.png", type=TechnologyType.DEVOPS)]

    db.session.add_all(technologies)
    db.session.commit()
