#!/bin/bash
export DATABASE_URL="postgresql://postgres@localhost:5432/postgres"
export AUTH_DOMAIN='dev-3y22uvpavowk2d67.us.auth0.com'
export JWT_SECRET=
export AUTH_CLIENT_ID='63d6b34a6dcbc2e1d4876078'
echo "setup.sh script executed successfully!"

https://dev-3y22uvpavowk2d67.us.auth0.com/authorize?audience=showmesandiego.listings&response_type=token&client_id=IKzxbUqeXYz7WYKSfxOPAbom3sZ37LbN&redirect_uri=http://localhost:5000/login-results