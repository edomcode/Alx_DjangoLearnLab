#  Social Media API

A Django REST Framework-based API that allows users to create, view, update, and delete posts and comments. Built as part of the **Alx_DjangoLearnLab** project to demonstrate core backend functionality in a social media context.

---

##  Tech Stack

- Python 3.x
- Django
- Django REST Framework
- SQLite (default)
- Token Authentication

---

##  Installation & Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations posts
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
