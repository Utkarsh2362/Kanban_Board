from flask import current_app as app
from flask import jsonify
import json
from flask_login import current_user
from flask_restful import Resource, marshal_with, fields, reqparse
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from werkzeug.exceptions import Conflict
from sqlalchemy.exc import IntegrityError
from application.models import db
from application.models import *
from flask_security import auth_required, hash_password
from datetime import datetime as dt
from application.get_api import *
from application.cache_setup import cache_create as cache




user_datastore = SQLAlchemyUserDatastore(db, USER, Role)
security = Security(app, user_datastore)





class User(Resource):
    def post(self):
        user_req = reqparse.RequestParser()
        user_req.add_argument('email', required=True, help="email required")
        user_req.add_argument('username', required=True, help="username required")
        user_req.add_argument('password', required=True, help="password required")
        data = user_req.parse_args()
        if user_datastore.find_user(email=data.get('email')) or user_datastore.find_user(username=data.get('username')):
            raise Conflict
        try:
            user = user_datastore.create_user(
                username=data.get('username'), email=data.get('email'),
                password=hash_password(data.get('password')))
            db.session.commit()
            return {"email": user.email}
            #return {"signup" : "user successfully created"}, 201
        except IntegrityError:
            return {"signup" : "failed"}, 406
            raise Conflict  
        return {"signup" : "user successfully created"}, 201
    @auth_required('token')  
    def get(self):
        return {"email": current_user.email, "username": current_user.username}, 200
class lists(Resource):
    @auth_required('token')
    def get(self):
        user = current_user
        print(user.id)
        list_detail = get_list_details(user_id=user.id)      #getting cached result
        return list_detail


    @auth_required('token')
    def post(self):
        user = current_user
        cache.delete_memoized(get_list_details, user.id)
        cache.delete_memoized(get_card_details, user.id)        
        list_req = reqparse.RequestParser()
        list_req.add_argument('title', required=True, help="title required")
        info = list_req.parse_args()
        if user:

            try:
                list_title = info.get('title')
                list_data = List(title=list_title, user_id=user.id)
                db.session.add(list_data)
                db.session.commit()
                return {"list_creation" : "successfull"}, 201
            except:
                return {"list_creation" : "failed"}, 404
                
        else:
            return {"info" : "there is some error"}, 400

    @auth_required('token')  
    def patch(self, lists_id):
        user = current_user
        cache.delete_memoized(get_list_details, user.id)
        cache.delete_memoized(get_card_details, user.id, lists_id)        
        list_update = reqparse.RequestParser()
        list_update.add_argument('title', required=True, help="title required")
        data = list_update.parse_args()
        new_title = data.get('title', None)
        if user:
            try:

                list_data = List.query.filter_by(id=lists_id).first()
                if list_data.user_id == current_user.id:
                    old_data = List.query.filter_by(id=lists_id).first()
                    old_data.title = new_title
                    db.session.commit() 
                    return {"message": "list updated successfully"}, 200  
                else:
                    return {"message": "User doesn't have this list"}, 400
            except:
                return {"message": "list update failed"}, 400             
                
        else:
            return {"message": "login credentials required"}, 400
                
    @auth_required('token')
    def delete(self, lists_id):
        user = current_user
        cache.delete_memoized(get_list_details, user.id)
        cache.delete_memoized(get_card_details, user.id, lists_id)
        if user:
            try:
                list_info = List.query.filter_by(id=lists_id).first()
                if list_info.user_id == user.id:
                    List.query.filter_by(id=lists_id).delete()
                    Card.query.filter_by(list_id=lists_id).delete() #some changes in this line
                    db.session.commit()
                    return {"message": "list deletion successfull"}, 200
                else:
                    return {"message": "User doesn't have this list"}, 400
                    
            except:
                return {"message": "list deletion failed"}, 400
        else:
            return {"message": "login credentials required"}, 400
                

class Cards(Resource):
    @auth_required('token')
    def get(self, lists_id):
        user = current_user
        card_detail = get_card_details(user_id=user.id, list_id=lists_id)
        return card_detail

    @auth_required('token')
    def post(self, lists_id):
        user = current_user
        cache.delete_memoized(get_list_details, user.id)
        cache.delete_memoized(get_card_details, user.id, lists_id)
        the_list = List.query.filter_by(id=lists_id).first()
        card_req = reqparse.RequestParser()
        card_req.add_argument('card_title', required=True, help="title required")
        card_req.add_argument('content', required=True, help="some content required")
        card_req.add_argument('deadline', required=True, help="provide deadline for you task")
        data = card_req.parse_args()

        if user:

            if user.id == the_list.user_id:

                try:

                    card_det = Card.query.filter_by(list_id=the_list.id).all()
                    if len(card_det)>0:
                        for the_cards in card_det:
                            print("I am here")
                            if the_cards.card_title == data.get('card_title'):
                                return {"message": "card with this title already exists"}, 400
                            else:
                                card_create = Card(card_title=data.get('card_title'), content=data.get('content'), deadline=data.get('deadline'), list_id=the_list.id)
                                db.session.add(card_create)
                                db.session.commit()
                                return {"message": "card has been created"}, 200
                    else:
                        card_create = Card(card_title=data.get('card_title'), content=data.get('content'), deadline=data.get('deadline'), list_id=the_list.id, created_at=dt.now().strftime('%Y-%m-%d %H:%M'))
                        db.session.add(card_create)
                        db.session.commit()
                        return {"message": "card has been created"}, 200
                                
                except:
                    return {"message": "card creation failed"}, 400

            else:
                return {"message": "User doesn't have this list"}, 400
        else:
            return {"message": "login credentials required"}, 400


    @auth_required('token')
    def patch(self, lists_id, cards_id):
        user = current_user
        cache.delete_memoized(get_list_details, user.id)
        cache.delete_memoized(get_card_details, user.id, lists_id)        
        the_list = List.query.filter_by(id=lists_id).first()
        the_card = Card.query.filter_by(id=cards_id).first()
        card_update = reqparse.RequestParser()
        card_update.add_argument('card_title')
        card_update.add_argument('content')
        card_update.add_argument('completed')
        card_update.add_argument('deadline')
        card_update.add_argument('completed_at')
        data = card_update.parse_args()
        if user and the_list is not None and the_card is not None:
            if user.id == the_list.user_id:
                if the_list.id == the_card.list_id:
                    print(type(data.get('completed')))
                    if data.get('card_title'):
                        the_card.card_title = data.get('card_title')
                    if data.get('content'):
                        the_card.content = data.get('content')
                    if data.get('completed'):
                        print(type(data.get('completed')))
                        the_card.completed = eval(data.get('completed'))
                        if data.get('completed') == "True":
                            the_card.completed_at = dt.now().strftime('%Y-%m-%d %H:%M')
                        
                    if data.get('deadline'):
                        the_card.deadline = data.get('deadline')                                                                        
                    db.session.commit()
                    return {"message": "card updated"}, 200
                
                else:
                    return {"message": "error"}, 400
            else:
                return {"message": "user doesn't have this list"}, 400
        else:
            return {"message": "login credentials required or wrong list id or card id given"}, 400
                 
                
    @auth_required('token')
    def delete(self, lists_id, cards_id):
        user = current_user
        cache.delete_memoized(get_list_details, user.id)
        cache.delete_memoized(get_card_details, user.id, lists_id)        
        if user:
            try:
                the_list = List.query.filter_by(id=lists_id).first()
                the_card = Card.query.filter_by(id=cards_id).first()
                if user.id == the_list.user_id:
                    if the_list.id == the_card.list_id:
                        Card.query.filter_by(id=cards_id).delete()
                        db.session.commit()
                        return {"message": "card deleted successfully"}
                    else:
                        return {"message": "list doesn't have this card"}, 400
                else:
                    return {"message": "User doesn't have this list"}, 400
            except:
                return {"message": "card deletion failed"}, 400
        else:
            return {"message": "login credentials required"}, 400
                
                
                    

                        
                        

