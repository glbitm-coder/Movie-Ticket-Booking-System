import datetime
import os
from flask import jsonify, make_response, request
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from application import db

from application.Models.theatre import Theatre

from ..validation import BadRequest, BusinessValidationError, NotFoundError, UnAuthorizedError
from ..Models.user import User
from ..Models.role import Role
from werkzeug.security import check_password_hash
from flask_restful import Resource, fields, marshal_with
from ..Parser.theatreParser import theatre_parser



class TheatreAPI(Resource):

    @jwt_required()
    def post(self, user_id = None):

        errorMessages = []

        current_user_id = get_jwt_identity()
        if user_id is not None and user_id != current_user_id:
            errorMessages.append("Unautorized")
            return UnAuthorizedError(error_messages=errorMessages)
        
        user = User.query.filter_by(id = user_id).first()
        if not user:
            errorMessages.append("User not found")
            return NotFoundError(error_messages=errorMessages)


        input_name = request.form.get("input_name", None)
        input_place = request.form.get("input_place", None)
        input_capacity = request.form.get("input_capacity", None)
        input_image = request.files.get("input_image", None)

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

        theatre = Theatre(storedName=input_name, storedPlace=input_place, storedCapacity=input_capacity, creator=user)
        db.session.add(theatre)
        db.session.commit()
        # Get the path to the 'src' folder using the current file's path
        current_file_path = os.path.abspath(__file__)
        project_folder_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
        src_folder_path = os.path.join(project_folder_path, 'src/assets/images')

        # Get the filename from the uploaded image
        image_filename = input_image.filename

        # Construct the new image filename with the prefix and serial number
        new_filename = f"theatre_{theatre.id}_{image_filename}"

        # Construct the full path to save the image
        image_save_path = os.path.join(src_folder_path, new_filename)
        # Save the image to the full path
        input_image.save(image_save_path)
        theatre.storedImage= '' + new_filename
        db.session.commit()

        return make_response(jsonify({
                    "message" : "Theatre created successfully"
                }), 201)
    
    @jwt_required()
    def get(self, user_id = None, theatre_id = None):
        

        errorMessages = []
        theatre_list = []

        current_user_id = get_jwt_identity()
        if user_id is not None and user_id != current_user_id:
            errorMessages.append("Unautorized")
            return UnAuthorizedError(error_messages=errorMessages)
        
        user = User.query.filter_by(id = user_id).first()
        if not user:
            errorMessages.append("User not found")
            return NotFoundError(error_messages=errorMessages)
        
        if theatre_id is None:
            theatres = user.theatres_created.all()
            for theatre in theatres:
                theatre_data = {
                "id": theatre.id,
                "name": theatre.storedName,
                "place": theatre.storedPlace,
                "capacity": theatre.storedCapacity,
                "image": theatre.storedImage
                # Add more fields as needed
                }
                theatre_list.append(theatre_data)

            if theatres is None:
                errorMessages.append("There is no theatre")
                raise BusinessValidationError(error_messages=errorMessages)
            else:
                return make_response(jsonify({"theatres": theatre_list}), 200)
        else:
            theatre = Theatre.query.filter_by(id = theatre_id).first()
            if not theatre:
                errorMessages.append("There is no theatre")
                raise BadRequest(error_messages=errorMessages)
            else:
                theatre_data = {
                "id": theatre.id,
                "name": theatre.storedName,
                "place": theatre.storedPlace,
                "capacity": theatre.storedCapacity,
                "image": theatre.storedImage
                # Add more fields as needed
                }
                return make_response(jsonify(theatre_data), 200)
        

    @jwt_required()
    def put(self, user_id = None, theatre_id = None):
        
        errorMessages = []

        current_user_id = get_jwt_identity()
        if user_id is not None and user_id != current_user_id:
            errorMessages.append("Unautorized")
            return UnAuthorizedError(error_messages=errorMessages)
        
        user = User.query.filter_by(id = user_id).first()
        if not user:
            errorMessages.append("User not found")
            return NotFoundError(error_messages=errorMessages)

        theatre = Theatre.query.filter_by(id = theatre_id).first()
        if not theatre:
            errorMessages.append("There is no theatre")
            raise BadRequest(error_messages=errorMessages)

        input_name = request.form.get("input_name", None)
        input_place = request.form.get("input_place", None)
        input_capacity = request.form.get("input_capacity", None)
        input_image = request.files.get("input_image", None)

        if input_name is not None:
            theatre.storedName = input_name
        if input_place is not None:
            theatre.storedPlace = input_place
        if input_capacity is not None:
            theatre.storedCapacity = input_capacity

        db.session.commit()
        theatre_data = {
            "id": theatre.id,
            "name": theatre.storedName,
            "place": theatre.storedPlace,
            "capacity": theatre.storedCapacity,
            "image": theatre.storedImage,
            "message": "Successfully updated the theatre"
        }
        return make_response(jsonify(theatre_data), 200)
    

    @jwt_required()
    def delete(self, user_id = None, theatre_id = None):

        errorMessages = []

        current_user_id = get_jwt_identity()
        if user_id is not None and user_id != current_user_id:
            errorMessages.append("Unautorized")
            return UnAuthorizedError(error_messages=errorMessages)
        
        user = User.query.filter_by(id = user_id).first()
        if not user:
            errorMessages.append("User not found")
            return NotFoundError(error_messages=errorMessages)
        
        theatre = Theatre.query.filter_by(id = theatre_id).first()
        if not theatre:
            errorMessages.append("There is no theatre")
            raise BadRequest(error_messages=errorMessages)
        else:
            current_file_path = os.path.abspath(__file__)
            project_folder_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
            src_folder_path = os.path.join(project_folder_path, 'src/assets/images')
            image_save_path = os.path.join(src_folder_path, theatre.storedImage)
            replaced_string = image_save_path.replace("\\", "/")
            
            os.remove(replaced_string)
            db.session.delete(theatre)
            db.session.commit()
            return make_response(jsonify({"message" : "Theatre successfully deleted"}), 200)
        
        


