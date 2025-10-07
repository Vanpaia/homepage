from app import create_app, db
from config import Config

from app.models import DevelopmentStatus, SectionType, TechnologyType, ContentType
from app.models import Project, ProjectFeature, ProjectSection, Technology, RelatedContent
app = create_app(config_class=Config)
with app.app_context():
    '''
    feature1 = ProjectFeature(title="Official API integration", status=DevelopmentStatus.COMPLETED, order=1)
    feature2 = ProjectFeature(title="Live updated metro map", status=DevelopmentStatus.COMPLETED, order=2) 
    feature3 = ProjectFeature(title="Flyout for metro timetable", status=DevelopmentStatus.IN_PROGRESS, order=3) 
    overview = ProjectSection(type=SectionType.OVERVIEW, body="""
I have always wondered what the live metro map of Brussels looks like, since the official live trackers only show one line in one direction.

This project serves as an introduction to JavaScript for me. I realised I need JavaScript to make interactive web experiences and thought it was a great project to learn interacting with the DOM. 
""")
    learning_goals = ProjectSection(type=SectionType.GOALS, title="Learning Objectives", body="""
- Learn JavaScript
- Working with WebSockets
- Accessing and using third-party APIs""", order=1)
    practical_goals= ProjectSection(type=SectionType.GOALS, title="Practical Objectives", body="""
- A live, real-time metro map of Brussels""", order=2)
    implementation1= ProjectSection(type=SectionType.IMPLEMENTATION, title="Backend Architecture", body="Built with the Bun framework. Connections to the live map are imlemented with WebSockets.", icon="fas fa-3x fa-server", order=1)
    implementation2= ProjectSection(type=SectionType.IMPLEMENTATION, title="Frontend Design", body="Minimal frontend design is provided by direct DOM manipulation, changing the rendered SVG, based on information received through WebSockets.", icon="fas fa-3x fa-palette", order=2)
    implementation3= ProjectSection(type=SectionType.IMPLEMENTATION, title="Deployment Infrastructure", body="Deployment on a VPS served with a Bun HTTP server and routed with NGINX.", icon="fas fa-3x fa-sitemap", order=3)
    next_steps1 = ProjectSection(type=SectionType.EXPLORATION, title="Project Enhancements", body="""
- Manage API fetches based on WebSocket connections.
- Implement zoom and pan on the map.
- Live toasts for metro notifications.
    """,order=1)
    next_steps2 = ProjectSection(type=SectionType.EXPLORATION, title="Follow-up Projects", body="""
- Create a picture galery for metro stations.
    """,order=2)
    project = Project(title="Metro Map", subtitle="Who doesn't like WebSockets and the Metro?", status=DevelopmentStatus.IN_PROGRESS, extract="This is implementing a real-time map of the Brussels metro using WebSockets and Bun.", deployment_url="https://metro.hagen.social", github_url="https://github.com/Vanpaia/metro_map", features=[feature1, feature2, feature3], sections=[overview, learning_goals, practical_goals, implementation1, implementation2, implementation3, next_steps1, next_steps2], slug="metro-map")
    db.session.add(project)
    db.session.commit()

    technologies = []
    technologies.append(Technology.query.filter_by(title="JavaScript 18.19.x").first())
    technologies.append(Technology.query.filter_by(title="nginx 1.18.x").first())
    technologies.append(Technology(title="Bun 1.2.x", type=TechnologyType("backend"), image="bun.png", order=1))
    project.technologies = technologies
    db.session.commit()

    ''' 
    project = Project.query.filter_by(id=4).first()
    project.featured_order=1
    db.session.commit()








