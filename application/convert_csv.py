import csv
from datetime import datetime as dt



def user_export(list_arr, user_id):
	file = "user_list_" + str(user_id) + "_" + dt.now().strftime('%Y-%m-%d %H:%M') +".csv"
	with open("static/export_download/"+file, 'w', newline='') as export_file:
		header = ["List_id", "List_name"]
		writer = csv.writer(export_file)
		writer.writerow(header)

		for list_obj in list_arr:
			writer.writerow([str(list_obj.id), list_obj.title])

	return f'static/export_download/{file}'



def list_export(cards_arr, username, listname):
	if len(cards_arr) > 0:
		file = "cards_" + listname + "_" + dt.now().strftime('%Y-%m-%d %H:%M') +".csv"
		with open("static/export_download/"+file, 'w') as export_file:
			header = ["Card_id", "Card_title", "content", "Creation_date", "Completion_date", "Deadline"]
			writer = csv.writer(export_file)
			writer.writerow(header)

			for card_obj in cards_arr:
				writer.writerow([str(card_obj.id), card_obj.card_title, card_obj.content, card_obj.created_at, card_obj.completed_at, card_obj.deadline])

	return f'static/export_download/{file}'        
