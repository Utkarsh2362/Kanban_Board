from celery import current_app as celery
from application.models import *
from application.convert_csv import *
from application.send_email import *
from application.date_convert import *
from application.report_pdf import *
from celery.schedules import crontab
from jinja2 import Template
from datetime import date
import os
import time, random
import pdfkit

#celery.set_current()

@celery.on_after_configure.connect
def reminder_periodic_task(sender, **kwargs):

	sender.add_periodic_task(
		crontab(minute=54, hour=23, day_of_week="*"),
		tasks_reminder.s(),
		name="daily reminder"
	)   

	sender.add_periodic_task(
		crontab(minute=19, hour=22),
		report_pdf.s(),
		name="Monthly Report"
	)


@celery.task()
def list_export_task(user_id, username, to_email):
	if user_id:
		try:


			list_arr = List.query.filter_by(user_id=user_id).all()
			file_loc = user_export(list_arr, user_id)
			with open(r"templates/download_temp.html") as file:
				templ = Template(file.read())
			sub = "List Data Download KANBAN APP"
			message = templ.render(username=username)
			send_email(to_mail=to_email, subject=sub, msg=message, attachment=file_loc)
			return {"message" : "successfull"}, 200
		except:
			return {"message" : "your export failed"}, 400

		
	else:
		return {"message" : "failed"}, 400
			

@celery.task()
def cards_export_task(list_id, username, listname, to_email):
	if username:
		try:
			cards_arr = Card.query.filter_by(list_id=list_id).all()
			file_loc = list_export(cards_arr, username, listname)
			with open(r"templates/download_temp.html") as file:
				templ = Template(file.read())
			sub = "Card Data Download KANBAN APP"
			message = templ.render(username=username)
			send_email(to_mail=to_email, subject=sub, msg=message, attachment=file_loc)         
			return {"message" : "successfull"}, 200
		except:
			return {"message" : "your export failed"}, 400

	else:
		return {"message" : "failed"}, 400


# @celery.task()
# def all_data_task()
			

@celery.task()
def tasks_reminder():
	all_lists = List.query.all()  
	all_cards = Card.query.all()
	list_req = []
	send_to = None
	for cards in all_cards:
		if cards.completed_at == "Not completed" and type_date(cards.deadline) > date.today():
			list_req.append([cards.list_id, cards.id])
	for l in list_req:
		val = List.query.filter_by(id=l[0]).first()
		title = List.query.filter_by(id=l[0]).first().title
		task = Card.query.filter_by(id=l[1]).first().card_title
		send_to = USER.query.filter_by(id=val.user_id).first().email
		username = USER.query.filter_by(id=val.user_id).first().username        
		with open(r"templates/reminder.html") as file:
			templ = Template(file.read())
		sub= "Daily Reminder KANBAN APP"
		message = templ.render(username=username, list=title, task=task)
		send_email(to_mail=send_to, subject=sub, msg=message)
		print("TASKS SENT SUCCESSFULLY")

	
	return {"message" : "tasks sent if there were any"}, 200    

@celery.task()
def report_pdf():
	all_user = USER.query.all()
	today = str(date.today())
	month = date.today().strftime("%B")
	with open(r"templates/report_mail.html") as file:
		rep_mail_tem = Template(file.read())

	with open(r"templates/report_temp.html") as file:
		rep_tem = Template(file.read())

	for users in all_user:
		list_data = list_info(users)
		username = users.username
		to_email = users.email
		mail_msg = rep_mail_tem.render(username=username)
		cards_list = Card.query.all()
		pdf_temp = rep_tem.render(username=username, today=today, month=month, lists=list_data, cards_list=cards_list)
		sub = f"Monthly Report KANBAN APP"
		pdf_loc = create_pdf(username, pdf_temp)
		send_email(to_mail=to_email, subject=sub, msg=mail_msg, attachment=pdf_loc)
	

	return {"message" : "Monthly report sent"}, 200








			






