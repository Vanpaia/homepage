from markupsafe import Markup
from flask import render_template_string

def jinja_markdown(content: str) -> Markup:
    """Renders markdown, then passes the result back through Jinja for rendering."""
    rendered_content = render_template_string(content)
    
    return Markup(rendered_content)
