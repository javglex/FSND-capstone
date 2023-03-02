import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Listing, User
import traceback

TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IndWbjI5bzhMUWpYRXFHbjU0emYxcCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zeTIydXZwYXZvd2syZDY3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2ZmZGY5OTc4ZjNkYTBjZTQ4MGRhYTIiLCJhdWQiOiJzaG93bWVzYW5kaWVnby5saXN0aW5ncyIsImlhdCI6MTY3Nzc0MDk1OSwiZXhwIjoxNjc3NzQ4MTU5LCJhenAiOiJJS3p4YlVxZVhZejdXWUtTZnhPUEFib20zc1ozN0xiTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmxpc3RpbmdzIiwicGF0Y2g6bGlzdGluZ3MiLCJwb3N0Omxpc3RpbmdzIiwicmVhZDpsaXN0aW5ncyJdfQ.FiE3_HgLFuGCXp3i-3OK607LSYXGdlrAnR8h2QiCGDIyLTys2z0ynyszceOz-oUHcUvdbq0lRlskJKO9uRmzEn-2DQx20pcjLHNSg4DK0z0zfq7lqQGtNcHRIEd0tffXOjp7NnTrfX3Mf2b3SZEd8J6yyhZxMXRyyRY8hFpIn02aZ9VwEUUfdUQLAYjWv-K1muRYp0QCjglJfOMG5iH3t8r2Dn1Rs0qAak3tIpMvlUZAS5GZBuNjKwju1dWwVcF3BHgCnuNaHHGHEGGNUpdvWkmvG1BWQC91qH0cMcLgIMx1dTO6_-unc885pASGoUuHyx6sn6ETqapcr-OXRuoHgQ'
SECRET = 'TestSecret'
headers={'Content-Type': 'application/json','Authorization':'Bearer ' + TOKEN}


class ApiTestCase(unittest.TestCase):

    """This class represents the api test case"""

    """populates database with test values"""
    def init_db(self):
        try:
            existingUser = User.query.filter(Listing.id == 1).one_or_none()
            if existingUser==None:
                newUser = User(id = 1, username="testuser", email="test@email.com")
                newUser.insert()
        except Exception:
            print("error creating user")

    def setUp(self):
        """Define test variables and initialize app."""
        os.environ['JWT_SECRET'] = SECRET
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "postgres_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_listing = {"title": "Test Car For Sale", "description": "2013 Test Honda Civic", "subtitle": "Color red. Low milage. Test drive today", "user_id": 1}
        self.new_listing_invalid = {"title": None, "description": "??", "subtitle": "", "user_id": None}
        self.init_db()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    
    """Retrieve Listings Tests"""

    def test_retrieve_listings_success(self):

        res = self.client().get("/listings")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["listings"])
        self.assertTrue(len(data["listings"]))

    def test_retrieve_listings_out_of_bounds(self):
        res = self.client().get("/listings?page=2000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    """Create New Listing Tests"""

    def test_create_listing_success(self):
        res = self.client().post("/listings", headers=headers, json=self.new_listing)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["new_posting"])

    def test_create_listing_invalid(self):
        res = self.client().post("/listings", headers=headers, json=self.new_listing_invalid)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    """Delete Listings Tests"""

    def test_delete_listing_success(self):
        res = self.client().post("/listings", headers=headers, json=self.new_listing)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["new_posting"])

        idCreated = data["new_posting"]["id"]
        print("id created: "+ str(idCreated))
        res = self.client().delete("/listings/"+str(idCreated), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["deleted_id"], str(idCreated))

    def test_delete_listing_invalid(self):
        res = self.client().post("/listings", headers=headers, json=self.new_listing)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        res = self.client().delete("/listings/"+str(-1), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    """Patch Listings Tests"""

    def test_update_listing_title(self):
        res = self.client().patch("/listings/1", headers=headers, json={"title": "updated title"})
        data = json.loads(res.data)
        listing = Listing.query.filter(Listing.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(listing.format()["title"], "updated title")

    def test_update_listing_title_invalid(self):
        res = self.client().patch("/listings/1", headers=headers, json={"title": ""})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()