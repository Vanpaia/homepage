from app import create_app, db
from config import Config

from app.models import DevelopmentStatus, SectionType, TechnologyType
from app.models import Project, ProjectFeature, ProjectSection, Technology
app = create_app(config_class=Config)
with app.app_context():
    feature1 = ProjectFeature(title="Dynamically populated personal blog", status=DevelopmentStatus.COMPLETED, order=1)
    feature2 = ProjectFeature(title="Dynamically populated project portfolio", status=DevelopmentStatus.COMPLETED, order=2) 
    feature3 = ProjectFeature(title="Category, tags, and technologies tagging system", status=DevelopmentStatus.COMPLETED, order=3) 
    feature4 = ProjectFeature(title="Landing Page", status=DevelopmentStatus.PLANNED, order=4) 
    overview = ProjectSection(type=SectionType.OVERVIEW, body="""
This project implements a unified landing page for my server. It is meant to provide easier access to several web application deployed on hagen.social sub-domains. Additionally, I wanted to create an overview for myself of finished, ongoing, and planned personal projects, to maintain an overview of what I have done and what I plan to do. This will be made in such a way to also serve as a portfolio for myself. Finally, I am adding a personal blog to share thoughts and articles within my network. 

At the same time, I am using this opportunity to try an alternative CSS framework to Bootstrap, which I have most experience with. I decided to try my hand with the [Bulma CSS](https://bulma.io/) framework.""")
    learning_goals = ProjectSection(type=SectionType.GOALS, title="Learning Objectives", body="""
- Implement secure Basic Authentication for REST API access.
- Learn the use of the Bulma CSS framework.
- Practice the interaction of pyright LSP and the SQLAlchemy ORM.""", order=1)
    practical_goals= ProjectSection(type=SectionType.GOALS, title="Practical Objectives", body="""
- A landing page for my server
- A coding project portfolio
- A personal blog""", order=2)
    implementation1= ProjectSection(type=SectionType.IMPLEMENTATION, title="Backend Architecture", body="Built with Flask framework using blueprints for modular design. Implements SQLAlchemy ORM for database operations with migration support via Alembic.", icon="fas fa-3x fa-server", order=1)
    implementation2= ProjectSection(type=SectionType.IMPLEMENTATION, title="Frontend Design", body="Responsive UI built with Bulma CSS framework. Jinja2 templates provide server-side rendering with minimal JavaScript for enhanced interactions.", icon="fas fa-3x fa-palette", order=2)
    implementation3= ProjectSection(type=SectionType.IMPLEMENTATION, title="Deployment Infrastructure", body="Deployment on a VPS served with the Gunicorn HTTP server and routed with NGINX. Data is served throught a MariaDB instance.", icon="fas fa-3x fa-sitemap", order=3)
    next_steps1 = ProjectSection(type=SectionType.EXPLORATION, title="Project Enhancements", body="""
- Enable comments on blogposts.
- Allow e-mail signup for new developments.
- Implement searching and filtering by tags/categories/languages.
- Create related articles/projects.
    """,order=1)
    next_steps2 = ProjectSection(type=SectionType.EXPLORATION, title="Follow-up Projects", body="""
- Create a Bulma + JS carousel.
- Central admin dashboard.
- Implement web analytics.
    """,order=2)
    project = Project(title="Homepage", subtitle="A landing page for my server, an overview of my projects, and personal blog", status=DevelopmentStatus.IN_PROGRESS, extract="I was in need of a unified landing page to refer to various deployed projects and decided it would be a perfect opportunity to try learning a new CSS framework: Bulma CSS", deployment_url="https://hagen.social", github_url="https://github.com/Vanpaia/homepage", image="homepage.png", featured_order=3, features=[feature1, feature2, feature3, feature4], sections=[overview, learning_goals, practical_goals, implementation1, implementation2, implementation3, next_steps1, next_steps2], slug="homepage")
    db.session.add(project)
    db.session.commit()

    project = Project.query.filter_by(title="Homepage").first()
    technologies = Technology.query.all()
    project.technologies = technologies

    db.session.commit()
