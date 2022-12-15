from src.models import Movie
from flask.testing import FlaskClient

from tests.utils import create_movie, refresh_db

def test_get_all_movies(test_app: FlaskClient):
        # Setup
        refresh_db()
        test_movie = create_movie()

        # Run action
        res = test_app.get('/movies')
        page_data: str = res.data.decode()

        # Asserts
        assert res.status_code == 200
        assert f'<td><a href="/movies/{test_movie.movie_id}">Borat</a></td>' in page_data
        assert '<td>Some guy</td>' in page_data
        assert '<td>5</td>' in page_data

def test_get_all_movies_empty(test_app: FlaskClient):
        #Setup
        refresh_db()
        
        # Run action
        res = test_app.get('/movies')
        page_data: str = res.data.decode()

        # Asserts
        assert res.status_code == 200
        assert '<td>' not in page_data

def test_get_single_movie(test_app: FlaskClient):
    # Setup
    refresh_db()
    test_movie = create_movie()

    # Run action
    res = test_app.get(f'/movies/{test_movie.movie_id}')
    page_data: str = res.data.decode()

    # Asserts
    assert res.status_code == 200
    assert '<h1>Borat - 5</h1>' in page_data
    assert '<h2>Some guy</h2>' in page_data

def test_get_single_movie_404(test_app: FlaskClient):
    # Setup
    refresh_db()

    # Run action
    res = test_app.get('/movies/1')

    # Asserts
    assert res.status_code == 404

def test_create_movie(test_app: FlaskClient):
    # Setup
    refresh_db()

    # Run action
    res = test_app.post('/movies', data = {
            'title': 'Borat',
            'director': 'Some guy',
            'rating': 5
    }, follow_redirects=True)
    page_data = res.data.decode()
    
    # Asserts
    assert res.status_code == 200
    assert '<h1>Borat - 5</h1>' in page_data
    assert '<h2>Some guy</h2>' in page_data

    test_movie = Movie.query.filter_by(title='Borat').first()
    assert test_movie is not None
    assert test_movie.title == 'Borat'
    assert test_movie.director == 'Some guy'
    assert test_movie.rating == 5
    

def test_create_movie_400(test_app: FlaskClient):
    # Setup
    refresh_db()

    # Run action
    res = test_app.post('/movies', data={}, follow_redirects=True)

    # Asserts
    assert res.status_code == 400

def refresh_db():
    Movie.query.delete()
    db.session.commit()