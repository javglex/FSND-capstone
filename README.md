## API Reference

This project is a backend API for viewing and managing listings such as in ecommerce. A listing represents an item that will be put up for sale. The reason why I wanted to create this API is because I want to expand it and use it for a real world project.

### Getting Started
- Base URL: This app can run either locally or from Heroku. Backend app is set to be hosted locally in `http://127.0.0.1:5000/`, and on Heroku in `https://fsnd-capstone-javi.herokuapp.com/`
- Authentication: Auth0.
- NOTE: we only have one existing user in DB (user_id = 1). Use this ID when creating new listings. In future projects, we will automatically create user IDs with Auth0 hooks.


## To run application:

### You should have setup.sh and requirements.txt available
chmod +x setup.sh
source setup.sh

pip install -r requirements.txt
#### Run the app
python3 app.py

### Run tests
dropdb postgres_test 
createdb postgres_test
python3 test_api.py

### Getting User Token
Login/Signup using`https://dev-3y22uvpavowk2d67.us.auth0.com/authorize?audience=showmesandiego.listings&response_type=token&client_id=IKzxbUqeXYz7WYKSfxOPAbom3sZ37LbN&redirect_uri=http://localhost:5000/login-results`

For account with Venue permissions (update,delete,patch listings) use `merchanttest@yopmail.com` with pass `abc@1234`

Once TOKEN is returned, you can save it to CLI using export=TOKEN command. Thereafter, you can use the curl commands below.

### Error Handling
Errors are JSON responses formatted in the following:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The following are error codes that can potentially be returned by the API:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /listings
- General:
    - Returns a list of available listings (advertisements)
    - No authentication or permissions required
- Sample: `curl --request GET http://127.0.0.1:5000/listings`
- Heroku Sample: `curl --request GET https://fsnd-capstone-javi.herokuapp.com/listings`

``` 
{
    "listings":[
        { 
            "body": "sample body",
            "description": "description sample",
            "id": 3,
            "image": "image.url",
            "publish_dates": [],
            "subtitle": "subtitle sample",
            "title": "title sample"
        }
    ],
    "success": true,
    "total_listings": 1
}
```

#### DELETE /listings/{listing_id}
- General:
    - Deletes a listing with the given ID. Returns the id of the deleted listing, and success value.
    - User token with authentication and venue permissions required
- Sample: `curl -X DELETE http://127.0.0.1:5000/listings/1 -H "Content-Type: application/json" "Authorization: Bearer ${TOKEN}"`
- Heroku Sample: `curl -X DELETE https://fsnd-capstone-javi.herokuapp.com/listings/1 -H "Content-Type: application/json" "Authorization: Bearer ${TOKEN}"`
```
{
  "deleted_id": 16,
  "success": true,
}
```


#### PATCH /listings/{listing_id}
- General:
    - Updates the listing's by the given ID, with a title. Returns the id of the updated listing, and success value.
    - User token with authentication and venue permissions required
- Local Sample: `curl -X PATCH http://127.0.0.1:5000/listings/1 -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"title": "new title"}'`
- Heroku Sample: `curl -X PATCH https://fsnd-capstone-javi.herokuapp.com/listings/1 -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"title": "new title"}'`
```
{
    "listing":
    { 
        "body": "sample body",
        "description": "description sample",
        "id": 3,
        "image": "image.url",
        "publish_dates": [],
        "subtitle": "subtitle sample",
        "title": "new title"
    },
    "success": true
}
```

#### POST /user
- General:
    - Used internally. Will be used for a hook with Auth0 authentication in the future
    - Returns success state, and new user created
    - Can be used for testing purposes
- Local Sample: `curl http://127.0.0.1:5000/listings -X POST -H "Content-Type: application/json" -d '{"username":"testName", "email":"test@email.com", "user_id":1}'`
- Heroku Sample: `curl https://fsnd-capstone-javi.herokuapp.com/user -X POST -H "Content-Type: application/json" -d '{"username":"testName", "email":"test@email.com", "user_id":1}'`
``` {
    "user":
    {
      'id': 1,
      'username': 'test name',
      'email': 'self.email'
      },
    "success": true
  }
```