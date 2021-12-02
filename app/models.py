from threading import Condition
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime)
    postings = db.relationship('Posting', backref='user',lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.full_name)
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))    


class Posting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer,db.ForeignKey('book.ISBN'))
    condition = db.Column(db.String(120))
    price = db.Column(db.Integer)
    img = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return 'ISBN: {}'.format(self.book_id)


class Book(db.Model):
    ISBN = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    author = db.Column(db.String(60))
    retail = db.Column(db.Integer)
    postings = db.relationship('Posting', backref='book',lazy=True)
    #image = db.Column(db.Text, nullable=False)
    # sa.Column('image', sa.Text(), nullable=False),

    def __repr__(self) -> str:
        return '<Title {}, ISBN {}>'.format(self.title,self.ISBN)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.Text, nullable=False)
    time_sent = db.Column(db.DateTime)
    chat_id = db.Column(db.Integer,db.ForeignKey('chat.id'))


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2 = db.Column(db.Integer, db.ForeignKey('user.id'))
    messages = db.relationship('Message',backref='chat',lazy=True)
    def __repr__(self) -> str:
        return '<Id {}, user1 {}, user2 {}>'.format(self.id,self.user1, self.user2)