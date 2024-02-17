from application.models import *
from application.cache_setup import cache_create as cache
from application.date_convert import *
from datetime import date
from time import sleep


@cache.memoize(timeout=300)
def get_list_details(user_id=None):
	if user_id:
		all_ids = []
		list_descr = {}
		lists_ids = List.query.filter_by(user_id=user_id).all()

		for lists in lists_ids:
			list_descr[lists.id] = lists.title	
		return list_descr
	else:
		return {"message" : "login information required"}, 404


@cache.memoize(timeout=300)
def get_card_details(user_id=None, list_id=None):
	if user_id:
		card_descr = {}
		try:
			list_info = List.query.filter_by(id=list_id).first()
			if list_info:

				if user_id == list_info.user_id:
					all_cards = Card.query.filter_by(list_id=list_id).all()
					for cards in all_cards:
						if(date.today() >= convert_date(cards.deadline) and cards.completed == False):
							card_descr[cards.id] = [cards.card_title, cards.content, cards.completed, cards.created_at, cards.completed_at, cards.deadline, cards.list_id, "Deadline passed"]
						elif(date.today() < convert_date(cards.deadline) and cards.completed == False):
							card_descr[cards.id] = [cards.card_title, cards.content, cards.completed, cards.created_at, cards.completed_at, cards.deadline, cards.list_id, "Task is due"]
						elif(cards.completed == True):
							card_descr[cards.id] = [cards.card_title, cards.content, cards.completed, cards.created_at, cards.completed_at, cards.deadline, cards.list_id, "Completed"]

							

						
					return card_descr
				else:
					return {"message": "user doesn't have this list"}, 400
			else:
				return {"message": "couldn't fetch card details"}, 400

					
		except:
			return {"message": "couldn't fetch card details"}, 400
	else:
		return {"message" : "login information required"}, 404

			
				

