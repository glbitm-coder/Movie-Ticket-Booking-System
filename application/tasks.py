from datetime import datetime, timedelta
import os
import time

from jinja2 import Template
from application.Models.booking import Booking
from application.Models.show import Show
from application.Models.theatre import Theatre
from application.Models.user import User
from application.email_send import send_email
from application.pdf_generator import generate_pdf_report, get_entertainment_data, get_summary_entertainment_data
from main import celery
from flask_weasyprint import HTML


@celery.task()
def generate_csv(theatre_id, theatre_name, shows):

    import csv 
    time.sleep(5)
    
    fields = ['Theatre ID', 'Theatre Name', 'Show ID', 'Show Name', 'Bookings'] 
        
    current_file_path = os.path.abspath(__file__)
    project_folder_path = os.path.dirname(current_file_path)
    src_folder_path = os.path.join(project_folder_path, 'static')

    filename = os.path.join(src_folder_path, "data.csv")
        
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 
        
        for show in shows:
            show_id = show["id"]
            show_name = show["storedName"]
            
            bookings = Booking.query.filter_by(theatre_id=theatre_id, show_id=show_id).all()
            total_tickets = sum(booking.number_of_tickets for booking in bookings)
            csvwriter.writerow([theatre_id, theatre_name, show_id, show_name, total_tickets])

    return "Job started..."


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(30.0, send_email_reminder.s(), name="daily reminder")
    sender.add_periodic_task(60.0, send_monthly_report.s(), name="monthly report")



@celery.task()
def send_email_reminder():
    # Get the list of users who haven't visited the website in the last 24 hours
    # You can query your database for this information
    users_to_remind = get_users_to_remind()

    # Send email reminders to each user in the list
    for user in users_to_remind:

        with open("mail.html", 'r') as h:
            temp=Template(h.read())
            send_email(user.stored_email, subject="Daily Reminder",message=temp.render(name=user))
    
        

def get_users_to_remind():
    # Calculate the datetime 24 hours ago from the current time
    last_24_hours = datetime.now() - timedelta(minutes=2)
    print(last_24_hours)

    # Query the database for users whose last_login is older than 24 hours
    users_to_remind = User.query.filter(User.last_visited < last_24_hours).all()
    print(users_to_remind)

    return users_to_remind


@celery.task()
def send_monthly_report():
    users_to_send_montly_report = get_users_to_send_montly_report()
    for user in users_to_send_montly_report:
        entertainment_data = {}
        entertainment_data = get_entertainment_data(user.id)
        if user.report_format == "HTML":
            with open("report_html.html", 'r') as h:
                temp=Template(h.read())
                html_content = temp.render(name=user, data = entertainment_data)
                send_email(user.stored_email, subject="Monthly Entertainment Report",message=html_content)
        else:
            with open("report_pdf.html", 'r') as h:
                temp=Template(h.read())
                summary_entertainment_data = get_summary_entertainment_data(user.id)
                html_content = temp.render(name=user, data = summary_entertainment_data)
                pdf_file = generate_pdf_report(user ,entertainment_data)
                send_email(user.stored_email, subject="Monthly Entertainment Report",message=html_content, attachment=pdf_file, attachment_name="report.pdf" )



def get_users_to_send_montly_report():
    users_to_send_montly_report = User.query.filter(User.role_id==1).all()
    return users_to_send_montly_report