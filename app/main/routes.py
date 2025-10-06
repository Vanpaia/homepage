from flask import render_template, render_template_string
from app.main import bp
from app.models import BlogPost, Project
from app import db
from markupsafe import Markup
from markdown import markdown

@bp.app_context_processor
def inject_global_vars():
    """Make variables available to all templates"""
    return {
        'navbar_projects': Project.get_deployed()
    }

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    deployed_projects = Project.get_deployed()
    latest_posts = BlogPost.get_recent()
    featured_projects = Project.get_featured()[:3]
    return render_template('index.html', deployed_projects=deployed_projects, latest_posts=latest_posts, featured_projects=featured_projects, title='Home')

@bp.route('/blog', methods=['GET'])
def blog():
    posts = BlogPost.query.all()
    return render_template('blog.html', posts=posts, title='Blog')

@bp.route('/blog/<int:post_id>-<post_slug>', methods=['GET'])
def blogpost(post_id, post_slug):
    post_content = db.first_or_404(db.select(BlogPost).filter_by(id=post_id))
    html_content = markdown(post_content.body)
    post_body = Markup(render_template_string(html_content))
    print(post_body)
    return render_template('blogpost.html', body=post_body, post=post_content, title='Blog')

@bp.route('/portfolio', methods=['GET'])
def portfolio():
    projects = Project.query.all()
    return render_template('portfolio.html',projects=projects, title='Portfolio')

@bp.route('/portfolio/<int:project_id>-<project_slug>', methods=['GET'])
def project(project_id, project_slug):
    project_data = Project.query.filter_by(id=project_id).first_or_404()
    return render_template('project.html', project=project_data, title='Portfolio')
