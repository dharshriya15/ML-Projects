from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import requests
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    author = db.Column(db.String(140))
    published_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    reviews = db.relationship('Review', backref='book', lazy='dynamic')

def fetch_books():
    api_url = "https://wolnelektury.pl/api/books/"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        books = response.json()
        for book_data in books:
            published_date = datetime.strptime(book_data['published_date'], '%Y-%m-%d') if 'published_date' in book_data else datetime.utcnow()
            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                published_date=published_date
            )
            db.session.add(book)
        db.session.commit()
    else:
        print(f"Failed to fetch books: {response.status_code}")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)
        
        # Call the function to fetch and store books
        fetch_books()
        
    return app
