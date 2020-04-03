# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# ------------------------f----------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#


database_name = "startup"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()




# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Team(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), primary_key=False)
    artist = db.relationship('Artist')
    venue = db.relationship('Venue')


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    deadline = db.Column(db.String, nullable=False)
    team = db.relationship('Team')


class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    team = db.relationship('Team')

db.create_all()
