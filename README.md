
# DjangoPollsProMaxPlus

DjangoPollsProMaxPlus is a comprehensive polling application built with Django, featuring a frontend interface, admin interface, REST API, model, serializer, authentication, and logging. This project showcases a full-stack implementation, demonstrating skills in web development, API design, and backend management.

## Features

- **Frontend Interface**: User-friendly web interface for creating and participating in polls.
- **Admin Interface**: Management interface for handling polls, questions, and responses.
- **REST API**: Endpoints for CRUD operations on polls, questions, and choices with activity logging.
- **Model**: Robust database models for handling poll data.
- **Serializer**: Custom serializers for data conversion and logging.
- **Authentication**: Secure user authentication system.
- **Logging**: Detailed logging of model changes and API activities.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/seogenis/DjangoPollsProMaxPlus.git
   cd DjangoPollsProMaxPlus
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```plaintext
DjangoPollsProMaxPlus/
├── mysite/
│   ├── polls/
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── templates/
│   │   │   ├── polls/
│   │   │       ├── index.html
│   │   │       ├── detail.html
│   │   │       ├── results.html
│   │   ├── static/
│   │       ├── polls/
│   │           ├── css/
│   │           ├── js/
│   │           ├── images/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
├── manage.py
├── README.md
├── requirements.txt
├── .gitignore
```

## Key Files and Their Roles

### `polls/models.py`

Defines the database models for the application, including `Question`, `Choice`, and `ObjectLog` for logging activities.

### `polls/serializers.py`

Contains the serializers for `Question`, `Choice`, and a custom `LoggedModelSerializer` to handle logging of API activities.

### `polls/views.py`

Implements views for handling web and API requests, including CRUD operations and logging.

### `polls/urls.py`

Defines URL patterns for routing requests to the appropriate views.

### `polls/tests.py`

Includes test cases for ensuring the functionality of the application components.

## Contribution

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
