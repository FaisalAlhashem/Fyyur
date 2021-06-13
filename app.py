#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.orm import backref, session
from sqlalchemy.sql.expression import null
from forms import *
from datetime import datetime
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Genres(db.Model):
    __tablename__ = 'Genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)


class States(db.Model):
    __tablename__ = 'States'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)


class Show(db.Model):
    __tablename__ = 'Shows'

    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'Venue.id'), primary_key=True)
    time = db.Column(db.String, nullable=False, primary_key=True)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120), default='no Website')
    facebook_link = db.Column(db.String(120), default='no Facebook')
    seeking_artist = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', backref='Venue', lazy=True)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120), default=None)
    facebook_link = db.Column(db.String(120), default=None)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', backref='Artist', lazy=True)


# this method will seed the States and Genres tables with data
# how to use: in terminal cd into file dir and enter the python3 mode
# then enter "from app import db , Genre, States, dbSeed"
# then run dbSeed()
def dbSeed():
    if len(Genres.query.all()) == 0:
        genres = [Genres(name='Alternative'),
                  Genres(name='Blues'),
                  Genres(name='Classical'),
                  Genres(name='Country'),
                  Genres(name='Electronic'),
                  Genres(name='Folk'),
                  Genres(name='Funk'),
                  Genres(name='Hip-Hop'),
                  Genres(name='Heavy Metal'),
                  Genres(name='Instrumental'),
                  Genres(name='Jazz'),
                  Genres(name='Musical Theatre'),
                  Genres(name='Pop'),
                  Genres(name='Punk'),
                  Genres(name='R&B'),
                  Genres(name='Reggae'),
                  Genres(name='Rock n Roll'),
                  Genres(name='Soul'),
                  Genres(name='Other')]

        db.session.add_all(genres)
    if len(States.query.all()) == 0:
        states = [States(name='AL'),
                  States(name='AK'),
                  States(name='AZ'),
                  States(name='AR'),
                  States(name='CA'),
                  States(name='CO'),
                  States(name='CT'),
                  States(name='DE'),
                  States(name='DC'),
                  States(name='FL'),
                  States(name='GA'),
                  States(name='HI'),
                  States(name='ID'),
                  States(name='IL'),
                  States(name='IN'),
                  States(name='IA'),
                  States(name='KS'),
                  States(name='KY'),
                  States(name='LA'),
                  States(name='ME'),
                  States(name='MT'),
                  States(name='NE'),
                  States(name='NV'),
                  States(name='NH'),
                  States(name='NJ'),
                  States(name='NM'),
                  States(name='NY'),
                  States(name='NC'),
                  States(name='ND'),
                  States(name='OH'),
                  States(name='OK'),
                  States(name='OR'),
                  States(name='MD'),
                  States(name='MA'),
                  States(name='MI'),
                  States(name='MN'),
                  States(name='MS'),
                  States(name='MO'),
                  States(name='PA'),
                  States(name='RI'),
                  States(name='SC'),
                  States(name='SD'),
                  States(name='TN'),
                  States(name='TX'),
                  States(name='UT'),
                  States(name='VT'),
                  States(name='VA'),
                  States(name='WA'),
                  States(name='WV'),
                  States(name='WI'),
                  States(name='WY')]
        db.session.add_all(states)
    if len(Venue.query.all()) == 0:
        venues = [
            Venue(
                id=1,
                name='The Musical Hop',
                city='San Francisco',
                state='CA',
                address='1015 Folsom Street',
                phone='123-123-1234',
                genres='Jazz, Reggae, Swing, Classical, Folk',
                image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
                website_link='https://www.themusicalhop.com/',
                facebook_link='https://www.facebook.com/TheMusicalHop',
                seeking_artist=True,
                seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us."
            ),
            Venue(
                id=2,
                name='The Dueling Pianos Bar',
                city='New York',
                state='NY',
                address='335 Delancey Street',
                phone='914-003-1132',
                genres='Classical, R&B, Hip-Hop',
                image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',
                website_link='https://www.theduelingpianos.com/',
                facebook_link='https://www.facebook.com/theduelingpianos'
            ),
            Venue(
                id=3,
                name='Park Square Live Music & Coffee',
                city='San Francisco',
                state='CA',
                address='34 Whiskey Moore Ave',
                phone='415-000-1234',
                genres='Rock n Roll, Jazz, Classical, Folk',
                image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
                website_link='https://www.parksquarelivemusicandcoffee.com/',
                facebook_link='https://www.facebook.com/ParkSquareLiveMusicAndCoffee'
            )
        ]
        db.session.add_all(venues)

    if len(Artist.query.all()) == 0:
        artists = [
            Artist(
                id=4,
                name=' Guns N Petals ',
                city='San Francisco',
                state='CA',
                phone=' 326-123-5000 ',
                genres=' Rock n Roll ',
                seeking_venue=True,
                seeking_description='Looking for shows to perform at in the San Francisco Bay Area!',
                image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
                website_link='https://www.gunsnpetalsband.com/',
                facebook_link='https://www.facebook.com/GunsNPetals'
            ),
            Artist(
                id=5,
                name=' Matt Quevedo ',
                city='New York',
                state='NY',
                phone=' 300-400-5000 ',
                genres=' Jazz ',
                image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
                facebook_link='https://www.facebook.com/mattquevedo923251523'
            ),
            Artist(
                id=6,
                name=' The Wild Sax Band ',
                city='San Francisco',
                state='CA',
                phone=' 432-325-5432 ',
                genres='Jazz, Classical',
                image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
            )
        ]
        db.session.add_all(artists)
    if len(Show.query.all()) == 0:
        shows = [
            Show(
                venue_id=1,
                artist_id=4,
                time="2019-05-21T21:30:00.000Z"
            ),
            Show(
                venue_id=3,
                artist_id=5,
                time="2019-06-15T23:00:00.000Z"
            ),
            Show(
                venue_id=3,
                artist_id=6,
                time="2035-04-01T20:00:00.000Z"
            ),
            Show(
                venue_id=3,
                artist_id=6,
                time="2035-04-08T20:00:00.000Z"
            ),
            Show(
                venue_id=3,
                artist_id=6,
                time="2035-04-15T20:00:00.000Z"
            )]
        db.session.add_all(shows)
    db.session.commit()
    print('database seeded')


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@ app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@ app.route('/venues')
def venues():
    data = []
    Queries = db.session.query(Venue).order_by('id').all()
    locations = {}
    now = datetime.now()
    now = now.strftime("%Y-%m-%dT%H:%M:%S")
    for query in Queries:
        locations[query.city] = query.state

    for location in locations:
        venues = []
        state = locations[location]
        allVenues = db.session.query(Venue).filter_by(
            state=state, city=location).all()

        for venue in allVenues:
            shows = Show.query.filter(
                Show.venue_id == venue.id, Show.time > now).count()
            print(venue.name, shows)
            diction = {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": shows
            }

            venues.append(diction)
        row = {
            "city": location,
            "state": state,
            "venues": venues
        }
        data.append(row)
    return render_template('pages/venues.html', areas=data)


@ app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    search = "%"+search_term+"%"
    results = Venue.query.filter(Venue.name.ilike(search)).all()
    data = []
    now = datetime.now()
    now = now.strftime("%Y-%m-%dT%H:%M:%S")
    for result in results:
        shows = Show.query.filter(
            Show.venue_id == result.id, Show.time > now).count()
        print(result.name, shows)
        row = {
            "id": result.id,
            "name": result.name,
            "num_upcoming_shows": shows
        }
        data.append(row)

    response = {
        "count": len(results),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@ app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    now = datetime.now()
    now = now.strftime("%Y-%m-%dT%H:%M:%S")
    venue = Venue.query.get(venue_id)
    shows = venue.shows
    past_shows = []
    upcoming_shows = []
    for show in shows:
        row = {
            "artist_id": show.artist_id,
            "artist_name": show.Artist.name,
            "artist_image_link": show.Artist.image_link,
            "start_time": show.time
        }
        if show.time < now:
            past_shows.append(row)
        else:
            upcoming_shows.append(row)
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres.rsplit(", "),
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_artist,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@ app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@ app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        name = request.form.get("name")
        city = request.form.get("city")
        state = request.form.get("state")
        address = request.form.get("address")
        phone = request.form.get("phone")
        genresArray = request.form.getlist("genres")
        genres = ''
        for genre in genresArray:
            genres = genres + genre + ", "
        image_link = request.form.get("image_link")
        website_link = request.form.get("website_link")
        facebook_link = request.form.get("facebook_link")
        seeking_artist = request.form.get("seeking_talent")
        if seeking_artist == 'y':
            seeking_artist = True
        else:
            seeking_artist = False
        seeking_description = request.form.get("seeking_description")
        print(id, name, city, state, address, phone, genres,
              seeking_artist, seeking_description)
        venue = Venue(
            name=name,
            city=city,
            state=state,
            address=address,
            phone=phone,
            genres=genres,
            image_link=image_link,
            website_link=website_link,
            facebook_link=facebook_link,
            seeking_artist=seeking_artist,
            seeking_description=seeking_description
        )
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + name + ' was successfully listed!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Venue '+name+' could not be listed.')
        abort(500)
    finally:
        db.session.close()
    return render_template('pages/home.html')


@ app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash("venue "+venue.name+" has been deleted successfully")
    except:
        flash('something went wrong')
        print(sys.exc_info())
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()
    return jsonify({'sucess': True})


@ app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    genres = venue.genres.rsplit(', ')
    website = venue.website_link
    facebook = venue.facebook_link
    description = venue.seeking_description
    if facebook == 'None':
        facebook = ""
    if description == 'None':
        description = ""
    if website == 'None':
        website = ""
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.genres.data = genres
    form.facebook_link.data = facebook
    form.image_link.data = venue.image_link
    form.website_link.data = venue.website_link
    form.seeking_talent.data = venue.seeking_artist
    form.seeking_description.data = venue.seeking_description
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@ app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    try:
        venue.name = request.form.get("name")
        venue.city = request.form.get("city")
        venue.state = request.form.get("state")
        venue.address = request.form.get("address")
        venue.phone = request.form.get("phone")
        genresArray = request.form.getlist("genres")
        print(genresArray)
        genres = genresArray[0]
        if len(genresArray) > 1:
            i = 1
            while i < len(genresArray):
                genres = genres + ", " + genresArray[i]
                i += 1
        venue.genres = genres
        venue.image_link = request.form.get("image_link")
        venue.website_link = request.form.get("website_link")
        venue.facebook_link = request.form.get("facebook_link")
        seeking_artist = request.form.get("seeking_talent")
        if seeking_artist == 'y':
            venue.seeking_artist = True
        else:
            venue.seeking_artist = False
        venue.seeking_description = request.form.get("seeking_description")
        print(venue.genres)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully Modfiyed!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Venue '+venue.name+' could not be Modfiyed.')
        abort(500)
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Artists
#  ----------------------------------------------------------------
@ app.route('/artists')
def artists():
    data = []
    Queries = db.session.query(Artist).order_by('id').all()
    for artist in Queries:
        diction = {
            "id": artist.id,
            "name": artist.name,
        }
        data.append(diction)
    return render_template('pages/artists.html', artists=data)


@ app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    search = "%"+search_term+"%"
    results = Artist.query.filter(Artist.name.ilike(search)).all()
    data = []
    now = datetime.now()
    now = now.strftime("%Y-%m-%dT%H:%M:%S")
    for result in results:
        shows = Show.query.filter(
            Show.venue_id == result.id, Show.time > now).count()
        print(result.name, shows)
        row = {
            "id": result.id,
            "name": result.name,
            "num_upcoming_shows": 0
        }
        data.append(row)

    response = {
        "count": len(results),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@ app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    now = datetime.now()
    now = now.strftime("%Y-%m-%dT%H:%M:%S")
    artist = Artist.query.get(artist_id)
    shows = artist.shows
    past_shows = []
    upcoming_shows = []
    for show in shows:
        row = {
            "venue_id": show.venue_id,
            "venue_name": show.Venue.name,
            "venue_image_link": show.Venue.image_link,
            "start_time": show.time
        }
        if show.time < now:
            past_shows.append(row)
        else:
            upcoming_shows.append(row)
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.rsplit(", "),
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@ app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    genres = artist.genres.rsplit(', ')
    website = artist.website_link
    facebook = artist.facebook_link
    description = artist.seeking_description
    if facebook == 'None':
        facebook = ""
    if description == 'None':
        description = ""
    if website == 'None':
        website = ""
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = genres
    form.facebook_link.data = facebook
    form.image_link.data = artist.image_link
    form.website_link.data = artist.website_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@ app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)
    try:
        artist.name = request.form.get("name")
        artist.city = request.form.get("city")
        artist.state = request.form.get("state")
        artist.phone = request.form.get("phone")
        genresArray = request.form.getlist("genres")
        print(genresArray)
        genres = genresArray[0]
        if len(genresArray) > 1:
            i = 1
            while i < len(genresArray):
                genres = genres + ", " + genresArray[i]
                i += 1
        artist.genres = genres
        artist.image_link = request.form.get("image_link")
        artist.website_link = request.form.get("website_link")
        artist.facebook_link = request.form.get("facebook_link")
        seeking_artist = request.form.get("seeking_venue")
        if seeking_artist != None:
            artist.seeking_venue = True
        else:
            artist.seeking_venue = False
        artist.seeking_description = request.form.get("seeking_description")
        print(artist.genres)
        db.session.commit()
        flash('artist ' + request.form['name'] + ' was successfully Modfiyed!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Artist ' +
              artist.name+' could not be Modfiyed.')
        abort(500)
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------


@ app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    try:
        name = request.form.get("name")
        city = request.form.get("city")
        state = request.form.get("state")
        phone = request.form.get("phone")
        genresArray = request.form.getlist("genres")
        genres = ''
        for genre in genresArray:
            genres = genres + genre + ", "
        image_link = request.form.get("image_link")
        website_link = request.form.get("website_link")
        facebook_link = request.form.get("facebook_link")
        seeking_venue = request.form.get("seeking_venue")
        if seeking_venue == 'y':
            seeking_venue = True
        else:
            seeking_venue = False
        seeking_description = request.form.get("seeking_description")
        print(name, city, state, phone, genres,
              seeking_venue, seeking_description)
        venue = Artist(
            name=name,
            city=city,
            state=state,
            phone=phone,
            genres=genres,
            image_link=image_link,
            website_link=website_link,
            facebook_link=facebook_link,
            seeking_venue=seeking_venue,
            seeking_description=seeking_description
        )
        db.session.add(venue)
        db.session.commit()
        flash('Artist ' + name + ' was successfully listed!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Artist '+name+' could not be listed.')
        abort(500)
    finally:
        db.session.close()
    return render_template('pages/home.html')
# delete artist

#  Shows
#  ----------------------------------------------------------------


@ app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    return render_template('pages/shows.html', shows=data)


@ app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
