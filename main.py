from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
import os
import csv

# app configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = "kkkkk"
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///invitees_tres.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# FORMS

class AreaForm(FlaskForm):
    area = SelectField(
                       choices=["Ashok Nagar", 'Thirumangalam', "ICF", "Ayinavaram", "Otteri",
                                "Chetpet", "Alwarthirunagar", "Vizhuppuram", "Pallavaram", "Others", "KV ", "IITH", "TITO", "All"])
    submit = SubmitField("Go")


# DB Tables
class areaMaster(db.Model):
    __tablename__ = "areaMaster"
    id = Column(Integer, primary_key=True)
    name = Column(String(300))

    # relationship
    invitee = relationship("inviteesMaster", back_populates="area")


class inviteesMaster(db.Model):
    __tablename__ = "inviteesMaster"
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    address = Column(String(300))
    dress = Column(Boolean)
    invitation_completed = Column(Boolean)

    # child relationship
    areaId = Column(Integer, ForeignKey("areaMaster.id"))
    area = relationship("areaMaster", back_populates="invitee")


# db.create_all()
#
area_list = ["Ashok Nagar", 'Thirumangalam', "ICF", "Ayinavaram", "Otteri",
             "Chetpet", "Alwarthirunagar", "Vizhuppuram", "Pallavaram", "Others", "KV ", "IITH", "TITO", "All"]
# #
# for i in area_list:
#     new_area = areaMaster(name=i)
#     db.session.add(new_area)
#     db.session.commit()
#
# inviteeEntries = [{"name": "Viswanathan-Gangeswari", "address": "Chetpet", "dress": True},
#                   {"name": "Vilvanan", "address": "Thirumangalam", "dress": False},
#                   {"name": "Moorthy-Kalai", "address": "ICF", "dress": True},
#                   {"name": "MKP Kumar", "address": "Otteri", "dress": False},
#                   {"name": "Dhanammal-Veerappan", "address": "Ashok Nagar", "dress": True},
#                   {"name": "Selvakumar-Malarvizhi", "address": "Alwarthirunagar", "dress": True},
#                   {"name": "Glory-Solomon", "address": "Ayinavaram", "dress": False},
#                   {"name": "Balaji Mamanar", "address": "Vizhuppuram", "dress": False},
#                   {"name": "Kandasamy", "address": "Pallavaram", "dress": False},
#                   {"name": "D Sathesh", "address": "Pallikarnai", "dress": False}]
#
# rows = []
# with open("invitees.csv", 'r') as file:
#     csvreader = csv.reader(file)
#     header = next(csvreader)
#     for row in csvreader:
#         rows.append(row)
#
# for i in rows:
#     if i[1] in area_list:
#         area_element = db.session.query(areaMaster).filter_by(name=i[1]).first()
#     else:
#         area_element = db.session.query(areaMaster).filter_by(name="Others").first()
#
#     a = None
#
#     if i[2] == "TRUE":
#         a = True
#     else:
#         a = False
#
#     new_invitee = inviteesMaster(name=i[0], address=i[1], dress=a, area=area_element,
#                                  invitation_completed=False)
#     db.session.add(new_invitee)
#     db.session.commit()


# Website routes
@app.route('/', methods=["GET", "POST"])
def cover():
    form = AreaForm()
    if form.validate_on_submit():
        if form.area.data == "All":
            invitees = db.session.query(inviteesMaster).all()
            return render_template("index1.html", form=form, state="Remaining", html=invitees)
        else:
            area = form.area.data

            area_element = db.session.query(areaMaster).filter_by(name=area).first()
            invitees = db.session.query(inviteesMaster).filter_by(areaId=area_element.id).all()

            return render_template("index1.html", form=form, state="Remaining", html=invitees)

    return render_template("index.html", form=form, state="Remaining")


@app.route('/done', methods=["GET", "POST"])
def cover_done():
    form = AreaForm()
    if form.validate_on_submit():
        if form.area.data == "All":
            invitees = db.session.query(inviteesMaster).all()
            return render_template("index2.html", form=form, state="Done", html=invitees)
        else:
            area = form.area.data

            area_element = db.session.query(areaMaster).filter_by(name=area).first()
            invitees = db.session.query(inviteesMaster).filter_by(areaId=area_element.id).all()

        return render_template("index2.html", form=form, state="Done", html=invitees)

    return render_template("index.html", form=form, state="Done")


@app.route('/done/<invitee_id>/<area>', methods=["GET", "POST"])
def done(invitee_id, area):
    form = AreaForm()
    invitee = db.session.query(inviteesMaster).filter_by(id=invitee_id).first()
    invitee.invitation_completed = True
    db.session.commit()
    area_element = db.session.query(areaMaster).filter_by(name=area).first()
    invitees = db.session.query(inviteesMaster).filter_by(areaId=area_element.id).all()
    if form.validate_on_submit():
        if form.area.data == "All":
            invitees = db.session.query(inviteesMaster).all()
            return render_template("index1.html", form=form, state="Remaining", html=invitees)
        else:
            area = form.area.data

            area_element = db.session.query(areaMaster).filter_by(name=area).first()
            invitees = db.session.query(inviteesMaster).filter_by(areaId=area_element.id).all()

            return render_template("index1.html", form=form, state="Remaining", html=invitees)

    return render_template("index1.html", form=form, state="Done", html=invitees)


@app.route('/remaining/<invitee_id>/<area>', methods=["GET", "POST"])
def remaining(invitee_id, area):
    form = AreaForm()
    invitee = db.session.query(inviteesMaster).filter_by(id=invitee_id).first()
    invitee.invitation_completed = False
    db.session.commit()
    area_element = db.session.query(areaMaster).filter_by(name=area).first()
    invitees = db.session.query(inviteesMaster).filter_by(areaId=area_element.id).all()
    if form.validate_on_submit():
        if form.area.data == "All":
            invitees2 = db.session.query(inviteesMaster).all()
            return render_template("index2.html", form=form, state="Done", html=invitees2)
        else:
            area = form.area.data

            area_element = db.session.query(areaMaster).filter_by(name=area).first()
            invitees3 = db.session.query(inviteesMaster).filter_by(areaId=area_element.id).all()

            return render_template("index2.html", form=form, state="Done", html=invitees3)
    return render_template("index2.html", form=form, state="Remaining", html=invitees)


if __name__ == "__main__":
    app.run(debug=True)
