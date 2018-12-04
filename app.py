"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)


############ USER ROUTES #############
@app.route("/")
def redirect_to_users():
    """Redirect to list of users"""
    import pdb
    pdb.set_trace()
    return redirect("/users")


@app.route("/users")
def list_users():
    """List users and show link to add form"""
    users = User.query.all()
    return render_template("index.html", users=users)


@app.route("/users/new")
def show_add_form():
    """ Show an add form for users"""
    return render_template("add_user.html")


@app.route("/users", methods=["POST"])
def process_add_form():
    """ Process add form, adding a new user, then go back to /users"""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url')

    user = User(
        first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_profile(user_id):
    """ Show information about the given user, with edit/delete options"""
    user = User.query.get_or_404(user_id)

    return render_template("profile.html", user=user)


@app.route("/users/<int:user_id>/edit")
def show_edit_form(user_id):
    """ Show an edit form for users"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def process_edit_form(user_id):
    """ Process edit form, edit user, then go back to /users """
    first_name_edit = request.form.get('first_name_edit')
    last_name_edit = request.form.get('last_name_edit')
    image_url_edit = request.form.get('image_url_edit')

    current_user = User.query.get_or_404(user_id)

    current_user.first_name = first_name_edit
    current_user.last_name = last_name_edit
    current_user.image_url = image_url_edit

    db.session.add(current_user)
    db.session.commit()

    return redirect(f"/users/{current_user.id}")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """ Delete the current user """
    current_user = User.query.get_or_404(user_id)
    db.session.delete(current_user)
    db.session.commit()

    return redirect("/users")


############ POST ROUTES #############


@app.route("/users/<int:user_id>/posts/new")
def show_add_post(user_id):
    """show form to add a new post"""
    current_user = User.query.get_or_404(user_id)

    return render_template("add_post.html", user=current_user)


@app.route("/users/<int:user_id>/posts", methods=["POST"])
def handle_add_post(user_id):
    """Handle add form; add post and redirect to user detail page"""

    title = request.form.get("title")
    content = request.form.get("content")

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show post on post detail page with post edit options"""
    post = Post.query.get(post_id)
    return render_template("post_detail.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """Show form to edit post and cancel"""

    post = Post.query.get(post_id)
    return render_template("edit_post.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def handle_post_edit(post_id):
    """Allow for post to be edited. Redirect back to post view"""

    edit_title = request.form.get('edit-title')
    edit_content = request.form.get('edit-content')

    current_post = Post.query.get(post_id)

    current_post.title = edit_title
    current_post.content = edit_content

    db.session.add(current_post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete instance of post"""

    current_post = Post.query.get(post_id)
    temp = current_post.user_id
    db.session.delete(current_post)
    db.session.commit()

    return redirect(f"/users/{temp}")


############ TAG ROUTES #############


@app.route("/tags")
def list_tags():
    """ List all tags, with links to tag detail page"""
    tags = Tag.query.all()
    return render_template("list_tag.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    """" Show detail about a tag and be able to edit/delete """
    tag = tag.query.get(tag_id)
    render_template("tag_detail.html", tag=tag)
