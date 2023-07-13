import datetime
import os
from flask import jsonify, make_response, request
from flask_jwt_extended import create_access_token, jwt_required

from ..validation import BusinessValidationError
from ..Models.user import User
from ..Models.role import Role
from werkzeug.security import check_password_hash
from flask_restful import Resource
from ..Parser.theatreParser import theatre_parser

class TheatreAPI(Resource):
    @jwt_required()
    def post(self):
        
        args = theatre_parser.parse_args()
        input_name = args.get("input_name", None)
        input_place = args.get("input_place", None)
        input_capacity = args.get("input_capacity", None)
        input_image = request.files.get('input_image', None)
        errorMessages = []
        print(input_image.filename)
