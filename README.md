# Students API

A REST API built with Python and FastAPI to manage student
information and courses.

## Features

- Student management
- Course management
- SQLAlchemy database integration
- JWT-based authentication
- Password hashing
- Request validation and error handling
- Automated tests with pytest
- Interactive API documentation with Swagger UI

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- PyJWT
- pytest
- Uvicorn

## Live API

Live API documentation:
https://students-api-fg3j.onrender.com

## Run Locally

1. Clone this repository.
2. Install dependencies:

   pip install -r requirements.txt

3. Configure the SECRET_KEY environment variable.
4. Start the server:

   uvicorn main:app --reload

5. Open http://127.0.0.1:8000/docs

## Testing

Run the tests with:

pytest -v