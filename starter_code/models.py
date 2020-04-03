# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
from time import strftime

import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import literal, Table, table, insert
from datetime import datetime
from sqlalchemy import extract
from dateutil import parser

from forms import *
from flask_migrate import Migrate

# ------------------------f----------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Member(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), primary_key=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=False)
    artist = db.relationship('Artist')
    venue = db.relationship('Venue')


class Project(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    deadline = db.Column(db.String, nullable=False)
    members = db.relationship('Member')

    def get_venue(self):
        return {
            'id': self.id,

            'name': self.name,

            'num_upcoming_shows': 2
        }


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show')
