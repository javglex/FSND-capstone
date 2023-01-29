import os
from flask import Flask, jsonify, request, abort
from models import Listing, setup_db
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
        title = request.get_json('title')
        subtitle = request.get_json('subtitle')
        description = request.get_json('description')

        try:
            newListing = Listing(title = str(title), subtitle = subtitle)
            newListing.insert()
        except Exception:
            traceback.print_exc()
            abort(500)
        
        return jsonify(
            {
                "success": True,
                "drinks": newListing.format()
            }
        ), 200

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
