## Social Media API
A Django REST Framework–powered backend that enables users to create, read, update, and delete posts and comments. Developed as part of the Alx_DjangoLearnLab to showcase core RESTful API design in a social media context.

## Tech Stack
Python 3.x

Django

Django REST Framework

SQLite (default for development)

Token Authentication

Installation & Setup
bash
# Clone the repository
git clone https://github.com/edomcode/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# (Optional) Create a superuser for admin access
python manage.py createsuperuser

# Start the development server
python manage.py runserver
API Root
Once the server is running, visit:

Code
http://127.0.0.1:8000/api/
You’ll see the default root view provided by Django REST Framework’s DefaultRouter. It returns metadata like:

json
{
  "name": "Api Root",
  "description": "The default basic root view for DefaultRouter",
  "renders": ["application/json", "text/html"],
  "parses": ["application/json", "application/x-www-form-urlencoded", "multipart/form-data"]
}
This confirms your API is live and ready to serve requests.

 Authentication
This API uses Token Authentication. To access protected endpoints:

Obtain a token via login or registration.

Include the token in your request headers:

http
Authorization: Token your_token_here