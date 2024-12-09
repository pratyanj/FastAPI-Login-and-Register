# FastAPI Authentication System

A secure authentication system built with FastAPI and modern Python.

## Features

- User registration and authentication
- Login/Logout functionality 
- Password hashing with bcrypt
- JWT token based authentication
- Password reset capabilities
- Role-based access control (RBAC)
- Session management
- API documentation with Swagger/OpenAPI

## Tech Stack

- Backend: FastAPI
- Database: PostgreSQL
- Authentication: JWT tokens
- Password Hashing: Passlib with bcrypt
- API Documentation: Swagger/OpenAPI
- Python 3.8+

## Installation

1. Clone the repository:

git clone https://github.com/yourusername/fastapi-auth.git


2. Create virtual environment:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


3. Install dependencies:

pip install -r requirements.txt


4. Set up environment variables:

cp .env.example .env
# Edit .env with your configuration


5.Start the server:

uvicorn app.main:app --reload


## API Documentation

Once the server is running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details


