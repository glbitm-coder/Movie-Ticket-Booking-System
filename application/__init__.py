from flask import Flask, request, redirect
from flask import render_template
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask_jwt_extended import JWTManager

from application.validation import UnAuthorizedError
from application.blocklist import BLOCKLIST

db = SQLAlchemy()
DB_NAME = "ticket_show.db"

def create_app():
    app = Flask(__name__)
    CORS(app, origins=['http://localhost:8080'])
    
            
    app.config['SECRET_KEY'] = "gveghwijlmrkb"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['JWT_SECRET_KEY'] = 'something-is-super-secret'  # Change this!
    app.config['CORS_SUPPORTS_CREDENTIALS'] = True
    db.init_app(app)
    api = Api(app)
    
    jwt = JWTManager(app)
    
    from application.jwt_token import check_if_token_in_blocklist, revoked_token_callback
    jwt.token_in_blocklist_loader(check_if_token_in_blocklist)
    jwt.revoked_token_loader(revoked_token_callback)

    # from .views import view
    # from .auth import auth
    # from .all_api.user_api  import UserAPI

    from application.all_api.Authentication.loginAPI import LoginAPI
    from application.all_api.Authentication.logoutAPI import LogoutAPI
    from application.all_api.Authentication.signupAPI import SignUpAPI
    from application.all_api.role_api import RoleAPI
    from application.all_api.theatre_api import TheatreAPI      
    from application.all_api.shows_api import ShowAPI
    from application.all_api.booking_api import BookingAPI
    from application.all_api.search_theatre_api import SearchTheatreAPI

    api.add_resource(LoginAPI, "/login")
    api.add_resource(SignUpAPI, "/signup")
    api.add_resource(RoleAPI, "/api/roles")
    api.add_resource(TheatreAPI, "/user/<int:user_id>/theatre_api", "/user/<int:user_id>/theatre_api/<int:theatre_id>", "/theatre_api")
    api.add_resource(ShowAPI, "/user/<int:user_id>/theatre/<int:theatre_id>/show_api",
                     "/user/<int:user_id>/theatre/<int:theatre_id>/show_api/<int:show_id>")
    api.add_resource(LogoutAPI, "/logout")
    api.add_resource(BookingAPI, "/user/<int:user_id>/theatre/<int:theatre_id>/show/<int:show_id>/booking_api")
    api.add_resource(SearchTheatreAPI, "/search/user/<int:user_id>/theatres")    

    from .Models.user import User
    from .Models.role import Role
    from .Models.show import Show
    from .Models.theatre import Theatre
    from .Models.show_theatre import ShowTheatreAssociation
    from .Models.booking import Booking
    from .Models.rating import Rating

    with app.app_context():
        create_database()
        add_initial_roles()


    return app


def create_database():
    if not path.exists("websites/" + DB_NAME):
        db.create_all()
        
def add_initial_roles():
    from .Models.role import Role

    # Check if the role table is empty
    if Role.query.count() == 0:
        # Add the initial roles
        user_role = Role(id=1, storedName='User')
        admin_role = Role(id=2, storedName='Admin')

        db.session.add(user_role)
        db.session.add(admin_role)
        db.session.commit()
