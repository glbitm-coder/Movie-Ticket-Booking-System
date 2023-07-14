import datetime
import os
from flask import jsonify, make_response, request
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, jwt_required

from ..validation import BusinessValidationError
from ..Models.user import User
from ..Models.role import Role
from werkzeug.security import check_password_hash
from flask_restful import Resource
from ..Parser.theatreParser import theatre_parser

class TheatreAPI(Resource):
    @cross_origin(origin="localhost:8080")
    @jwt_required()
    def post(self):
        
        input_name = request.form.get("input_name")
        input_place = request.form.get("input_place")
        input_capacity = request.form.get("input_capacity")
        input_image = request.files.get("input_image")

        errorMessages = []
        print(input_name)
        print(input_image.filename)
