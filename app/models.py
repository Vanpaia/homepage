from app import db
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Column, Table, Boolean
from sqlalchemy import Enum as SQLEnum
from flask import url_for
from enum import Enum
from markdown import markdown
from dataclasses import dataclass


class DevelopmentStatus(str, Enum):
    """Status options for projects"""
    PLANNED = "planned" 
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"
    ON_HOLD = "on_hold"

    @property
    def display_title(self) -> str:
        """Converts the enum value ('in-progress') into a human-readable string ('In Progress')."""
        name_with_spaces = self.value.replace('_', ' ').replace('-', ' ')

        return name_with_spaces.title()

class ContentType(str, Enum):
    """Types of categories for sorting"""
    BLOG = "blogpost" 
    PROJECT = "code_project" 

class TechnologyType(str, Enum):
    """Types of technologies used in Projects"""
    BACKEND = "backend" 
    FRONTEND = "frontend" 
    DEVOPS = "devops" 
    LANGUAGE = "language" 

class SectionType(str, Enum):
    """Types of technologies used in Projects"""
    OVERVIEW = "overview" 
    GOALS = "project_goals" 
    IMPLEMENTATION = "implementation_details" 
    EXPLORATION = "exploratory_avenues" 


# Association tables
project_tags = Table('project_tags', db.Model.metadata,
    Column('project_id', Integer, ForeignKey('coding_project.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('homepage_tag.id'), primary_key=True)
)

project_technologies = Table('project_technologies', db.Model.metadata,
    Column('project_id', Integer, ForeignKey('coding_project.id'), primary_key=True),  
    Column('technology_id', Integer, ForeignKey('homepage_technology.id'), primary_key=True)
)

blogpost_tags = Table('blogpost_tags', db.Model.metadata,
    Column('blogpost_id', Integer, ForeignKey('blog_post.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('homepage_tag.id'), primary_key=True)  
)

blogpost_technologies= Table('blogpost_technologies', db.Model.metadata,
    Column('blogpost_id', Integer, ForeignKey('blog_post.id'), primary_key=True),  
    Column('technology_id', Integer, ForeignKey('homepage_technology.id'), primary_key=True)
)

related_projects = Table('related_projects', db.Model.metadata,
    Column('coding_project_id_1', Integer, ForeignKey('coding_project.id'), primary_key=True),  
    Column('coding_project_id_2', Integer, ForeignKey('coding_project.id'), primary_key=True)
)

@dataclass
class RelatedItem:
    """
    A wrapper class for the RelatedContent model, so both Project and Blogpost models can be passed
    """
    type: str
    object: object

    @property
    def icon(self):
        return "fa-project-diagram" if self.type == "project" else "fa-pen-nib"

    @property
    def url(self):
        if self.type == "blogpost":
            return_url = url_for("main.blogpost", post_id=self.object.id, post_slug=self.object.slug)
        else:
            return_url = url_for("main.project", project_id=self.object.id, project_slug=self.object.slug)

        return return_url



class RelatedContent(db.Model):
    """
    Related content model attaching blogposts and projects to each other.
    Attributes:
        id (int): Primary key, auto-incrementing post ID
        source_type (ContentType): ContentType is an Enum
        source_id (int): Faux foreign key refering to the ID of one side of the relationship
        target_type (ContentType): ContentType is an Enum
        target_id (int): Faux foreign key refering to the ID of the other side of the relationship
    """
    __tablename__ = "related_content"

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, nullable=False)
    source_type: Mapped[ContentType] = mapped_column(
        SQLEnum(ContentType), 
        nullable=False,
        index=True
    )

    target_id = db.Column(db.Integer, nullable=False)
    target_type: Mapped[ContentType] = mapped_column(
        SQLEnum(ContentType), 
        nullable=False,
        index=True
    )

    __table_args__ = (
        db.UniqueConstraint("source_type", "source_id", "target_type", "target_id", name="uq_related_content"),
        db.CheckConstraint("NOT (source_id = target_id AND source_type = target_type)", name="ck_no_self_link"),
    )

    if TYPE_CHECKING:
        def __init__(
            self, 
            *,
            source_type: ContentType,
            source_id: int,
            target_type: ContentType,
            target_id: int,
        ) -> None: ...
    else:
        def __init__(self, source_type, source_id, target_type, target_id):
            # normalize pair to avoid reverse duplicates
            if (target_type, target_id) < (source_type, source_id):
                source_type, target_type = target_type, source_type
                source_id, target_id = target_id, source_id

            self.source_type = source_type
            self.source_id = source_id
            self.target_type = target_type
            self.target_id = target_id
 
    def __repr__(self) -> str:
        return f'<Related Content: {self.source_id} - {self.target_id}>'

    def __str__(self) -> str:
        return f'This entry represents the relationship between: {self.source_type} - {self.source_id} and {self.target_type} - {self.target_id}'
    
class Category(db.Model):
    """
    Category model for categorizing blogposts and projects.
    Attributes:
        id (int): Primary key, auto-incrementing post ID
        title (str): Category title, max 32 characters
        type (ContentType): ContentType is an Enum
        color (str): Color hex code, max 7 characters
    """
    __tablename__ = 'homepage_category'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    type: Mapped[ContentType] = mapped_column(
        SQLEnum(ContentType), 
        nullable=False,
        index=True
    )
    color: Mapped[str] = mapped_column(String(7), nullable=False)
    
    if TYPE_CHECKING:
        def __init__(
            self, 
            *,
            title: str,
            type: ContentType,
            color: str,
        ) -> None: ...
    
    def __repr__(self) -> str:
        return f'<Homepage Category: {self.id} - {self.title}>'
 
    def __str__(self) -> str:
        return f'Homepage Category: {self.title}'



class Tag(db.Model):
    """
    Tag model for tagging blogposts and projects.
    Attributes:
        id (int): Primary key, auto-incrementing post ID
        title (str): Category title, max 32 characters
    """
    __tablename__ = 'homepage_tag'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    
    if TYPE_CHECKING:
        def __init__(
            self, 
            *,
            title: str,
        ) -> None: ...
     
    def __repr__(self) -> str:
        return f'<Homepage Tag: {self.id} - {self.title}>'
 
    def __str__(self) -> str:
        return f'Homepage Tag: {self.title}'


class Technology(db.Model):
    """
    Model for tagging blogposts and projects with specific programming languages.
    Attributes:
        id (int): Primary key, auto-incrementing post ID
        title (str): Category title, max 32 characters
        type (TechnologyType): TechnologyType is an Enum
        image (str | None): Path to image, max 128 characters
        order (int): Interger determining the order of entry
    """
    __tablename__ = 'homepage_technology'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    type: Mapped[TechnologyType] = mapped_column(
        SQLEnum(TechnologyType), 
        nullable=False,
        index=True
    )
    image: Mapped[str | None] = mapped_column(String(128), nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    if TYPE_CHECKING:
        def __init__(
            self, 
            *,
            title: str,
            type: TechnologyType,
            image: str | None = None,
            order: int | None = None,
        ) -> None: ...
    
    def __repr__(self) -> str:
        return f'<Homepage Technology: {self.id} - {self.title}>'
 
    def __str__(self) -> str:
        return f'Homepage Technology: {self.type} - {self.title}'

    @property
    def image_url(self) -> str:
        """Generate full URL for the image attached to this Technology"""
        return url_for('static', filename=self.image, _external=True)


class ProjectSection(db.Model):
    """
    A Model to define different sections in the Project visualisation dynamically.
    Attributes:
        id (int): Primary key, auto-incrementing post ID
        project_id (int | None): Foreign key, refering to the related Project 
        title (str | None): Section title, max 64 characters
        type (TechnologyType): TechnologyType is an Enum
        body (str): Full post content formatted with Markdown (unlimited text)
        icon (str | None): Name of fontawesome v5.3.1 icon, max 128 characters
        order (int): Interger determining the order of entry
    """
    __tablename__ = 'project_section'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str | None] = mapped_column(String(64), nullable=True)
    type: Mapped[SectionType] = mapped_column(
        SQLEnum(SectionType), 
        nullable=False,
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)
    icon: Mapped[str | None] = mapped_column(String(128), nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    project_id: Mapped[int] = mapped_column(ForeignKey('coding_project.id'), index=True)  
    project: Mapped["Project"] = relationship(back_populates="sections")      
    if TYPE_CHECKING:
        def __init__(
            self, 
            *,
            title: str | None = None,
            type: SectionType,
            body: str,
            icon: str | None = None,
            order: int | None = None,
            project_id: int | None = None,
        ) -> None: ...
     
    def __repr__(self) -> str:
        return f'<Project Section {self.type}: {self.id}>'

    def __str__(self) -> str:
        return f'Project {self.project.id} Section {self.type}: {self.title}'

    def render_html(self) -> str:
        return markdown(self.body or "")

class ProjectFeature(db.Model):
    """
    Model for adding features to projects and show their status.
    Attributes:
        id (int): Primary key, auto-incrementing post ID
        project_id (int | None): Foreign key, refering to the related Project 
        title (str): Category title, max 64 characters
        status (DevelopmentStatus): DevelopmentStatus is an Enum
        order (int | None): Interger determining the order of entry
    """
    __tablename__ = 'project_feature'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[DevelopmentStatus] = mapped_column(
        SQLEnum(DevelopmentStatus), 
        nullable=False,
        default=DevelopmentStatus.PLANNED,
    )
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    project_id: Mapped[int] = mapped_column(ForeignKey('coding_project.id'), index=True)  
    project: Mapped["Project"] = relationship(back_populates="features")
    
    if TYPE_CHECKING:
        def __init__(
            self, 
            *,
            title: str,
            status: DevelopmentStatus | None = None,
            order: int | None = None,
            project_id: int | None = None,
        ) -> None: ...
     
    def __repr__(self) -> str:
        return f'<Project Feature {self.id} - {self.title}>'

    def __str__(self) -> str:
        return f'Project {self.project.id} Feature {self.id}'

    @property
    def status_badge_color(self) -> str:
        """Return CSS class for status badge"""
        return {
            DevelopmentStatus.PLANNED: "tag is-primary",
            DevelopmentStatus.IN_PROGRESS: "tag is-warning",
            DevelopmentStatus.COMPLETED: "tag is-success",
            DevelopmentStatus.ON_HOLD: "tag is-danger",
        }.get(self.status, "tag is-primary")


class BlogPost(db.Model):
    """
    Blog post model for storing articles and content.
    Attributes:
        id (int): Primary key, auto-incrementing post ID
        created_at (datetime): UTC timestamp when post was created (auto-set)
        title (str): Post title, max 128 characters
        subtitle (str | None): Post subtitle, max 128 characters
        body (str): Full post content formatted with Markdown (unlimited text)
        extract (str): Short excerpt/summary, max 512 characters
        image (str): Path to main post image, max 128 characters
        thumbnail (str | None): Path to thumbnail image, max 128 characters
        slug (str | None): Slug for url routes
    """
    __tablename__ = 'blog_post'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        index=True, 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        index=True, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    title: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    subtitle: Mapped[str | None] = mapped_column(String(128), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    extract: Mapped[str] = mapped_column(String(512), nullable=False)
    image: Mapped[str] = mapped_column(String(128), nullable=False)
    thumbnail: Mapped[str | None] = mapped_column(String(128), nullable=True)
    slug: Mapped[str] = mapped_column(String(128), nullable=False, index=True)

    category_id: Mapped[int | None] = mapped_column(ForeignKey('homepage_category.id', name='fk_blog_post_category_id'), index=True)
    category: Mapped["Category | None"] = relationship("Category")
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary=blogpost_tags)
    technologies: Mapped[list["Technology"]] = relationship("Technology", secondary=blogpost_technologies)

    if TYPE_CHECKING:
        def __init__(
            self, 
            *,
            created_at: datetime | None = None,
            visible: bool | None = None,
            title: str,
            subtitle: str | None = None,
            body: str,
            extract: str,
            image: str,
            thumbnail: str | None = None,
            slug: str,
            tags: list[Tag] | None = None,
            technologies: list[Technology] | None = None,
        ) -> None: ...
    
    def __repr__(self) -> str:
        return f'<BlogPost {self.title}>'

    def __str__(self) -> str:
        return f'{self.title} - {self.extract}'

    def render_html(self) -> str:
        """Get the markdown body as html rendered"""
        return markdown(self.body or "")

    @property
    def url(self) -> str:
        """Generate full URL for this post"""
        return url_for('main.blogpost', post_id=self.id, post_slug=self.slug, _external=True)

    @property
    def image_url(self) -> str:
        """Generate full URL for the image attached to this post"""
        return url_for('static', filename=self.image, _external=True)

    @property
    def thumbnail_url(self) -> str:
        """Generate full URL for the thumbnail attached to this post"""
        return url_for('static', filename=self.thumbnail, _external=True)

    @property
    def formatted_created_at(self) -> str:
        """Human-readable creation date"""
        return self.created_at.strftime('%A, %d %B %Y')

    @property
    def formatted_updated_at(self) -> str:
        """Human-readable update date"""
        return self.updated_at.strftime('%A, %d %B %Y')

    @classmethod
    def get_recent(cls, limit: int = 3) -> list["BlogPost"]:
        """Get recent blogposts ordered by date"""
        return cls.query.order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def get_by_slug(cls, slug: str) -> "BlogPost | None":
        """Get blogpost by slug"""
        return cls.query.filter_by(slug=slug).first()

    @classmethod
    def get_by_id(cls, id: int) -> "BlogPost | None":
        """Get blogpost by id"""
        return cls.query.filter_by(id=id).first()
       
    @classmethod
    def with_tag(cls, tag_title: str) -> list["BlogPost"]:
        """Get blogposts with a specific tag"""
        return cls.query.join(cls.tags).filter(Tag.title == tag_title).all()

    @classmethod
    def with_technology(cls, technology_title: str) -> list["BlogPost"]:
        """Get blogposts with a specific technology"""
        return cls.query.join(cls.tags).filter(Technology.title == technology_title).all()

    @classmethod
    def with_category(cls, category_title: str) -> list["BlogPost"]:
        """Get blogposts with a specific category"""
        return cls.query.join(cls.tags).filter(Category.title == category_title).all()

class Project(db.Model):
    """
    Project model for storing project descriptions and details.
    Attributes:
        id (int): Primary key, auto-incrementing post ID
        created_at (datetime): UTC timestamp when post was created (auto-set)
        title (str): Project title, max 128 characters
        subtitle (str): Project subtitle, max 128 characters
        status (DevelopmentStatus): DevelopmentStatus is an Enum
        extract (str): Short excerpt/summary, max 512 characters
        github_url (str | None): URL to the github repository, max 64 characters
        deployment_url (str | None): URL to the hosted project, max 64 characters
        image (str | None): Path to main project image, max 128 characters
        featured_order (int | None): Only Projects with a featured order get featured, in the order of Integers low -> high
        slug (str | None): Slug for url routes
    """
    __tablename__ = 'coding_project'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        index=True, 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        index=True, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    subtitle: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[DevelopmentStatus] = mapped_column(
        SQLEnum(DevelopmentStatus), 
        nullable=False,
        index=True,
        default=DevelopmentStatus.IN_PROGRESS,
    )
    extract: Mapped[str] = mapped_column(String(512), nullable=False)
    github_url: Mapped[str | None] = mapped_column(String(128), nullable=True)
    deployment_url: Mapped[str | None] = mapped_column(String(128), nullable=True)
    image: Mapped[str | None] = mapped_column(String(128), nullable=True)
    featured_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    slug: Mapped[str] = mapped_column(String(128), nullable=False, index=True)

    category_id: Mapped[int | None] = mapped_column(ForeignKey('homepage_category.id'), index=True)  
    category: Mapped["Category | None"] = relationship("Category")
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary=project_tags)
    technologies: Mapped[list["Technology"]] = relationship("Technology", secondary=project_technologies)
    features: Mapped[list["ProjectFeature"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="ProjectFeature.order"
    )
    sections: Mapped[list["ProjectSection"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="ProjectSection.order"
    )

    related_sources = db.relationship(
        "RelatedContent",
        primaryjoin="and_(foreign(RelatedContent.source_id) == Project.id, RelatedContent.source_type == 'code_project')",
        cascade="all, delete-orphan",
        lazy="select",
    )

    related_targets = db.relationship(
        "RelatedContent",
        primaryjoin="and_(foreign(RelatedContent.target_id) == Project.id, RelatedContent.source_type == 'code_project')",
        cascade="all, delete-orphan",
        lazy="select",
    )

    # Type hints for LSP - these won't affect runtime but help static analysis
    if TYPE_CHECKING:
        def __init__(
            self, 
            *,
            created_at: datetime | None = None,
            visible: bool | None = None,
            title: str,
            subtitle: str | None = None,
            status: DevelopmentStatus| None = None,
            extract: str,
            github_url: str | None = None,
            deployment_url: str | None = None,
            image: str | None = None,
            featured_order: int | None = None,
            slug: str,
            tags: list[Tag] | None = None,
            technologies: list[Technology] | None = None,
            features: list[ProjectFeature] | None = None,
            sections: list[ProjectSection] | None = None,
        ) -> None: ...
    
    def __repr__(self) -> str:
        return f'<Project {self.id} - {self.title}>'

    def __str__(self) -> str:
        return f'Project {self.title} - {self.extract}'

    @property
    def status_badge_color(self) -> str:
        """Return CSS class for status badge"""
        return {
            DevelopmentStatus.PLANNED: "tag is-primary",
            DevelopmentStatus.IN_PROGRESS: "tag is-warning",
            DevelopmentStatus.COMPLETED: "tag is-success",
            DevelopmentStatus.ON_HOLD: "tag is-danger",
        }.get(self.status, "tag is-primary")

    @property
    def url(self) -> str:
        """Generate full URL for this post"""
        return url_for('main.blogpost', post_id=self.id, post_slug=self.slug, _external=True)

    @property
    def image_url(self) -> str:
        """Generate full URL for the image attached to this post"""
        return url_for('static', filename=self.image, _external=True)

    @property
    def has_github(self) -> bool:
        return self.github_url is not None and len(self.github_url) > 0
    
    @property
    def has_deployment(self) -> bool:
        return self.deployment_url is not None and len(self.deployment_url) > 0
    
    @property
    def is_featured(self) -> bool:
        return self.featured_order is not None

    @property
    def formatted_created_at(self) -> str:
        """Human-readable creation date"""
        return self.created_at.strftime('%A, %d %B %Y')

    @property
    def formatted_updated_at(self) -> str:
        """Human-readable update date"""
        return self.updated_at.strftime('%A, %d %B %Y')

    @property
    def backend_technologies(self) -> list[Technology]:
        """Filter technologies by backend type"""
        return [t for t in self.technologies if t.type == TechnologyType.BACKEND]
    
    @property
    def frontend_technologies(self) -> list[Technology]:
        """Filter technologies by frontend type"""
        return [t for t in self.technologies if t.type == TechnologyType.FRONTEND]

    @property
    def devops_technologies(self) -> list[Technology]:
        """Filter technologies by devops type"""
        return [t for t in self.technologies if t.type == TechnologyType.DEVOPS]
       
    @property
    def languages(self) -> list[Technology]:
        """Filter technologies by language type"""
        return [t for t in self.technologies if t.type == TechnologyType.LANGUAGE]
 
    @property
    def section_overview(self) -> list[ProjectSection]:
        """Filter sections by overview type"""
        return [s for s in self.sections if s.type == SectionType.OVERVIEW]
    
    @property
    def section_goals(self) -> list[ProjectSection]:
        """Filter sections by goal type"""
        return [s for s in self.sections if s.type == SectionType.GOALS]
      
    @property
    def section_implementation(self) -> list[ProjectSection]:
        """Filter sections by implementation type"""
        return [s for s in self.sections if s.type == SectionType.IMPLEMENTATION]
      
    @property
    def section_exploration(self) -> list[ProjectSection]:
        """Filter section by exploration type"""
        return [s for s in self.sections if s.type == SectionType.EXPLORATION]
       
    @property
    def related_content(self) -> list[RelatedContent]:
        """Get related content"""
        results = []
        rels = list(self.related_sources) + list(self.related_targets) #type: ignore

        for rel in rels:
            if rel.source_type == "code_project" and rel.source_id != self.id:
                obj = Project.query.get(rel.source_id)
                if obj:
                    results.append(RelatedItem("code_project", obj))
            elif rel.target_type == "code_project" and rel.target_id != self.id:
                obj = Project.query.get(rel.target_id)
                if obj:
                    results.append(RelatedItem("code_project", obj))
            elif rel.source_type == "blogpost":
                obj = BlogPost.query.get(rel.source_id)
                if obj:
                    results.append(RelatedItem("blogpost", obj))
            elif rel.target_type == "blogpost":
                obj = BlogPost.query.get(rel.target_id)
                if obj:
                    results.append(RelatedItem("blogpost", obj))

        seen = set()
        unique = []
        for item in results:
            key = (item.type, item.object.id)
            if key not in seen:
                seen.add(key)
                unique.append(item)

        return unique[:5]


    @classmethod
    def get_recent(cls, limit: int = 3) -> list["Project"]:
        """Get recent projects ordered by date"""
        return cls.query.order_by(cls.created_at.desc()).limit(limit).all()
     
    @classmethod
    def get_deployed(cls) -> list["Project"]:
        """Get projects that have been deployed"""
        return cls.query.filter((cls.deployment_url.is_not(None)) & (cls.deployment_url != '')).all()
     
    @classmethod
    def get_featured(cls) -> list["Project"]:
        """Get projects that have been featured"""
        return cls.query.filter(cls.featured_order.is_not(None)).order_by(cls.featured_order.asc()).all()

    @classmethod
    def get_by_slug(cls, slug: str) -> "Project | None":
        """Get project by slug"""
        return cls.query.filter_by(slug=slug).first()

    @classmethod
    def get_by_id(cls, id: int) -> "Project | None":
        """Get project by id"""
        return cls.query.filter_by(id=id).first()
       
    @classmethod
    def with_tag(cls, tag_title: str) -> list["Project"]:
        """Get projects with a specific tag"""
        return cls.query.join(cls.tags).filter(Tag.title == tag_title).all()

    @classmethod
    def with_technology(cls, technology_title: str) -> list["Project"]:
        """Get projects with a specific technology"""
        return cls.query.join(cls.tags).filter(Technology.title == technology_title).all()

    @classmethod
    def with_category(cls, category_title: str) -> list["Project"]:
        """Get projects with a specific category"""
        return cls.query.join(cls.tags).filter(Category.title == category_title).all()


