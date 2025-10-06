from app import create_app, db
from config import Config

from app.models import DevelopmentStatus, SectionType, TechnologyType, ContentType
from app.models import Project, ProjectFeature, ProjectSection, Technology, RelatedContent
app = create_app(config_class=Config)
with app.app_context():
    '''
    feature1 = ProjectFeature(title="Create carousel HTML scaffolding", status=DevelopmentStatus.IN_PROGRESS, order=1)
    feature2 = ProjectFeature(title="Bulma CSS styling of carousel", status=DevelopmentStatus.PLANNED, order=2) 
    feature2 = ProjectFeature(title="Make carousel interactive with JS", status=DevelopmentStatus.PLANNED, order=2) 
    overview = ProjectSection(type=SectionType.OVERVIEW, body="""
Currently, my homepage has 3 available cards for latest blogposts and featured projects. I would like to have a carousel to showcase more than three cards and rotate between them.

Bulma CSS does not have a native carousel. Eventhough carousel extensions are available, I would like to prevent needless dependencies and would like to dive deeper into Bulma CSS by extending the native components myself.
""")
    learning_goals = ProjectSection(type=SectionType.GOALS, title="Learning Objectives", body="""
- Deepen my knowledge about the Bulma CSS framework.
- Practice the interaction JS and Bulma CSS.""", order=1)
    practical_goals= ProjectSection(type=SectionType.GOALS, title="Practical Objectives", body="""
- A reusable Bulma CSS carousel""", order=1)
    implementation1= ProjectSection(type=SectionType.IMPLEMENTATION, title="CSS", body="JavaScript for animations and interactions", icon="fas fa-3x fa-gear", order=1)
    implementation2= ProjectSection(type=SectionType.IMPLEMENTATION, title="CSS", body="Extending the Bulma CSS framework with custom CSS.", icon="fas fa-3x fa-palette", order=2)
    next_steps1 = ProjectSection(type=SectionType.EXPLORATION, title="Project Enhancements", body="""
- Create Bulma CSS tags input extension.
- Create Bulma CSS popup tooltip.
    """,order=1)
    next_steps2 = ProjectSection(type=SectionType.EXPLORATION, title="Project Implemention", body="""
- Implement the Bulma CSS carousel in the homepage.
    """,order=2)
    project = Project(title="Bulma CSS carousel", subtitle="A homemade extension to the Bulma CSS framework, implementing a carousel function.", status=DevelopmentStatus.IN_PROGRESS, extract="Having no native JS implementation, Bulma CSS lacks an animated carousel component. Writing this extension would help me learn Bulma CSS better.", github_url="https://github.com/Vanpaia/bulma_carousel", features=[feature1, feature2], sections=[overview, learning_goals, practical_goals, implementation1, implementation2, next_steps1, next_steps2], slug="bulma-carousel")
    db.session.add(project)
    db.session.commit()
    '''

    project1 = Project.query.filter_by(title="Homepage").first()
    project2 = Project.query.filter_by(title="Bulma CSS carousel").first()
    [print(p.object.title) for p in project1.related_content]


