#TODO: DONE! 
#TODO: Find a way to have a user delete a row from the data.csv file
#TODO: Find a way to have a user ADD a row to the data.csv file
#TODO: Implement Kivy GUI
#TODO: Find out how to format email into html code??

from backend_class import Backend

import datetime

today = str(datetime.date.today())

backend = Backend
backend.read_csv(backend)
print(backend.csv_data)
backend.update_data(backend)
backend.write_csv(backend)
backend.send_email(backend)