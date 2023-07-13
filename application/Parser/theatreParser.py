from flask_restful import reqparse


theatre_parser = reqparse.RequestParser()
theatre_parser.add_argument('input_name')
theatre_parser.add_argument('input_place')
theatre_parser.add_argument('input_capacity')
theatre_parser.add_argument('input_image')