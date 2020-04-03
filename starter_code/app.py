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
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

    areas = Venue.query.distinct('city', 'state').all()
    data = []
    for area in areas:
        venues = Venue.query.filter(Venue.city == area.city, Venue.state == area.state).all()
        record = {
            'city': area.city,
            'state': area.state,
            'venues': [venue.get_venue() for venue in venues],
        }
        data.append(record)
    return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():

    search_term = request.form.get('search_term')
    search = "%{}%".format(search_term)
    response = Venue.query.filter(Venue.name.ilike(search)).all()
    response_length = len(response)
    return render_template('pages/search_venues.html', results=response, response_length=response_length,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

    real_data = Venue.query.filter_by(id=venue_id).one()
    return render_template('pages/show_venue.html', venue=real_data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        phone = request.form.get('phone')
        genres = request.form.getlist('genres')
        facebook_link = request.form.get('facebook_link')

        new_venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres,
                          facebook_link=facebook_link)

        db.session.add(new_venue)
        db.session.commit()

        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    except:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        db.session.rollback()

    finally:
        return render_template('pages/home.html')


@app.route('/venues/<int:venue_id>', methods=['GET', 'POST'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.filter_by(id=venue_id).one()
        shows = Show.query.filter_by(venue_id=venue_id).all()
        for show in shows:
            db.session.delete(show)
        db.session.delete(venue)
        db.session.commit()
        flash('Venue was properly deleted')

    except:
        db.session.rollback()
        flash('Venue ' + venue.name + " could not be deleted")

    finally:
        return render_template('pages/home.html')


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    return render_template('pages/artists.html', artists=Artist.query.order_by('name').all())


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term')
    search = "%{}%".format(search_term)
    response = Artist.query.filter(Artist.name.ilike(search)).all()
    resplen = len(response)
    return render_template('pages/search_artists.html', results=response, resplen=resplen,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

    artist = Artist.query.filter_by(id=artist_id).one()
    artist.upcoming_shows_count = 0
    artist.past_shows_count = 0
    artist.upcoming_shows = []
    artist.past_shows = []

    today = datetime.now()
    print(today)
    for show in artist.shows:
        show_time = parser.parse(show.start_time)
        if show_time > today:
            artist.upcoming_shows_count += 1
            artist.upcoming_shows.append(show)
        else:
            artist.past_shows_count += 1
            artist.past_shows.append(show)

    return render_template('pages/show_artist.html', artist=artist)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    try:
        artist = Artist.query.filter_by(id=artist_id).first()
        form = ArtistForm(obj=artist)

        real_artist = Artist.query.filter_by(id=artist_id).one()
        return render_template('forms/edit_artist.html', form=form, artist=real_artist)

    except:
        flash('There was an error accessing this artist page ' + artist.name)
        return render_template('index.html')


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        artist_to_edit = Artist.query.filter_by(id=artist_id).first()

        artist_to_edit.name = request.form.get('name')
        artist_to_edit.city = request.form.get('city')
        artist_to_edit.state = request.form.get('state')
        artist_to_edit.phone = request.form.get('phone')
        artist_to_edit.genres = request.form.getlist('genres')
        artist_to_edit.image_link = request.form.get('image_link')
        artist_to_edit.facebook_link = request.form.get('facebook_link')

        db.session.add(artist_to_edit)
        db.session.commit()
        # artist record with ID <artist_id> using the new attributes
        flash('Artist ' + artist_to_edit.name + ' was successfully updated!')

    except:
        flash('There was an issue updating artist: ' + artist_to_edit.name)

    finally:
        return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.filter_by(id=venue_id).first()
    form = VenueForm(obj=venue)

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        venue_to_edit = Venue.query.filter_by(id=venue_id).first()
        venue_to_edit.name = request.form.get('name')
        venue_to_edit.city = request.form.get('city')
        venue_to_edit.state = request.form.get('state')
        venue_to_edit.address = request.form.get('address')
        venue_to_edit.phone = request.form.get('phone')
        venue_to_edit.genres = request.form.getlist('genres')
        venue_to_edit.facebook_link = request.form.get('facebook_link')

        db.session.add(venue_to_edit)
        db.session.commit()
        # venue record with ID <venue_id> using the new attributes
        flash(venue_to_edit.name + " was successfully updated")

    except:
        flash("There was an error updating Venue: " + venue_to_edit.name)

    finally:
        return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        # called upon submitting the new artist listing form
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')

        phone = request.form.get('phone')
        genres = request.form.getlist('genres')
        image_link = request.form.get('image_link')
        facebook_link = request.form.get('facebook_link')

        new_artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, image_link=image_link,
                            facebook_link=facebook_link)
        db.session.add(new_artist)
        db.session.commit()

        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')

    except:
        flash("There was an issue while creating a new artist")

    finally:
        return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # shows are ordered by coming soon

    shows = Show.query.order_by('start_time').all()

    return render_template('pages/shows.html', shows=shows)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    try:

        venue_id = request.form.get('venue_id')
        artist_id = request.form.get('artist_id')
        start_time = request.form.get('start_time')

        venue = Venue.query.filter_by(id=venue_id).first()

        artist = Artist.query.filter_by(id=artist_id).first()
        show = Show(start_time=start_time)
        show.artist = artist
        show.venue = venue
        venue.shows.append(show)
        artist.shows.append(show)


        db.session.commit()


        flash('Show was successfully listed!')


    except:
        flash('There was an error while listing this show!')

    finally:
        return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
