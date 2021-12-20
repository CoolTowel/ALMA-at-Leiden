from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt

from flask_app import app, db
from flask_app.models import User, Antenna, Picture

from flask.views import View


class Test(View):
    @login_required  
    def dispatch_request(self, test_opt='1', test_opt2='2'):
        return render_template('test.html', test_opt=test_opt, test_opt2=test_opt2)


app.add_url_rule('/test1', view_func=Test.as_view('test23'))
app.add_url_rule('/test2', view_func=Test.as_view('test2', test_opt='3', test_opt2='4'))
