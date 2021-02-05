"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, PostTag, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = '123ABC'


# ******************** USER ROUTES ********************
@app.route("/")
def homepage():
    """Redirect to list of users."""
    return redirect("/users")


@app.route("/users")
def list_users():
    """Show all users."""

    users = User.query.all()
    tags = Tag.query.all()
    return render_template("user_list.html", users=users, tags=tags)


@app.route("/users/new", methods=["GET"])
def add_user_form():
    """Show an add form for users"""
    return render_template('new.html')


@app.route("/users/new", methods=["POST"])
def add_user():
    """Handle new user submission"""

    f_name = request.form['f_name']
    l_name = request.form['l_name']
    img_url = request.form['profile_img']

    user = User(f_name=f_name, l_name=l_name, img_url=img_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route("/users/<int:id>")
def show_user(id):
    """Show information about the given user."""
    posts = Post.query.filter_by(user_id=id)
    user = User.query.get_or_404(id)
    return render_template("profile.html", user=user, posts=posts)


@app.route("/users/<int:id>/edit")
def render_edit(id):
    """Render edit form"""
    user = User.query.get_or_404(id)
    return render_template('edit.html', user=user)


@app.route("/users/<int:id>/edit", methods=["POST"])
def edit_user(id):
    """Process the edit form, returning the user to the /users page."""

    user = User.query.get_or_404(id)
    user.f_name = request.form['edit_f_name']
    user.l_name = request.form['edit_l_name']
    user.img_url = request.form['edit_profile_img']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')
    

@app.route("/users/<int:id>/delete")
def delete_user(id):
    """Delete the user."""

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


# ******************** POST ROUTES ********************
@app.route("/users/<int:id>/posts/new")
def render_post(id):
    """Render new post form"""
    # post = Post.query.get_or_404(id)
    user = User.query.get_or_404(id)
    tags = Tag.query.all()
    return render_template('add_post.html', user=user, tags=tags)


@app.route("/users/<int:id>/posts/new", methods=["POST"])
def add_post(id):
    """Add new user post, redirect to /users page."""

    tag_ids = [int(num) for num in request.form.getlist('tag_list')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(title=request.form['post_title'], content=request.form['post_content'], user_id=id, post_tags=tags)
    db.session.add(post)
    db.session.commit()

    
    return redirect(f"/users/{id}")


@app.route("/post/<int:id>")
def show_post(id):
    """Show a post."""
    post = Post.query.get_or_404(id)
    user = User.query.get_or_404(post.user_id)
    return render_template("post.html", post=post, user=user)
    

@app.route("/post/<int:id>/edit")
def render_edit_post(id):
    """Render edit post form."""
    post = Post.query.get_or_404(id)
    user = User.query.get_or_404(post.user_id)
    tags = Tag.query.all()

    return render_template('edit_post.html', post=post, tags=tags, user=user)


@app.route("/post/<int:id>/edit", methods=["POST"])
def submit_edit_post(id):
    """Handle editing of a post. Redirect back to the post view."""

    post = Post.query.get_or_404(id)
    post.title = request.form['edit_title']
    post.content = request.form['edit_post_content']

    tag_ids = [int(num) for num in request.form.getlist('edit_tag_list')]
    post.post_tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/post/{id}')


@app.route("/post/<int:id>/delete")
def delete_post(id):
    """Delete the post."""

    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


# ******************** TAG ROUTES ********************
@app.route("/tags/<int:id>")
def tag_detail(id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(id)

    return render_template("tag.html", tag=tag)


@app.route("/tags/new")
def show_tag_form():
    """Shows a form to add a new tag."""
    return render_template("new_tag.html")


@app.route("/tags/new", methods=["POST"])
def process_tag_form():
    """Process add form, adds tag, and redirect to tag list."""

    tag = Tag(name=request.form['tag_name'])

    db.session.add(tag)
    db.session.commit()

    return redirect("/")


@app.route("/tags/<int:id>/edit")
def show_tag_edit(id):
    """Show edit form for a tag."""

    tag = Tag.query.get_or_404(id)

    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:id>/edit", methods=["POST"])
def process_tag_edit(id):
    """Process edit form, edit tag, and redirects to the tags list."""

    tag = Tag.query.get_or_404(id)
    tag.name = request.form['edit_tag_name']

    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/{id}')


@app.route("/tags/<int:id>/delete")
def delete_tag(id):
    """Delete a tag."""

    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/users")