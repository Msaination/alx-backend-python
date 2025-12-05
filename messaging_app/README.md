📬 Messaging App local
A Django-based messaging application with modular structure, RESTful API endpoints, and best-practice configuration.
🚀 Project Setup
Prerequisites

    Python 3.10+

    Django 5+

    PostgreSQL (or SQLite for development)

    Virtual environment (venv)

Installation
# Clone repository
git clone https://github.com/yourusername/messaging_app.git
cd messaging_app

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver

🔑 Environment Configuration

Use a .env file for secrets and environment variables:
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/messaging_db
ALLOWED_HOSTS=localhost,127.0.0.1

Load with django-environ in settings/base.py:
import environ
env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
DATABASES = {"default": env.db()}

🧩 Models Overview

    User: Django’s built-in User model.

    ChatRoom: Represents group or one-to-one conversations.

    Message: Stores sender, content, timestamp, and read status.

    UserProfile: Extends User with avatar and bio (optional).

🌐 API Endpoints
ChatRooms

    GET /api/v1/chatrooms/ → List all chatrooms

    POST /api/v1/chatrooms/ → Create new chatroom

    GET /api/v1/chatrooms/<id>/ → Retrieve single chatroom

    PUT /api/v1/chatrooms/<id>/ → Update chatroom

    DELETE /api/v1/chatrooms/<id>/ → Delete chatroom

Messages

    GET /api/v1/messages/ → List all messages

    POST /api/v1/messages/ → Send new message

    GET /api/v1/messages/<id>/ → Retrieve single message

    PUT /api/v1/messages/<id>/ → Update message (e.g., mark as read)

    DELETE /api/v1/messages/<id>/ → Delete message

Nested Routes

    GET /api/v1/chatrooms/<id>/messages/ → List messages in a chatroom

🛡 Security

    Configure ALLOWED_HOSTS properly.

    Use .env for credentials.

    Enable CORS with django-cors-headers.

🧪 Testing

Run unit tests with Django’s test client:
python manage.py test

Use Postman/Insomnia for manual API validation.
📑 Documentation

    Inline comments in models/views.

    Auto-generated API docs with drf-yasg:

        Visit /api/v1/docs/ for Swagger UI.

📂 Project Structure
messaging_app/
├── apps/
│   ├── chats/
│   └── accounts/
├── core/
├── settings/
│   ├── base.py
│   ├── dev.py
│   └── prod.py
├── manage.py
└── README.md
✅ This README gives you a clear, executive-ready reference for setup, configuration, and API usage.

📬 Messaging App
A Django-based messaging application with modular structure, RESTful API endpoints, and best-practice configuration.
🚀 Project Setup
Prerequisites

    Python 3.10+

    Django 5+

    PostgreSQL (or SQLite for development)

    Virtual environment (venv)

Installation
# Clone repository
git clone https://github.com/yourusername/messaging_app.git
cd messaging_app

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver

🔑 Environment Configuration

Use a .env file for secrets and environment variables:
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/messaging_db
ALLOWED_HOSTS=localhost,127.0.0.1

Load with django-environ in settings/base.py:
import environ
env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
DATABASES = {"default": env.db()}

🧩 Models Overview

    User: Django’s built-in User model.

    ChatRoom: Represents group or one-to-one conversations.

    Message: Stores sender, content, timestamp, and read status.

    UserProfile: Extends User with avatar and bio (optional).

🌐 API Endpoints
ChatRooms

    GET /api/v1/chatrooms/ → List all chatrooms

    POST /api/v1/chatrooms/ → Create new chatroom

    GET /api/v1/chatrooms/<id>/ → Retrieve single chatroom

    PUT /api/v1/chatrooms/<id>/ → Update chatroom

    DELETE /api/v1/chatrooms/<id>/ → Delete chatroom

Messages

    GET /api/v1/messages/ → List all messages

    POST /api/v1/messages/ → Send new message

    GET /api/v1/messages/<id>/ → Retrieve single message

    PUT /api/v1/messages/<id>/ → Update message (e.g., mark as read)

    DELETE /api/v1/messages/<id>/ → Delete message

Nested Routes

    GET /api/v1/chatrooms/<id>/messages/ → List messages in a chatroom

🛡 Security

    Configure ALLOWED_HOSTS properly.

    Use .env for credentials.

    Enable CORS with django-cors-headers.

🧪 Testing

Run unit tests with Django’s test client:
python manage.py test

Use Postman/Insomnia for manual API validation.
📑 Documentation

    Inline comments in models/views.

    Auto-generated API docs with drf-yasg:

        Visit /api/v1/docs/ for Swagger UI.

📂 Project Structure
messaging_app/
├── apps/
│   ├── chats/
│   └── accounts
├── core/
├── settings/
│   ├── base.py
│   ├── dev.py
│   └── prod.py
├── manage.py
└── README.md
✅ This README gives you a clear, executive-ready reference for setup, configuration, and API usage.
