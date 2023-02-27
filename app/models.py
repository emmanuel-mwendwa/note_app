from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime, )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(56))
    lastName = db.Column(db.String(56))
    email = db.Column(db.String(56))
    password_hash = db.Column(db.String(128))
    notes = db.relationship('Note', backref='note')

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))