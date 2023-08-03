import os
import time
from application.Models.booking import Booking
from main import celery

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
