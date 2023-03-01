from . import db, login_manager
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
import datetime
import jwt


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(56))
    lastName = db.Column(db.String(56))
    email = db.Column(db.String(56))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    notes = db.relationship('Note', backref='note')

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_confirmation_token(self, expiration=3600):
        confirmation_token = jwt.encode({
            'confirm': self.id,
            'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=expiration)
        },
        current_app.config['SECRET_KEY'],
        algorithm = 'HS256'
        )
        return confirmation_token

    def confirm(self, token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway = datetime.timedelta(seconds=10),
                algorithms=['HS256']
            )
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))