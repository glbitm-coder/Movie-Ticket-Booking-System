from datetime import datetime
import os
from flask import jsonify, make_response, request
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from application import db
from application.Models.booking import Booking
from application.Models.rating import Rating
from application.Models.show import Show

from application.Models.theatre import Theatre

from ..validation import BadRequest, BusinessValidationError, NotFoundError, UnAuthorizedError
from ..Models.user import User
from ..Models.role import Role
from werkzeug.security import check_password_hash
from flask_restful import Resource, fields, marshal_with
from ..Parser.ratingParser import rating_parser



class RatingsAPI(Resource):

    @jwt_required()
    def post(self, user_id = None, theatre_id = None, show_id = None, booking_id = None):
                
        errorMessages = []
        current_user_id = get_jwt_identity()
        if user_id is not None and user_id != current_user_id:
            errorMessages.append("You are not authorized to see the page")
            return UnAuthorizedError(error_messages=errorMessages)
        
        user = User.query.filter_by(id = user_id).first()
        if not user:
            errorMessages.append("User not found")
            return NotFoundError(error_messages=errorMessages)
        
        theatre = Theatre.query.filter_by(id = theatre_id).first()
        if not theatre:
            errorMessages.append("Theatre not found")
            return NotFoundError(error_messages=errorMessages)
        
        show = Show.query.filter_by(id = show_id).first()
        if not show:
            errorMessages.append("Show not found")
            return NotFoundError(error_messages=errorMessages)
             

        args = rating_parser.parse_args()
        input_rating = args.get("rating", None)
        print(input_rating)
        new_rating = Rating(rating = input_rating, show_id=show_id, theatre_id=theatre_id, user_id=user_id, booking_id=booking_id)
        db.session.add(new_rating)
        db.session.commit()

        return make_response(jsonify({
                    "message" : "Booking done successfully"
                }), 201)