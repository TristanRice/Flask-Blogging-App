from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
	id 			   =  db.Column(db.Integer, primary_key=True)
	username 	   =  db.Column(db.String(64), index=True, unique=True)
	email 		   =  db.Column(db.String(120), index=True, unique=True)
	password_hash  =  db.Column(db.String(128))
	about_me       =  db.Column(db.String(128))
	posts 		   =  db.relationship("Post", backref="author", lazy="dynamic")
	followed = db.relationship(
		'User', secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref = db.backref('followers', lazy='dynamic'), lazy='dynamic')

	def __repr__(self):
		return "<User: {}>".format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def set_aboutMe(self, content):
		self.about_me = content

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	def is_following(self, user):
		return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
            
class Post(db.Model):
	id 		    =  db.Column(db.Integer, primary_key=True)
	title       =  db.Column(db.String(64))
	content     =  db.Column(db.String(128))
	timestamp   =  db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id     =  db.Column(db.Integer, db.ForeignKey("user.id"))

	def __repr__(self):
		return "<Post: {}>".format(self.content)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))