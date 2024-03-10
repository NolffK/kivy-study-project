import csv
import datetime
import smtplib

class Backend:

    message = 'time to study'
    todays_study_schedule = []
    future_study_schedule = []
    csv_data = 0
    csv_reader = 0

    def __init__(self, message, intro_message, future_study_schedule_message, todays_study_schedule, future_study_schedule, csv_data, csv_reader):
        self.message = message
        self.intro_message = intro_message
        self.future_study_schedule_message = future_study_schedule_message
        self.todays_study_schedule = todays_study_schedule
        self.future_study_schedule = future_study_schedule
        self.csv_data = csv_data
        self.csv_reader = csv_reader

    def update_next_study_day(next_study_day, days_remaining):
           
        date_object = datetime.datetime.strptime(next_study_day, '%Y-%m-%d')

        if days_remaining == '4':    
            date_object = date_object + datetime.timedelta(days=1)

        elif days_remaining == '3':
            date_object = date_object + datetime.timedelta(days=3)

        elif days_remaining == '2':
            date_object = date_object + datetime.timedelta(days=5)

        elif days_remaining == '1':
            date_object = date_object + datetime.timedelta(days=7)

        else:
            date_object = date_object + datetime.timedelta(days=14)

        date_object = date_object.strftime('%Y-%m-%d')
        return str(date_object)
    
    def update_remaining_study_days(days_remaining):

        days_remaining = int(days_remaining)
        days_remaining -= 1
        return str(days_remaining)
    
    def remove_row(data, remaining_study_days, index_):
        
        data.pop(index_)
        return data

    def read_csv(self):
        with open('data.csv', 'r') as csv_file:
            self.csv_reader = csv.DictReader(csv_file)
            self.csv_data = [row for row in self.csv_reader] # creates list (csv_data) of dicts (row)

    def update_data(self):
        today = str(datetime.date.today())
        index = 0
        for row in self.csv_data:
            if today == row["next_study_day"]:

                row['next_study_day'] = self.update_next_study_day(row['next_study_day'], row['remaining_study_days'])
                row['remaining_study_days'] = self.update_remaining_study_days(row['remaining_study_days'])
                self.todays_study_schedule.append(f"Study {row['topic']} today! {row['remaining_study_days']} day(s) remaining for this topic")

                if row['remaining_study_days'] > '0':
                    self.future_study_schedule.append(f"Study {row['topic']} on {row['next_study_day']}! {row['remaining_study_days']} day(s) remaining for this topic")
                else:
                    self.csv_data = self.remove_row(self.csv_data, row['remaining_study_days'], index)

            else:
                self.future_study_schedule.append(f"Study {row['topic']} on {row['next_study_day']}! {row['remaining_study_days']} day(s) remaining for this topic")

            index += 1
    
    def write_csv(self):

        with open('data.csv', 'w', newline='') as csv_file:
            fieldnames = self.csv_reader.fieldnames
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(self.csv_data)
    
    def send_email(self):

        email_message = f"""
     
        Hello! This is your study schedule for today:

        Today, you are going to study...

        {self.todays_study_schedule}

        That's it for today...upcoming study schedule:

        {self.future_study_schedule}

        """

        #establish connection to GMAIL SMTP server, 'with' keyword ensures that the connection is closed after code is executed
        #Uses SMTP class to creat an SMTP connection specified over smtp.gmail.com
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection: 
            #Starts the Transport Layer Security encryption for the connection.
            #TLS is a protocol that ensures the security of communication over a computer network
            connection.starttls()
            connection.login(user='peytonvecchi@gmail.com', password='maagkymawsgitjmf')
            connection.sendmail(from_addr='peytonvecchi@gmail.com', to_addrs='peytonvecchi@gmail.com',
            msg=email_message)