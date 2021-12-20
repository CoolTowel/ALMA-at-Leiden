from flask import Flask

from flask_sqlalchemy import SQLAlchemy
import flask_login

import csv

app = Flask(__name__)

app.secret_key = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

from flask_app.models import User, Antenna, Picture, Question
from flask_app import routes

db.create_all()

# import the antenna
with app.open_resource("antennas.csv", "rt") as csvfile:
    log1 = antenna_log_already = "already exist!"
    log2 = antenna_log_success = "successfully imported!"
    antennas_csv = csv.reader(csvfile)
    for antenna in antennas_csv:
        new_antenna = Antenna(antenna_id=antenna[0],
                              name=antenna[1],
                              longitude=antenna[2],
                              latitude=antenna[3],
                              altitude=antenna[4])
        try:
            db.session.add(new_antenna)
            db.session.commit()
        except:
            antenna_log_already = str(antenna[1]) + ", " + antenna_log_already
        else:
            antenna_log_success = str(antenna[1]) + ", " + antenna_log_success

    if antenna_log_success == log2:
        print(' * Antenna Database: All antennas are already imported!')
    else:
        print(' * Antenna Database: ' + antenna_log_success)
        if antenna_log_already != log1:
            print(' * Antenna Database: ' + antenna_log_already + "\n")

# import the pictures
with app.open_resource("pictures.csv", "rt") as csvfile:
    log3 = picture_log_already = "already exist!"
    log4 = picture_log_success = "successfully imported!"
    pictures_csv = csv.reader(csvfile)
    for picture in pictures_csv:
        new_picture = Picture(name=picture[0], path=picture[1])
        new_question = Question(name=picture[0])
        try:
            db.session.add(new_picture)
            db.session.add(new_question)
            db.session.commit()
        except:
            picture_log_already = str(picture[0]) + ", " + picture_log_already
        else:
            picture_log_success = str(picture[0]) + ", " + picture_log_success

    if picture_log_success == log4:
        print(' * Picture Database: All pictures are already imported!')
    else:
        print(' * Picture Database: ' + picture_log_success)
        if picture_log_already != log3:
            print(' * Picture Database: ' + picture_log_already)
