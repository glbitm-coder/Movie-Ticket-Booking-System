from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from application.Models.theatre import Theatre
from application.decorator import admin_required
from flask_restful import Resource

class GenerateCsvAPI(Resource):

    @jwt_required()
    @admin_required
    def get(self, user_id, theatre_id):

        theatre = Theatre.query.filter_by(id = theatre_id).first()
        all_shows = theatre.shows

        shows_list = []
        for show in all_shows:
            show_data = {
                "id": show.id,
                "storedName": show.storedName,
                
            }
            shows_list.append(show_data)

        from application.tasks import generate_csv
        a = generate_csv.delay(theatre_id=theatre.id, theatre_name=theatre.storedName, shows=shows_list)
        return make_response(jsonify({
            "Task_ID" : a.id
            }), 200)