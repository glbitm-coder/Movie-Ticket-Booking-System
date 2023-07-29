from datetime import datetime
import os
from flask import jsonify, make_response, request
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from application import db
from application.Models.show import Show

from application.Models.theatre import Theatre
from application.decorator import admin_required

from ..validation import BadRequest, BusinessValidationError, NotFoundError, UnAuthorizedError
from ..Models.user import User
from ..Models.role import Role
from werkzeug.security import check_password_hash
from flask_restful import Resource, fields, marshal_with
from ..Parser.searchTheatreParser import search_theatre_parser



class SearchTheatreAPI(Resource):

    @jwt_required()
    def get(self, user_id = None):
                
        input_name = request.args.get('input_name')
        input_location = request.args.get('input_location')
        searched_theatres = []

        if input_name and input_location:
            searched_theatres = Theatre.query.filter(
                Theatre.storedName.like(input_name + '%'),
                Theatre.storedPlace.like(input_location + '%')
            ).all()
        elif input_name:
            searched_theatres = Theatre.query.filter(
                Theatre.storedName.like(input_name + '%')).all()
        elif input_location:
            searched_theatres = Theatre.query.filter(
                Theatre.storedPlace.like(input_location + '%')
            ).all()
        else:
            searched_theatres = Theatre.query.all()

        theatre_list = []
        for theatre in searched_theatres:
            theatre_data = {
                "id": theatre.id,
                "name": theatre.storedName,
                "place": theatre.storedPlace,
                "capacity": theatre.storedCapacity,
                "image": theatre.storedImage
            }
            theatre_list.append(theatre_data)

        return make_response(jsonify({"theatres": theatre_list}), 200)
    