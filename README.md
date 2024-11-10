# README for Email Automation Flask API with Login and Sign-In Using OpenAI
## Overview
This project is a Flask-based API designed for email automation, featuring user authentication (login and sign-in) and integration with OpenAI's API. The API allows users to manage email subscriptions, send newsletters, and utilize AI capabilities for content generation.

## Features
User Authentication: Secure login and sign-in functionality for users.
Email Automation: Manage email subscriptions and send newsletters.
OpenAI Integration: Leverage OpenAI's API for generating content and enhancing user interactions.
Database Models: Structured models for URLs, articles, newsletters, email subscribers, and members.
## Requirements
Python 3.7 or higher
Flask
SQLAlchemy
Flask-SQLAlchemy
Flask-Login
OpenAI Python client
PostgreSQL or any other relational database
Installation
Clone the repository:


git clone https://github.com/RubyClous225/email-automation-flask-api.git
cd email-automation-flask-api
## Create a virtual environment:

bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
## Install dependencies:

bash

pip install -r requirements.txt
Set up environment variables:

Create a .env file in the root directory and add the following:

OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=your_database_url_here
SECRET_KEY=your_secret_key_here
Database Setup
Create the database:

Ensure you have PostgreSQL installed and create a database for the application.

Run migrations:

Use Flask-Migrate to handle database migrations:

bash

flask db init
flask db migrate -m "Initial migration."
flask db upgrade
## Usage
Run the application:

bash

flask run
## API Endpoints:

- User Registration: POST /register
- User Login: POST /login
- Send Newsletter: POST /send-newsletter
- Generate Content: POST /generate-content

## Example API Calls
User Registration
bash
curl -X POST http://localhost:5000/register \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "password": "yourpassword"}'
User Login
bash
curl -X POST http://localhost:5000/login \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "password": "yourpassword"}'
Send Newsletter
bash
curl -X POST http://localhost:5000/send-newsletter \
-H "Authorization: Bearer your_jwt_token" \
-H "Content-Type: application/json" \
-d '{"content": "Your newsletter content here."}'
Generate Content with OpenAI
bash
curl -X POST http://localhost:5000/generate-content \
-H "Authorization: Bearer your_jwt_token" \
-H "Content-Type: application/json" \
-d '{"prompt": "Write a newsletter about the latest tech trends."}'
## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## Support
If you have any questions or encounter any issues, please open an issue on the project's GitHub page.