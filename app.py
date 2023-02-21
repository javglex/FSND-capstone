import os
from auth import AuthError
from flask import Flask, jsonify, request, abort
from models import Listing, User, setup_db
from flask_cors import CORS
import json
import traceback

app = Flask(__name__)
setup_db(app)
CORS(app)


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    """
    This endpoint is called after successful auth response from Auth0.
    This endpoint is called within an Auth0 Action. Creates a user in our database
    """
    @app.route('/user', methods=['POST'])
    def user():
        userId = request.get_json()['user_id']
        username = request.get_json()['username']
        email = request.get_json()['email']

        try:
            newUser = User(id = userId, username = str(username), email = str(email))
            newUser.insert()
        except Exception:
            traceback.print_exc()
            abort(500)
        
        return jsonify(
            {
                "success": True,
                "new user": newUser.format()
            }
        ), 200


    @app.route("/listings", methods=['GET'])
    def retrieve_listings():
        selection = Listing.query.all()
        length = len(selection)
        listings = [listing.format() for listing in selection]
        
        return jsonify(
            {
                "success": True,
                "listings": listings,
                "total_listings": length
            }
        )

    @app.route("/listings", methods=['POST'])
    def post_listing():
        userId = request.get_json()['user_id']
        title = request.get_json()['title']
        subtitle = request.get_json()['subtitle']
        description = request.get_json()['description']

        print(str(title)+ " " + str(subtitle)+ " " + str(description))

        try:
            newListing = Listing(userId = int(userId), title = str(title), subtitle = str(subtitle), description = str(description))
            newListing.insert()
        except Exception:
            traceback.print_exc()
            abort(500)
        
        return jsonify(
            {
                "success": True,
                "new posting": newListing.format()
            }
        ), 200

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(AuthError)
    def invalid_credentials(error):
        return (
            jsonify({"success": False, "error": 403, "message": "invalid credentials"}),
            403,
        )
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
