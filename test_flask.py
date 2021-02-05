from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for Users."""

    def setUp(self):
        """Create sample user."""

        User.query.delete()
        Post.query.delete()

        user = User(f_name="Bob", l_name="Ross", img_url='http://www.newdesignfile.com/postpic/2009/09/generic-user-icon-windows_354183.png')
        post = Post(title="Happy little trees", content="Check out my latest painting!", user_id=user.id)
        # tag = Tag(name="#happylittletrees", post_tags=post.id)
        db.session.add(user)
        db.session.add(post)
        # db.session.add(tag)
        db.session.commit()

        self.id = user.id

    def tearDown(self):
        """Clean up."""

        db.session.rollback()

# ********************* USER TESTS *********************
    def test_list_user(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Bob', html)

    def test_add_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>Create a user</h3>', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id}")
            html = resp.get_data(as_text=True) 

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Bob Ross</h1>', html)

    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>Edit user</h3>', html)
    
    # ********************* POST TESTS *********************
    def test_render_post(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>Add post</h3>', html)

    # ********************* TAG TESTS *********************
    def test_show_tag_form(self):
        with app.test_client() as client:
            resp = client.get("/tags/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<input name="tag_name"></p>', html)
