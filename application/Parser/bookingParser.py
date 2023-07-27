from flask_restful import reqparse

booking_parser = reqparse.RequestParser()
booking_parser.add_argument('number_of_tickets')
booking_parser.add_argument('total_price')