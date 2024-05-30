from flask import render_template, flash, redirect, url_for
from flask import request, jsonify
from urllib.parse import urlparse
from app import db, Book
from app.models import User, Review
from app.forms import LoginForm, RegistrationForm, ReviewForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import Blueprint
import requests

bp = Blueprint('routes', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    books = Book.query.all()
    return render_template('home.html', title='Home', books=books)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book(book_id):
    book = Book.query.get_or_404(book_id)
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(body=form.review.data, author=current_user, book=book)
        db.session.add(review)
        db.session.commit()
        flash('Your review is now live!')
        return redirect(url_for('book', book_id=book.id))
    reviews = book.reviews.order_by(Review.timestamp.desc()).all()
    return render_template('book.html', title=book.title, book=book, form=form, reviews=reviews)