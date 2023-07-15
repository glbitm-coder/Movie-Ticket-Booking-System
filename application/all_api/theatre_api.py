import datetime
import os
from flask import jsonify, make_response, request
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, jwt_required
from application import db

from application.Models.theatre import Theatre

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
        
        input_name = request.form.get("input_name", None)
        input_place = request.form.get("input_place", None)
        input_capacity = request.form.get("input_capacity", None)
        input_image = request.files.get("input_image", None)

        errorMessages = []

        if not input_name:
            errorMessages.append("Name cannot be empty")
        elif not input_place:
            errorMessages.append("Place cannot be empty")
        elif not input_capacity:
            errorMessages.append("Capacity cannot be empty")
        elif not input_image:
            errorMessages.append("Image cannot be empty")
        
        if len(errorMessages) != 0:
            raise BusinessValidationError(error_messages=errorMessages)

        theatre = Theatre(storedName=input_name, storedPlace=input_place, storedCapacity=input_capacity)
        db.session.add(theatre)
        db.session.commit()
        # Get the path to the 'src' folder using the current file's path
        current_file_path = os.path.abspath(__file__)
        project_folder_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
        src_folder_path = os.path.join(project_folder_path, 'src')

        # Get the filename from the uploaded image
        image_filename = input_image.filename

        # Construct the new image filename with the prefix and serial number
        new_filename = f"theatre_{theatre.id}_{image_filename}"

        # Construct the full path to save the image
        image_save_path = os.path.join(src_folder_path, 'assets', new_filename)
        # Save the image to the full path
        input_image.save(image_save_path)
        theatre.storedImage="/src/assets/" + new_filename
        db.session.commit()

        return make_response(jsonify({
                    "message" : "Theatre created successfully"
                }), 201)
