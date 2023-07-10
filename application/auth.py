# import datetime
# from flask import Blueprint, Flask, jsonify, make_response, request, redirect, url_for, flash
# from flask import render_template
# from flask_jwt_extended import create_access_token, get_jwt, jwt_required

# from application.validation import BadRequest, BusineesValidationError
# from application.blocklist import BLOCKLIST
# from . import db
# from .models import User
# from flask_login import login_user, logout_user, login_required, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# import pytz
# from flask_restful import Resource, fields, marshal_with, reqparse


# auth = Blueprint('auth', __name__)


# login_parser = reqparse.RequestParser()
# login_parser.add_argument('input_email')
# login_parser.add_argument('input_password')


# signup_parser = reqparse.RequestParser()
# signup_parser.add_argument('input_email')
# signup_parser.add_argument('input_username')
# signup_parser.add_argument('input_password')
# signup_parser.add_argument('input_confirm_password')

# # API for user login
# class LoginAPI(Resource):

#     def post(self):
        
#         args = login_parser.parse_args()
#         input_email = args.get("input_email", None)
#         input_password = args.get("input_password", None)
#         if not input_email:
#             raise BusineesValidationError(error_message="Email cannot be empty")
#         elif not input_password:
#             raise BusineesValidationError(error_message="Password cannot be empty")
#         user = User.query.filter(User.stored_email==input_email).first()
#         if user:
#             if check_password_hash(user.stored_password, input_password):
#                 return make_response(jsonify({
#                     "message" : "Logged in successfully!",
#                     "id": str(user.id),
#                     "access_token": create_access_token(identity=user.id,expires_delta=datetime.timedelta(minutes=30))
#                 }), 200)
#             else:
#                 raise BusineesValidationError(error_message="Password is incorrect!")
#         else:
#             raise BusineesValidationError(error_message="Email id does not exist!")

# # API for user logout
# class LogoutAPI(Resource):
#     @jwt_required()
#     def post(self):
#         jti = get_jwt()["jti"]
#         BLOCKLIST.add(jti)
#         return make_response(jsonify({
#             "message": "You are successfully logged out!!"
#         }), 200)


# # API for user sign-up
# class SignUpAPI(Resource):
#     def post(self):

#         args = signup_parser.parse_args()
#         input_email = args.get("input_email", None)
#         input_password = args.get("input_password", None)
#         input_username = args.get("input_username", None)
#         input_confirm_password = args.get("input_confirm_password", None)

#         # Input fields empty validation
#         if not input_email:
#             raise BusineesValidationError(error_message="Email cannot be empty")
#         elif not input_username:
#             raise BusineesValidationError(error_message="Username cannot be empty")
#         elif not input_password:
#             raise BusineesValidationError(error_message="Password cannot be empty")
#         elif not input_confirm_password:
#             raise BusineesValidationError(error_message="Confirm password cannot be empty")    
        
#         # More validations
#         email_exists = User.query.filter(User.stored_email==input_email).first()
#         username_exists = User.query.filter(User.stored_username==input_username).first()
        
#         if email_exists:
#             raise BadRequest(error_message=input_email + " is already registered with us. Try to use different email")
#         elif username_exists:
#             raise BadRequest(error_message=input_username + " is already registered with us. Try to use different username")
#         elif input_password != input_confirm_password:
#             raise BadRequest(error_message='Passwords don\'t match! ')
#         elif len(input_username) < 2:
#             raise BadRequest(error_message='Username length should be atleast 2')
#         elif len(input_password) < 6:
#             raise BadRequest(error_message='Password length should be atleast 6')
#         elif len(input_email) < 4:
#             raise BadRequest(error_message='Email address is invalid')
#         else:
#             new_user = User(stored_name = "", stored_bio = "", stored_email = input_email, stored_username = input_username, 
#                             stored_password = generate_password_hash(input_password), stored_timestamp = datetime.datetime.now())
            
#             db.session.add(new_user)
#             db.session.commit()
#             print("b")
#             return make_response(jsonify({
#                 'message' : 'Account has been successfully created',
                
#             }),201)
