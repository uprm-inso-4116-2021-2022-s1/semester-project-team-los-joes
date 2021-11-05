import base64
import os
from flask.wrappers import Request
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.form import LoginForm, SignUpForm, NewPostingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Book, Posting, Message, Chat
from werkzeug.urls import url_parse
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_socketio import SocketIO, send

basedir = os.path.abspath(os.path.dirname(__file__))

images = UploadSet('images',IMAGES)
configure_uploads(app,images)

socketio = SocketIO(app, cors_allowed_origins='*')



@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if (not next_page or url_parse(next_page).netloc) != '':
            return redirect(url_for('home'))
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = SignUpForm()
    if form.validate_on_submit():
        full_name = form.firstname.data +" "+ form.lastname.data
        user = User(full_name=full_name,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register', form=form)


@app.route('/books')
def books():
    b = Book.query.all()
    return render_template('books.html',books=b)


@app.route('/books/<isbn>')
def postings(isbn):
    book = Book.query.filter_by(ISBN = isbn).first_or_404()
    postings = book.postings
    return render_template('postings.html',book=book, postings=postings,basedir=app.config["UPLOAD_FOLDER"])

def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic


@app.route('/books/create', methods=['GET', 'POST'])
@login_required
def createposting():
    form = NewPostingForm()
    if form.validate_on_submit():
        book = Book.query.filter_by(title = form.title.data).first_or_404()
        created_by = current_user
        book_id = book.ISBN
        condition = form.condition.data
        price = form.price.data
        filename = images.save(form.image.data)
        posting = Posting(created_by=created_by.id, book_id=book_id, condition=condition, price = price, img=filename)
        db.session.add(posting)
        db.session.commit()
        return redirect(url_for('books'))
    return render_template('newpost.html', form=form)


@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)


@app.route('/chats/messages')
@login_required
def messages():
    return render_template('messages.html')

@app.route('/chats')
@login_required
def chats():
    user = current_user
    chats = Chat.query.filter_by(user1=user.id).all() + Chat.query.filter_by(user2=user.id).all()
    return render_template('chats.html',user=user, chats=chats)
