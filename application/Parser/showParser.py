from flask_restful import reqparse

show_parser = reqparse.RequestParser()
show_parser.add_argument('input_name')
show_parser.add_argument('input_price')
show_parser.add_argument('input_date')
show_parser.add_argument('input_startTime')
show_parser.add_argument('input_endTime')
show_parser.add_argument('input_tags')