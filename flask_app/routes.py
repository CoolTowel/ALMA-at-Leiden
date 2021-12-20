from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt

from flask_app import app, db
from flask_app.models import User, Antenna, Picture
# from flask_app.forms import PostForm


@app.route("/")
def index():
    db.create_all()
    # posts = Post.query.all()
    return render_template("index.html"
                           #    , posts=posts
                           )

import flask_app.account_manage

import flask_app.tour

import flask_app.route_test