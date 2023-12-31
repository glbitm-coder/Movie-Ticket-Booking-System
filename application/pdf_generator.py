from datetime import datetime, timedelta
from jinja2 import Template
from application.Models.booking import Booking
from application.Models.rating import Rating
from application.Models.show import Show
from application.Models.theatre import Theatre
from weasyprint import HTML
from application.Models.user import User
from sqlalchemy import extract

def generate_pdf_report(user, entertainment_data):
    with open("report_template_pdf.html", 'r') as h:
        temp = Template(h.read())
        html_content = temp.render(name = user, data = entertainment_data)
    pdf_file = HTML(string=html_content, base_url="http://localhost:5000").write_pdf()
    return pdf_file


def get_summary_entertainment_data(user_id):
    from application import db
    summary_entertainment_data =  {
        'total_bookings': 0,
        'total_tickets': 0,
        'total_shows_seen': 0,
        'total_theatres_visited': 0,
        'nummber_of_ratings_given' : 0,
    }
    entertainment_data =  get_entertainment_data(user_id)
    summary_entertainment_data["total_bookings"] = len(entertainment_data["bookings"]) or 0
    summary_entertainment_data["total_tickets"] = sum(booking["number_of_tickets"] for booking in entertainment_data["bookings"]) or 0
    summary_entertainment_data["total_shows_seen"] = len(entertainment_data["shows"]) or 0
    summary_entertainment_data["total_theaters_visited"] = len(entertainment_data["theatres"]) or 0
    summary_entertainment_data["nummber_of_ratings_given"] = len(entertainment_data["ratings"]) or 0

    return summary_entertainment_data



def get_entertainment_data(user_id):
    entertainment_data = {
        "bookings": [],
        "shows": [],
        "theatres": [],
        "ratings": []
    }
    
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

    # Get bookings done by the user in the previous month
    bookings_done_by_user = Booking.query.filter(
        Booking.user_id == user_id,
        extract('year', Booking.created_date_time) == first_day_of_previous_month.year,
        extract('month', Booking.created_date_time) == first_day_of_previous_month.month
    ).all()

    # Get shows seen by the user in the previous month
    shows_seen_in_previous_month = Show.query.filter(
        extract('year', Show.date) == first_day_of_previous_month.year,
        extract('month', Show.date) == first_day_of_previous_month.month
    ).all()

    # Check each show to see if it was booked by the user previously
    for show in shows_seen_in_previous_month:
        # Check if the show was booked by the user earlier
        if Booking.query.filter_by(user_id=user_id, show_id=show.id).first():
            # Add show to the report if it was booked by the user earlier
            entertainment_data["shows"].append(show)

    # Get theaters to consider
    theatres_to_consider = set()
    for show in entertainment_data["shows"]:
        for theatre in show.theatres:
            # Check if there is any booking for this theatre made by the user in the previous month
            if Booking.query.filter(Booking.theatre_id == theatre.id, Booking.user_id == user_id).first():
                theatres_to_consider.add(theatre)

    # Fetch distinct shows based on show_ids
    shows = entertainment_data["shows"]
    for index, show in enumerate(shows, start=1):
        show.serial_no = index

    # Fetch distinct theatres to consider
    for index, theatre in enumerate(theatres_to_consider, start=1):
        theatre.serial_no = index
        entertainment_data["theatres"].append(theatre)

    # Fill bookings data in the entertainment_data
    
    for index, booking in enumerate(bookings_done_by_user, start=1):
        show = Show.query.get(booking.show_id)
        theatre = Theatre.query.get(booking.theatre_id)

        if show and theatre:
            entertainment_data["bookings"].append({
                "serial_no": index,
                "number_of_tickets": booking.number_of_tickets,
                "total_price": booking.total_price,
                "show_name": show.storedName,
                "theatre_name": theatre.storedName,
                "date_time": booking.created_date_time
            })

    ratings_given_by_user = Rating.query.filter(
        Rating.user_id == user_id,
        extract('year', Rating.created_date_time) == first_day_of_previous_month.year,
        extract('month', Rating.created_date_time) == first_day_of_previous_month.month
    ).all()

    for index, rating in enumerate(ratings_given_by_user, start=1):
        show = Show.query.get(rating.show_id)
        theatre = Theatre.query.get(rating.theatre_id)

        if show and theatre:
            entertainment_data["ratings"].append({
                "serial_no": index,
                "rating": rating.rating,
                "show_name": show.storedName,
                "theatre_name": theatre.storedName
            })

    return entertainment_data