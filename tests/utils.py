from src.models import Movie, db

def refresh_db():
    Movie.query.delete()
    db.session.commit()

def create_movie(title='Borat', director='Some guy', rating = 5) -> Movie:
    test_movie = Movie(title=title, director=director, rating=rating)
    db.session.add(test_movie)
    db.session.commit()
    return test_movie