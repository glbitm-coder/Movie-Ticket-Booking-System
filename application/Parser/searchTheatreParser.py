from flask_restful import reqparse

search_theatre_parser = reqparse.RequestParser()
search_theatre_parser.add_argument('input_name')
search_theatre_parser.add_argument('input_location')