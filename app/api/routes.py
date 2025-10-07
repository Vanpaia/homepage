from flask import render_template, render_template_string, request, jsonify, current_app
from app.api import bp
from app.models import BlogPost, Project, Category, ProjectFeature, ProjectSection, SectionType, Technology, Tag
from app.models import ContentType, DevelopmentStatus
from app import db
from markupsafe import Markup
from markdown import markdown
from functools import wraps
from datetime import datetime, timezone
from collections import defaultdict
from time import time

request_counts = defaultdict(list)

def rate_limit_check():
    """Simple rate limiting by IP address"""
    if not current_app.config['ENABLE_RATE_LIMITING'].lower() == 'true':
        return True
    
    ip = request.remote_addr
    now = time()
    
    # Clean old requests
    request_counts[ip] = [req_time for req_time in request_counts[ip] 
                          if now - req_time < int(current_app.config['RATE_WINDOW'])]
    
    # Check limit
    if len(request_counts[ip]) >= int(current_app.config['RATE_LIMIT']):
        return False
    
    # Add current request
    request_counts[ip].append(now)
    return True

def require_rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not rate_limit_check():
            return jsonify({'error': 'Rate limit exceeded. Try again later.'}), 429
        return f(*args, **kwargs)
    return decorated_function

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != current_app.config['SECRET_KEY']:
            return jsonify({'error': 'Invalid or missing API key'}), 401
        
        current_app.logger.info(f"API access: {request.method} {request.path} from {request.remote_addr}")

        return f(*args, **kwargs)
    return decorated_function

# Helper function to get or create tags
def get_or_create_tags(tag_titles):
    """Get existing tags or create new ones"""
    tags = []
    for title in tag_titles:
        tag = Tag.query.filter_by(title=title).first()
        if not tag:
            tag = Tag(title=title)
            db.session.add(tag)
        tags.append(tag)
    return tags

# Helper function to get or create technologies
def get_or_create_technologies(tech_data_list):
    """Get existing technologies or create new ones"""
    technologies = []
    for tech_data in tech_data_list:
        tech_title = tech_data if isinstance(tech_data, str) else tech_data.get('title')
        tech = Technology.query.filter_by(title=tech_title).first()
        if not tech and isinstance(tech_data, dict):
            # Create new technology with full data
            tech = Technology(
                title=tech_data['title'],
                type=tech_data['type'],
                image=tech_data.get('image'),
                order=tech_data['order']
            )
            db.session.add(tech)
        technologies.append(tech)
    return technologies

@bp.route('/posts', methods=['POST'])
@require_api_key
@require_rate_limit
def create_post():
    """Create a new blog post"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'body', 'extract', 'slug', 'image']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if slug already exists
    if BlogPost.query.filter_by(slug=data['slug']).first():
        return jsonify({'error': 'Slug already exists'}), 400
    
    # Create the blog post
    post = BlogPost(
        title=data['title'],
        created_at=data.get('created_at'),
        subtitle=data.get('subtitle'),
        body=data['body'],
        extract=data['extract'],
        slug=data['slug'],
        image=data['image'],
        thumbnail=data.get('thumbnail')
    )
    
    # Handle category
    if 'category' in data:
        category = Category.query.filter_by(title=data['category'], type=ContentType.BLOG).first()
        if category:
            post.category = category
    
    # Handle tags
    if 'tags' in data and isinstance(data['tags'], list):
        post.tags = get_or_create_tags(data['tags'])
    
    # Handle technologies
    if 'technologies' in data and isinstance(data['technologies'], list):
        post.technologies = get_or_create_technologies(data['technologies'])
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify({
        'message': 'Blog post created successfully',
        'id': post.id,
        'slug': post.slug
    }), 201


@bp.route('/posts/<int:post_id>', methods=['PUT', 'PATCH'])
@require_api_key
@require_rate_limit
def update_post(post_id):
    """Update an existing blog post"""
    post = BlogPost.query.get_or_404(post_id)
    data = request.get_json()
    
    # Update fields if provided
    if 'title' in data:
        post.title = data['title']
    if 'subtitle' in data:
        post.subtitle = data['subtitle']
    if 'body' in data:
        post.body = data['body']
    if 'extract' in data:
        post.extract = data['extract']
    if 'slug' in data:
        # Check if new slug is already taken by another post
        existing = BlogPost.query.filter_by(slug=data['slug']).first()
        if existing and existing.id != post_id:
            return jsonify({'error': 'Slug already exists'}), 400
        post.slug = data['slug']
    if 'image' in data:
        post.image = data['image']
    if 'thumbnail' in data:
        post.thumbnail = data['thumbnail']
    
    # Update category
    if 'category' in data:
        category = Category.query.filter_by(title=data['category'], type=ContentType.BLOG).first()
        post.category = category
    
    # Update tags
    if 'tags' in data and isinstance(data['tags'], list):
        post.tags = get_or_create_tags(data['tags'])
    
    # Update technologies
    if 'technologies' in data and isinstance(data['technologies'], list):
        post.technologies = get_or_create_technologies(data['technologies'])
    
    # Update timestamp
    post.updated_at = datetime.now(timezone.utc)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Blog post updated successfully',
        'id': post.id,
        'slug': post.slug
    }), 200

@bp.route('/posts/<int:post_id>', methods=['DELETE'])
@require_api_key
@require_rate_limit
def delete_post(post_id):
    """Delete a blog post"""
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'Blog post deleted successfully'}), 200

@bp.route('/projects', methods=['POST'])
@require_api_key
def create_project():
    """Create a new project"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'subtitle', 'extract', 'slug', 'features', 'sections']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
 
    # Check if slug already exists
    if Project.query.filter_by(slug=data['slug']).first():
        return jsonify({'error': 'Slug already exists'}), 400
    
    # Create features
    features = []
    for feature in data['features']:
        features.append(ProjectFeature(
            title=feature['title'],
            status=feature.get('status', 'planned'),
            order=int(feature.get('order', 0))))

    # Create sections
    sections = []
    for section in data['sections']:
        sections.append(ProjectSection(
            type=SectionType(section['type']),
            title=section.get('title') or None,
            icon=section.get('icon') or None,
            body=section['body'],
            order=int(section.get('order', 0))))

    # Create the project
    project = Project(
        title=data['title'],
        subtitle=data['subtitle'],
        status=DevelopmentStatus(data.get('status', 'in_progress')),
        extract=data['extract'],
        deployment_url=data.get('deployment_url') or None,
        github_url=data.get('github_url') or None,
        image=data.get('image') or None,
        featured_order=data.get('featured_order') or None,
        features=features,
        sections=sections,
        slug=data['slug'])

    # Handle category
    if 'category' in data:
        category = Category.query.filter_by(title=data['category'], type=ContentType.PROJECT).first()
        if category:
            project.category = category
    
    # Handle tags
    if 'tags' in data and isinstance(data['tags'], list):
        project.tags = get_or_create_tags(data['tags'])
    
    # Handle technologies
    if 'technologies' in data and isinstance(data['technologies'], list):
        project.technologies = get_or_create_technologies(data['technologies'])
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify({
        'message': 'Project created successfully',
        'id': project.id,
        'slug': project.slug,
    }), 201

@bp.route('/projects/<int:project_id>', methods=['PUT', 'PATCH'])
@require_api_key
@require_rate_limit
def update_project(project_id):
    """Update an existing project"""
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    
    # Update fields if provided
    if 'title' in data:
        project.title = data['title']
    if 'subtitle' in data:
        project.subtitle = data['subtitle']
    if 'extract' in data:
        project.extract = data['extract']
    if 'status' in data:
        project.status = DevelopmentStatus(data['status'])
    if 'github_url' in data:
        project.github_url = data['github_url']
    if 'deployment_url' in data:
        project.deployment_url = data['deployment_url']
    if 'image' in data:
        project.image = data['image']
    if 'featured_order' in data:
        project.featured_order = data['featured_order']
    
    # Update category
    if 'category' in data:
        category = Category.query.filter_by(title=data['category'], type=ContentType.PROJECT).first()
        project.category = category
    
    # Update tags
    if 'tags' in data and isinstance(data['tags'], list):
        project.tags = get_or_create_tags(data['tags'])
    
    # Update technologies
    if 'technologies' in data and isinstance(data['technologies'], list):
        project.technologies = get_or_create_technologies(data['technologies'])
    
    # Update timestamp
    project.updated_at = datetime.now(timezone.utc)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Project updated successfully',
        'id': project.id
    }), 200

@bp.route('/projects/<int:project_id>', methods=['DELETE'])
@require_api_key
@require_rate_limit
def delete_project(project_id):
    """Delete a project"""
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    
    return jsonify({'message': 'Project deleted successfully'}), 200

@bp.route('/projects/<int:project_id>/features', methods=['POST'])
@require_api_key
@require_rate_limit
def add_project_feature(project_id):
    """Add a feature to a project"""
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    
    # Validate required fields
    if 'title' not in data:
        return jsonify({'error': 'Missing required field: title'}), 400
    
    # Create feature
    feature = ProjectFeature(
        title=data['title'],
        status=DevelopmentStatus(data.get('status', 'planned')),
        order=data.get('order', 0),
        project_id=project_id
    )
    
    db.session.add(feature)
    db.session.commit()
    
    return jsonify({
        'message': 'Feature added successfully',
        'id': feature.id,
        'title': feature.title
    }), 201

@bp.route('/projects/<int:project_id>/features/<int:feature_id>', methods=['PATCH'])
@require_api_key
@require_rate_limit
def update_project_feature(project_id, feature_id):
    """Update a specific feature"""
    feature = ProjectFeature.query.filter_by(
        id=feature_id, 
        project_id=project_id
    ).first_or_404()
    
    data = request.get_json()
    
    # Update fields if provided
    if 'title' in data:
        feature.title = data['title']
    if 'status' in data:
        feature.status = DevelopmentStatus(data['status'])
    if 'order' in data:
        feature.order = data['order']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Feature updated successfully',
        'id': feature.id
    }), 200

@bp.route('/projects/<int:project_id>/features/<int:feature_id>', methods=['DELETE'])
@require_api_key
@require_rate_limit
def delete_project_feature(project_id, feature_id):
    """Delete a specific feature"""
    feature = ProjectFeature.query.filter_by(
        id=feature_id,
        project_id=project_id
    ).first_or_404()
    
    db.session.delete(feature)
    db.session.commit()
    
    return jsonify({'message': 'Feature deleted successfully'}), 200

@bp.route('/projects/<int:project_id>/sections', methods=['POST'])
@require_api_key
@require_rate_limit
def add_project_section(project_id):
    """Add a section to a project"""
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    
    # Validate required fields
    required = ['type', 'body']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create section
    section = ProjectSection(
        type=SectionType(data['type']),
        title=data.get('title') or None,
        body=data['body'],
        icon=data.get('icon') or None,
        order=data.get('order', 0),
        project_id=project_id
    )
    
    db.session.add(section)
    db.session.commit()
    
    return jsonify({
        'message': 'Section added successfully',
        'id': section.id
    }), 201

@bp.route('/projects/<int:project_id>/sections/<int:section_id>', methods=['PATCH'])
@require_api_key
@require_rate_limit
def update_project_section(project_id, section_id):
    """Update a specific section"""
    section = ProjectSection.query.filter_by(
        id=section_id,
        project_id=project_id
    ).first_or_404()
    
    data = request.get_json()
    
    # Update fields if provided
    if 'title' in data:
        section.title = data['title']
    if 'type' in data:
        section.type = SectionType(data['type'])
    if 'body' in data:
        section.body = data['body']
    if 'icon' in data:
        section.icon = data['icon']
    if 'order' in data:
        section.order = data['order']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Section updated successfully',
        'id': section.id
    }), 200

@bp.route('/projects/<int:project_id>/sections/<int:section_id>', methods=['DELETE'])
@require_api_key
@require_rate_limit
def delete_project_section(project_id, section_id):
    """Delete a specific section"""
    section = ProjectSection.query.filter_by(
        id=section_id,
        project_id=project_id
    ).first_or_404()
    
    db.session.delete(section)
    db.session.commit()
    
    return jsonify({'message': 'Section deleted successfully'}), 200

@bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@bp.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500
