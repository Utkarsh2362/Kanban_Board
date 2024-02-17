from application.models import *
import pdfkit
from datetime import date as dt
import os


def list_info(user):
	list_dict = {}
	all_list = List.query.filter_by(user_id=user.id).all()
	print(all_list)
	for l in all_list:
		list_dict[l.id] = l.title

	return list_dict
	


def create_pdf(username, templ):
	mon_name = dt.today().strftime("%B")
	file = f"static/export_download/{str(username)}_{mon_name}.pdf"
	pdfkit.from_string(templ, f'{file}')

	return file

