from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from application.Models.booking import Booking
from application.Models.rating import Rating
from application.Models.theatre import Theatre
from application.decorator import admin_required

from ..validation import BadRequest, BusinessValidationError, NotFoundError, UnAuthorizedError
from ..Models.user import User
from ..Models.role import Role
from werkzeug.security import check_password_hash
from flask_restful import Resource, fields, marshal_with
from ..Parser.theatreParser import theatre_parser
import matplotlib.pyplot as plt
import time


def popularity_of_shows(theatre_id):
    # Retrieve the theater
    theatre = Theatre.query.get(theatre_id)

    # Access all shows for the theater
    shows = theatre.shows

    # Calculate total number of tickets sold for each show
    for show in shows:
        bookings = Booking.query.filter(Booking.show_id == show.id, Booking.theatre_id == theatre.id).all()
        total_tickets_sold = sum(booking.number_of_tickets for booking in bookings)
        show.total_tickets_sold = total_tickets_sold

    # Sort shows based on total tickets sold in descending order
    sorted_shows = sorted(shows, key=lambda x: x.total_tickets_sold, reverse=True)

    # Consider only the top 5 shows
    top_5_shows_by_tickets_sold = sorted_shows[:5]
    return top_5_shows_by_tickets_sold

def calculate_average_rating(ratings):
    total_rating = sum(rating.rating for rating in ratings)
    total_users = len(ratings)
    
    if total_users == 0:
        return 0
    
    return total_rating / total_users


def ratings_of_shows(theatre_id):
    # Retrieve the theater
    theatre = Theatre.query.get(theatre_id)

    # Access all shows for the theater
    shows = theatre.shows

    # Calculate average ratings for each show
    for show in shows:
        ratings = Rating.query.filter(Rating.show_id == show.id, Rating.theatre_id == theatre.id).all()
        average_rating = calculate_average_rating(ratings)
        show.average_rating = average_rating

    # Sort shows based on average ratings in descending order
    sorted_shows = sorted(shows, key=lambda x: x.average_rating, reverse=True)

    # Consider only the top 5 shows
    top_5_shows = sorted_shows[:5]
    return top_5_shows

def price_for_shows(theatre_id):
    # Retrieve the theater
    theatre = Theatre.query.get(theatre_id)

    # Access all shows for the theater
    shows = theatre.shows

    # Calculate total price for each show
    for show in shows:
        bookings = Booking.query.filter(Booking.show_id == show.id, Booking.theatre_id == theatre.id).all()
        total_price = sum(booking.total_price for booking in bookings)
        show.total_price = total_price

    # Sort shows based on total price in descending order
    sorted_shows = sorted(shows, key=lambda x: x.total_price, reverse=True)

    # Consider only the top 5 shows
    top_5_shows_by_total_price = sorted_shows[:5]
    return top_5_shows_by_total_price


def create_bar_chart(data, x_labels, parameter_name, file_name):
    plt.bar(x_labels, data)
    plt.xlabel('Shows')
    plt.ylabel(parameter_name)
    plt.title(f'Top 5 Shows by {parameter_name}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(file_name)  # Save the figure to a file
    plt.close()

def summary_chart(theatre_id):
    top_shows_by_tickets_sold = popularity_of_shows(theatre_id)
    top_shows_by_average_rating = ratings_of_shows(theatre_id)
    top_shows_by_total_price = price_for_shows(theatre_id)
    
    # Extract show names and parameter values for plotting
    show_names = [show.storedName for show in top_shows_by_tickets_sold]
    tickets_sold = [show.total_tickets_sold for show in top_shows_by_tickets_sold]
    average_ratings = [show.average_rating for show in top_shows_by_average_rating]
    total_prices = [show.total_price for show in top_shows_by_total_price]
    
    # Create bar charts for each comparison
    create_bar_chart(tickets_sold, show_names, 'Number of Tickets Sold', f'src/assets/summary/theatre_{theatre_id}_tickets_sold.png')
    create_bar_chart(average_ratings, show_names, 'Average Rating', f'src/assets/summary/theatre_{theatre_id}_average_ratings.png')
    create_bar_chart(total_prices, show_names, 'Total Price', f'src/assets/summary/theatre_total_prices.png')


class SummaryAPI(Resource):

    @jwt_required()
    @admin_required
    def get(self, user_id = None, theatre_id = None):
        summary_chart(theatre_id)
        time.sleep(5)
        return make_response(jsonify({"message":"Successfully retrieved"}), 200)