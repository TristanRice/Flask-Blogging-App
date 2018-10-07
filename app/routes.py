#!/usr/bin/python3

#################################################################
from flask import render_template, flash, redirect, url_for     #
from app import app, db											#
from app.forms import *											#
from flask_login import current_user, login_user, logout_user   #
from app.models import *	 									#
#################################################################

@app.route("/")
def root( ):

	return redirect(url_for("index"))

@app.route("/test")
def test( ):

	return render_template("base.html")
	
@app.route("/index")
def index( ):
	user = {"username":"Tristan"}
	post = [
		{
			"author":{
				"username":"A"
			},
			"body": "aaa"
		},
		{
			"author":{
				"username":"B"
			},
			"body":"bbbb"
		}
	]

	return render_template("index.html", title="Home", user=user, posts=post)

@app.route("/login", methods=["GET", "POST"])
def login( ):
	if current_user.is_authenticated:
		return redirect(url_for("index"))
	form = Loginform( )
	if form.validate_on_submit( ):
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash("Invalid username or password")
			return redirect(url_for("login"))
		login_user(user)
		return redirect(url_for("index"))

	return render_template("login.html", title="Sign in", form=form)

@app.route("/logout")
def logout( ):
	logout_user( )

	return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register( ):
	form = RegisterForm( )
	if form.validate_on_submit( ):
		user = User(username=form.username.data, email=form.email.data) #make ORM model
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit( )
		flash("Now please log in")
		return redirect(url_for("login"))

	return render_template("register.html", title="Register", form=form)

@app.route("/make/post", methods=["GET", "POST"])
def makepost( ):
	if not current_user.is_authenticated:
		flash("You must be looged in to make a post")
		return redirect(url_for("index"))
	form = BlogPostForm( )
	if form.validate_on_submit( ):
		post = Post(title=form.title.data, content=form.content.data, user_id=current_user.get_id( ))
		db.session.add(post)
		db.session.commit( )
		flash("Your post has been added")
		return redirect(url_for("index"))

	return render_template("blogpost.html", title="MakePost", author=current_user, form=form)

@app.route("/user/<username>", methods=["GET"])
def user( username ):
	user = User.query.filter_by(username=username).first_or_404( )
	posts = user.posts.all( )
	return render_template("user.html", title=user.username, user=user, posts=posts)

@app.errorhandler(404)
def page404( e ):
	#ToDo: decide whether to route them back to the index apge or just show a normal 404
	return render_template("404.html")

@app.route("/editprofile/<username>", methods=["GET", "POST"])
def editprofile( username ):
	user = User.query.filter_by(username=username).first_or_404( )
	
	if not current_user.username == user.username:
		flash("You cannot edit another users profile")
		return redirect(url_for("index"))

	form = EditProfileForm( )
	if form.validate_on_submit( ):
		user = User.query.filter_by(username=username).first_or_404( )
		user.about_me = form.aboutMe.data
		db.session.commit( )
		flash("Your profile has been updated")
		return redirect(url_for("index"))
		
	return render_template( "editprofile.html", title="Edit Profile", form=form )

@app.route("/follow/<username>")
def follow( username ):
	follow  = User.query.filter_by(username=username).first_or_404( )
	if current_user.username==follow.username:
		flash("You cannot follow yourself")
		return redirect(url_for("index"))
	current_user.follow(follow)
	flash("You are now following {}".format(follow.username))
	return redirect(url_for("index"))

@app.route("/unfollow/<username>")
def unfollow( username ):
	unfollow = User.query.filter_by(username=username).first_or_404( )
	current_user.unfollow(unfollow)
	db.session.commit( )
	flash("User unfollowed")
	return redirect(url_for("index"))

@app.route("/see/folowers/<username>")
def seefolowers( username ):
	user      = User.query.filter_by(username=username).first_or_404( )
	followers = user.followed.all( )

	return render_template("followerlist.html", user=user, followers=followers)


