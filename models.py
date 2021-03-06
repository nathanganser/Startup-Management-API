import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql
import json
from config import database_path

# database_path is imported from config & hidden for security reasons.




db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    deadline = db.Column(db.String, nullable=False)
    team = db.relationship('Team')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def show(self):
        teams = Team.query.filter_by(project_id=self.id).all()
        team_members = []
        for member in teams:
            team_members.append(member.member_id)
        return {
            'id': self.id,
            'name': self.name,
            'deadline': self.deadline,
            'team': team_members
        }


class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    role = db.Column(db.String)
    team = db.relationship('Team')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), primary_key=False)
    member = db.relationship('Member')
    project = db.relationship('Project')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
