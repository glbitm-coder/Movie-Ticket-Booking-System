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



class SearchShowAPI(Resource):

    @jwt_required()
    def get(self, user_id = None):
                
        input_name = request.args.get('input_name')
        input_tag = request.args.get('input_tag')
        searched_shows = []

        if input_name and input_tag:
            searched_shows = Show.query.filter(
                Show.storedName.like(input_name + '%'),
                (Show.storedTags == input_tag) | 
                (Show.storedTags.like(input_tag + ',%')) | 
                (Show.storedTags.like('%,' + input_tag + ',%')) | 
                (Show.storedTags.like('%, ' + input_tag)) 
            ).all()
        elif input_name:
            searched_shows = Show.query.filter(
                Show.storedName.like(input_name + '%')
            ).all()
        elif input_tag:
            searched_shows = Show.query.filter(
                (Show.storedTags == input_tag) |  
                (Show.storedTags.like(input_tag + ',%')) |  
                (Show.storedTags.like('%,' + input_tag + ',%')) |  
                (Show.storedTags.like('%, ' + input_tag)) 
            ).all()
        else:
            searched_shows = Show.query.all()

        show_list = []
        for show in searched_shows:
            show_data = {
                "id": show.id,
                "name": show.storedName,
                "tags": show.storedTags,
                "price": show.storedPrice,
                "date": show.date.strftime('%Y-%m-%d'),  
                "startTime": show.startTime.strftime('%H:%M:%S'), 
                "endTime": show.endTime.strftime('%H:%M:%S') 
            }
            show_list.append(show_data)

        return make_response(jsonify({"shows": show_list}), 200)