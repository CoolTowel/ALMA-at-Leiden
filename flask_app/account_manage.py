from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt

from flask_app import app, db
from flask_app.models import User, Antenna, Picture


# Check if username or email are already taken
def user_exsists(username, email):
    # Get all Users in SQL
    users = User.query.all()
    for user in users:
        if username == user.username or email == user.email:
            return True

    # No matching user
    return False


@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('register.html')

    else:
        # Create user object to insert into SQL
        passwd1 = request.form.get('password1')
        passwd2 = request.form.get('password2')

        if passwd1 != passwd2 or passwd1 == None:
            flash('Password Error!', 'danger')
            return render_template('register.html')

        hashed_pass = sha256_crypt.encrypt(str(passwd1))

        new_user = User(username=request.form.get('username'),
                        email=request.form.get('username'),
                        password=hashed_pass)

        if user_exsists(new_user.username, new_user.email):
            flash('User already exsists!', 'danger')
            return render_template('register.html')
        else:
            # Insert new user into SQL
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            flash('Account created!', 'success')
            return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        username = request.form.get('username')
        password_candidate = request.form.get('password')

        # Query for a user with the provided username
        result = User.query.filter_by(username=username).first()

        # If a user exsists and passwords match - login
        if result is not None and sha256_crypt.verify(password_candidate,
                                                      result.password):

            # Init session vars
            login_user(result)
            flash('Logged in!', 'success')
            return redirect(url_for('index'))

        else:
            flash('Incorrect Login!', 'danger')
            return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out!', 'success')
    return redirect(url_for('index'))


@app.route("/antenna", methods=['GET', 'POST'])
@login_required
def antenna():
    if request.method == 'GET':
        return render_template('antenna.html')

    else:
        # Create relationship to insert into SQL
        antenna_id = request.form.get('antenna_id')
        user_new_antenna = Antenna.query.filter(
            Antenna.antenna_id == str(antenna_id)).first()

        if user_new_antenna == None:
            flash("Antenna doesn't exsist!", 'danger')
            return render_template('antenna.html')
        else:
            user = current_user
            user.antennas.append(user_new_antenna)
            db.session.commit()

            flash('Antenna collected!', 'success')
            return redirect(url_for('antenna-list'))


@app.route("/antenna-list")
@login_required
def antenna_list():
    user = current_user
    antennas = user.antennas
    return render_template("antenna-list.html", antennas=antennas)


@app.route("/antenna-more")
def antenna_more():
    return render_template("antenna-more.html")


@app.route("/all-antenna")
def all_antenna():
    return render_template("all-antenna.html")


@app.route("/account")
@login_required
def account():
    user = current_user
    user_name = user.username
    antennas = user.antennas
    i = 0
    for antenna in antennas:
        i += 1
    return render_template("account.html",
                           antennas=antennas,
                           user_name=user_name,
                           antenna_number=i)
