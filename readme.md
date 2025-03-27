# FastAPI Authentication System

A robust authentication API built with FastAPI, featuring user registration, login, logout, and token refresh functionality.

## Features

### User Management
- Registration with username, email, and password
- Secure login with JWT authentication
- Logout with token blacklisting
- Token refresh for extended sessions

### Security
- Password hashing
- JWT token-based authentication
- Token blacklisting for security
- Rate limiting to prevent abuse

### Database
- Prisma ORM integration
- SQLite database (easily configurable to other databases)
- User and BlacklistedToken models

## Tech Stack
- Backend: FastAPI
- Database: SQLite (via Prisma ORM)
- Authentication: JWT (JSON Web Tokens)
- ORM: Prisma Client Python

## Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/fastapi-auth-system.git
cd fastapi-auth-system
```

2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install fastapi uvicorn prisma pydantic python-jose passlib bcrypt python-multipart
```

4. Configure the database
   - Create a `.env` file with your database URL:
   ```
   DATABASE_URL="file:./BOT.sqlite"
   ```
   - Or update the `schema.prisma` file directly with your database path

5. Generate Prisma client
```bash
prisma generate
```

6. Run database migrations
```bash
prisma migrate dev --name init
```

7. Start the server
```bash
uvicorn main:app --reload
```

## API Endpoints
- `POST /register` - Register a new user
- `POST /login` - Authenticate and receive tokens
- `POST /logout` - Blacklist the current token
- `POST /refresh` - Get a new access token using refresh token
- `GET /me` - Get current user information (protected)

## Database Schema

The application uses two main models:

### User
- id: Unique identifier (auto-incremented)
- username: Unique username
- email: Unique email address
- password: Hashed password

### BlacklistedToken
- id: Unique identifier (auto-incremented)
- token: Blacklisted JWT token
- expiresAt: Token expiration timestamp

## Security Considerations
- Passwords are hashed before storage
- JWT tokens have configurable expiration
- Refresh tokens provide extended sessions
- Token blacklisting prevents token reuse after logout

## License
MIT License will be used

## Author
Pratyanj

---
Feel free to customize this README to better match your specific project implementation and requirements!
