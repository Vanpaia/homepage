from app import create_app, db
from config import Config

from app.models import Category, Tag, Language, BlogPost

app = create_app(config_class=Config)

with app.app_context():

    post = BlogPost.query.filter_by(title="Test").first()
    category = Category.query.filter_by(name="Politics").first()
    tag = Tag.query.filter_by(name="Privacy").first()
    post.category= category
    post.tags.append(tag)
    db.session.commit()

    print(post.category.name)
    for x in post.tags:
        print(x.name)
