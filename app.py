from flask import Flask, jsonify
app = Flask(__name__)

from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

from flask_sqlalchemy import SQLAlchemy

## DB CONNECTION AREA

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://tomato:123456@127.0.0.1:5432/ripe_tomatoes_db'

db = SQLAlchemy(app)

# CLI COMMANDS AREA
@app.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@app.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables Dropped")

@app.cli.command('seed')
def seed_db():
    movie = Movie(
        title = 'Spider-man: No way home',
        genre = 'Action',
        length = 148,
        release_year = 2021
    )

    movie1 = Movie(
        title = 'Lord of The rings',
        genre = 'Fantasy',
        length = 250,
        release_year = 2001
    )

    actor = Actor(
        first_name = 'Tom',
        last_name = 'Holland',
        gender = 'male',
        country = 'UK',
        dob = '01/06/1996'
    )

    actor1 = Actor(
        first_name = 'Tom',
        last_name = 'Hardy',
        gender = 'male',
        country = 'UK',
        dob = '01/06/1976'
    )

    db.session.add(movie)
    db.session.add(movie1)
    db.session.add(actor)
    db.session.add(actor1)
    db.session.commit()
    print('Tables seeded')

# MODELS AREA
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    genre = db.Column(db.Text)
    length = db.Column(db.Integer)
    release_year = db.Column(db.Integer)

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    gender = db.Column(db.Text)
    country = db.Column(db.String(100))
    dob = db.Column(db.String)

# SCHEMAS AREA
class MovieSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "genre", "length", "release_year")
movies_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

class ActorSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "gender", "country", "dob")
actors_schema = ActorSchema()
actors_schema = ActorSchema(many=True)



# ROUTING AREA

@app.route("/")
def hello():
  return "Welcome to Ripe Tomatoes API"

@app.route("/movies", methods=["GET"])
def get_movies():
    movies_list = Movie.query.all()
    result = movies_schema.dump(movies_list)
    return jsonify(result)

@app.route("/actors", methods=["GET"])
def get_actors():
    actors_list = Actor.query.all()
    result = actors_schema.dump(actors_list)
    return jsonify(result)