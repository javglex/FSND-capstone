

## API Reference

### Getting Started
- Base URL: Currently this app is only configured to run locally. Backend app is hosted in `http://127.0.0.1:5000/`
- Authentication: Auth0.

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

#### POST /listings
- General:
    - If authenticated, creates a new listing under User.
    - Returns success state, and new listing created
    - User token with authentication and venue permissions required
- Sample: `curl http://127.0.0.1:5000/listings -X POST -H "Content-Type: application/json" -d "Authorization: Bearer ${TOKEN}" '{"title": "Sample title", "subtitle": "Sample subtitle", "description":"Sample description", "user_id": 1}'`

``` {
    "listing":
    { 
        "body": "sample body",
        "description": "description sample",
        "id": 3,
        "image": "image.url",
        "publish_dates": [],
        "subtitle": "subtitle sample",
        "title": "title sample"
    },
    "success": true
  }
```


#### DELETE /listings/{listing_id}
- General:
    - Deletes a listing with the given ID. Returns the id of the deleted listing, and success value.
    - User token with authentication and venue permissions required
- Sample: `curl -X DELETE http://127.0.0.1:5000/listings/16 -H "Content-Type: application/json" -d "Authorization: Bearer ${TOKEN}"`
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
- Sample: `curl -X PATCH http://127.0.0.1:5000/listings/16 -H "Content-Type: application/json" -d "Authorization: Bearer ${TOKEN}" '{"title": "new title"}'`
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
        "title": "title sample"
    },
    "success": true
}
```
