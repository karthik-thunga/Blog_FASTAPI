# FastAPI Blog Application Backend
This is a backend application for a blog that allows users to create, read, update, and delete blog posts, as well as like and comment on posts. The application is built using FastAPI and uses a PostgreSQL database.
## Features
* Create, read, update and delete blog posts
* Add tags to blog posts
* Like and comment on blog posts
* Secure end points with authentication and authorization using JSON Web Tokens (JWT)
* API documentation with Swagger UI
## Technologies
* FastAPI
* SQLAlchemy
* Pydantic
* Alembic
* JWT
* Postgres
* uvicorn
## Configuration
This project uses environment variables for configuration. The following variables are required:

* 'SECRET_KEY' : Secret key for JWT authentication
* 'DATABASE_HOST' : Hostname or IP address of the PostgreSQL database server
* 'DATABASE_URL' : URL of the PostgreSQL database server
* 'DATABASE_PORT' : Port number of the PostgreSQL database server
* 'DATABASE_NAME' : Name of the PostgreSQL database
* 'DATABASE_USERNAME' : Username for the PostgreSQL database
* 'DATABASE_PASSWORD': Password for the PostgreSQL database
* 'ALGORITHM' : Algorithm used for token encode.
* 'ACCESS_TOKEN_EXPIRE_MINUTES' : Authorization token expire time.

To set these variables, create a file named .env in the root directory of the project with the following contents(Below is sample):
```
DATABASE_URL = postgresql
DATABASE_HOST = localhost
DATABASE_USERNAME = username
DATABASE_PASSWORD = password
DATABASE_PORT = 5432
DATABASE_NAME = database name
SECRET_KEY = "secret key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```
## Installation
1. Clone this repository
2. Create a virtual environment and activate it
3. Install dependencies using pip install -r requirements.txt
4. Set up a PostgreSQL database and update the database connection URL in the config.py file
5. Run database migrations using 'alembic upgrade head'
6. Start the API server using 'uvicorn main:app --reload'
