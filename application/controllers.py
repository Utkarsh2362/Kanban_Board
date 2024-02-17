from flask import current_app as app
from .tasks import *
from application.models import *
from flask_login import current_user
from flask_security import auth_required
from application.cache_setup import cache_create as cache



#Downloading all list names and ids

@app.route('/list/download/')
@auth_required('token')
@cache.memoize(timeout=20)
def list_task():
    print("task entered successfully")
    username = current_user.username
    user_id = current_user.id
    to_email = current_user.email
    result = list_export_task.delay(user_id, username, to_email)
    return {"message" : "downloaded"}, 200



#Downloading task details

@app.route('/cards/<int:list_id>/download/')
@auth_required('token')
@cache.memoize(timeout=20)
def cards_task(list_id):
	print("task entered successfully")
	username = current_user.username
	listname = List.query.filter_by(id=list_id).first().title
	to_email = current_user.email
	print(username, listname)
	result = cards_export_task.delay(list_id, username, listname, to_email)
	return {"message" : "downloaded"}, 200


    