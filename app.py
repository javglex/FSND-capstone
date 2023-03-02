import os
from auth import AuthError, requires_auth
from flask import Flask, jsonify, request, abort
from models import Listing, User, setup_db
from flask_cors import CORS
import json
import traceback

app = Flask(__name__)
setup_db(app)
CORS(app)
LISTINGS_PER_PAGE = 10


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        return "Hello! Read the included README to get started"

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

    @app.route("/login-results", methods=['GET'])
    def login_results():
        return "login success! make sure to copy the access token in the url above."


    @app.route("/listings", methods=['GET'])
    def retrieve_listings():
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * LISTINGS_PER_PAGE
        end = start + LISTINGS_PER_PAGE

        selection = Listing.query.paginate(page=page, error_out=False, max_per_page=LISTINGS_PER_PAGE).items
        length = len(selection)
        listings = [listing.format() for listing in selection]
        
        if length==0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "listings": listings,
                "total_listings": length
            }
        )

    @app.route("/listings", methods=['POST'])
    @requires_auth('post:listings')
    def post_listing(jwt):
        userId = request.get_json()['user_id']
        title = request.get_json()['title']
        subtitle = request.get_json()['subtitle']
        description = request.get_json()['description']

        print(str(title)+ " " + str(subtitle)+ " " + str(description))
        print("account id: "+ str(jwt['sub']))
        if userId == None or userId == "":
            abort(422)

        try:
            newListing = Listing(userId = int(userId), title = str(title), subtitle = str(subtitle), description = str(description))
            newListing.insert()
        except Exception:
            traceback.print_exc()
            abort(500)
        
        return jsonify(
            {
                "success": True,
                "new_posting": newListing.format()
            }
        ), 200

    @app.route("/listings/<listing_id>", methods=['DELETE'])
    @requires_auth('delete:listings')
    def remove_listing(jwt, listing_id):
        listing = Listing.query.filter(Listing.id == listing_id).one_or_none()
        userId = jwt['sub']

        if (listing is None):
            abort(404)
        
        try:
            #if (listing.user_id == userId): # in future ensure we are only deleting our own listing
            listing.delete()
        except Exception:
            traceback.print_exc()
            abort(500)

        return jsonify(
            {
                "success": True,
                "deleted_id": listing_id
            }
        ), 200

    @app.route("/listings/<listing_id>", methods=['PATCH'])
    @requires_auth('patch:listings')
    def update_listing(jwt, listing_id):
        title = request.get_json()['title'] # new title to update with
        userId = jwt['sub']

        listing = Listing.query.filter(Listing.id == listing_id).one_or_none()

        if title == "" or title is None:
            abort(422)

        if (listing is None):
            abort(404)
        
        listing.title = title

        try:
            # if (listing.user_id == userId): # in future ensure we are only updating our own listing
            listing.update()

        except Exception:
            traceback.print_exc()
            abort(500)

        return jsonify(
            {
                "success": True,
                "listing": [listing.format()]
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
            jsonify({"success": False, "error": error.status_code, "message": error.error}),
            error.status_code,
        )
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
