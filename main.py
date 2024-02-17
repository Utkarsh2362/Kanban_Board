from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from flask_login import LoginManager
from flask_security import utils
from application.database import db
from flask import current_app
from flask_restful import Resource, marshal_with, fields, reqparse
from werkzeug.exceptions import Conflict
from sqlalchemy.exc import IntegrityError
from application.models import * 
from application.celery_setup import *
from flask_security import auth_required, hash_password, current_user
from flask_caching import Cache
import celery



app = Flask(__name__)
api = Api(app)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///final_project_copy.sqlite3'
app.config['SECRET_KEY'] = 'Thisisasecretkey'
app.config['SECURITY_PASSWORD_SALT'] = 'Thisissalt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
app.config.update(CELERY_CONFIG={
    'broker_url': 'redis://localhost:6379/2',
    'result_backend': 'redis://localhost:6379/2',
    'enable_utc': False
})

celery = make_celery(app)


db.init_app(app)
app.app_context().push()
# db.create_all()
# db.session.commit()


from application.tasks import *
from application.controllers import *
from application.api import *


api.add_resource(User, '/user')	
api.add_resource(lists, '/add_list', '/api/get_lists/', '/api/<int:lists_id>/update/', '/api/<int:lists_id>/delete/')	
api.add_resource(Cards, '/add_card/<int:lists_id>/', '/api/get_cards/<int:lists_id>/', '/update_card/<int:lists_id>/<int:cards_id>/', '/delete_card/<int:lists_id>/<int:cards_id>/')



if __name__ == '__main__':
	app.run(debug=True)