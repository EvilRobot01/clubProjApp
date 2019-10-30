from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user, login_required
from clubAppFolder import db
from clubAppFolder.models import BlogPost
from clubAppFolder.blog_posts.forms import BlogPostForm
from clubAppFolder.blog_posts.picture_handler import add_blog_image

blog_posts = Blueprint('blog_posts', __name__)

@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(title=form.title.data,
                            text=form.text.data,
                            user_id=current_user.id
                            )

        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)


@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title, 
                            date=blog_post.date,post=blog_post)


@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_blog_image(form.image.data, username)
            current_user.profile_image = pic

        blog_post.title=form.tittle.data
        blog_post.text=form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post.id))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    blog_image = url_for('static', filename='blog_images/'+current_user.blog_image)
    return render_template('create_post.html', title='Updating', form=form)


@blog_posts.route('/<int:blog_post_id>/delete',methods=['POST'])
@login_required
def delete_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    
    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('core.index'))