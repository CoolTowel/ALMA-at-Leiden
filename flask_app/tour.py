from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt

from flask_app import app, db
from flask_app.models import User, Antenna, Picture, Question

import json, csv
with app.open_resource("static/texts.json", "rt") as jsonfile:
    full_texts = json.load(jsonfile)




# check if user has checked
def checked_in(user, antenna_name):
    antennas = user.antennas
    for antenna in antennas:
        if antenna_name == antenna.name:
            return True
    # if no matching
    return False


# check if user answered the question
def this_current_question_answered(user, picture_name):
    pictures = user.pictures
    for picture in pictures:
        if picture_name == picture.name:
            return True
    # if no matching
    return False

with app.open_resource("pictures.csv", "rt") as csvfile:
    pictures_csv = csv.reader(csvfile)
    antenna_name_sequence = []
    for picture in pictures_csv:
        antenna_name_sequence.append(picture[0])
    antenna_name_sequence_reverse = antenna_name_sequence.reverse()

def check_user_current(user):
    antennas = user.antennas
    for all_antenna in antenna_name_sequence:
        for user_antenna in antennas:
            if user_antenna.name == all_antenna:
                return all_antenna
    raise ValueError("no current antenna yet")
    
        
    
# # check if user has answered this quesiton correctly
# def answered_correctly(user, question_name):
#     questions = user.questions
#     for question in questions:
#         if question_name == question.name:
#             return True
#     return False

@app.route("/tour-info")
def tour_info():
    return render_template("tour-info.html")

@app.route("/tour-start")
@login_required
def tour_start():
    try:
        user = current_user
        current_antenna = check_user_current(user)
    except:
        return render_template("tour-start.html")
    else:
        return redirect("/tour/full/" + str(current_antenna))
    
@app.route("/tour/full/<antenna_input>", methods=['GET', 'POST'])
@login_required
def tour_full(antenna_input):
    user = current_user
    antenna_name = picture_name = str(antenna_input)  # 图片的ID（因为图片的区别是baseline不同所以用baseline来表示

    this_page = "/tour/full/" + antenna_name
    
    antenna = Antenna.query.filter(Antenna.name == antenna_name).first()
    
    picture = Picture.query.filter(Picture.name == picture_name).first()
    picture_path = picture.path
    
    question = Question.query.filter(Question.name == picture_name).first()
    
    checkin_question = full_texts[antenna_name]["checkin_question"]
    checkin_options = full_texts[antenna_name]["checkin_options"]
    checkin_answer = full_texts[antenna_name]["checkin_answer"]
    post_check = full_texts[antenna_name]["post_check"]
    astro_question = full_texts[antenna_name]["astro_question"]
    astro_options = full_texts[antenna_name]["astro_options"]
    astro_answer = full_texts[antenna_name]["astro_answer"]

    if checked_in(user=user, antenna_name=antenna_name):
        checkin_status = True
    else:
        checkin_status = False

    if this_current_question_answered(user=user, picture_name=picture_name):
        picture_usable = True
    else:
        picture_usable = False
        
    # if answered_correctly(user=user, question_name=picture_name):
    #     answered_correctly_status = True
    # else:
    #     answered_correctly_status = False

    if request.method == 'GET':
        return render_template(this_page + ".html",
                               this_page = this_page,
                               checkin_status=checkin_status,
                               picture_usable=picture_usable,
                               path=picture_path,
                               checkin_question=checkin_question,
                               checkin_options=checkin_options,
                               checkin_answer=checkin_answer,
                               post_check = post_check,
                               astro_question=astro_question,
                               astro_options=astro_options,
                               astro_answer=astro_answer,
                            #    answered_correctly=answered_correctly_status
                               )
    else:
        if not checkin_status: 
            answer = request.form.get(checkin_question)
            if answer == checkin_answer:
                user.antennas.append(antenna)
                db.session.commit()
                # checkin_status = True
                flash("Checked in!", "info")
                return redirect(this_page)
            else:
                flash("Wrong answer!", "danger")
                return redirect(this_page)
        else:
            answer = request.form.get(astro_question)
            if answer is not None:
                pass
            else:
                flash("You've already checked in.", "info")
                return redirect(this_page)
            if answer == astro_answer:
                user.pictures.append(picture)
                # user.questions.append(question)
                db.session.commit()
                picture_usable = True
                flash("Correct!", "info")
                return redirect(this_page)
            else:
                user.pictures.append(picture)
                db.session.commit()
                picture_usable = True
                flash("Wrong!", "danger")
                return redirect(this_page)

@app.route("/tour/full/final-314159")
@login_required
def tour_final():
    return render_template("/tour/full/final-314159.html")