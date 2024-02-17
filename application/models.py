from application.database import *
from flask_security import UserMixin, RoleMixin
from datetime import datetime as dt


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))  


class USER(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False) 
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))
    lists = db.relationship('List', backref='user', lazy=True)


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))  


class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cards = db.relationship('Card', backref='list', lazy=True)    

class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    card_title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.String(80), default=dt.now().strftime('%Y-%m-%d %H:%M'))
    completed_at = db.Column(db.String(80), default="Not completed")
    deadline  = db.Column(db.String(80))
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))
  