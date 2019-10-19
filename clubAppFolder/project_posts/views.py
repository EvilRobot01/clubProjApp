from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from clubAppFolder import db
from clubAppFolder.models import BlogPost
from clubAppFolder.blog_posts.forms import BlogPostForms

blog_posts = Blueprint('blog_posts', __name__)

@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post()
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_posts = BlogPost(title=form.tittle.data,
                            text=form.text.data,
                            user_id=current_user.id)

        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')