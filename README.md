# Notification Manager

## Introduction
This document provides detailed instructions for setting up and running the Notification Manager. It also includes API documentation for integrating with the developed service.

## Requirements
Before you begin, ensure you have the following software installed:
- Python 3.10
- Django 4.2.10
- Redis (for Celery)
- Celery

## Installation

### Clone the Repository
Start by cloning the project repository to your local machine:
```bash
git clone https://github.com/Kotolow/NotificationManager.git
cd NotificationManager

### Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies
Install the project dependencies using `pip`:
```bash
pip install -r requirements.txt
```

### Initialize the Database
Run the following commands to create the database tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Run the Development Server
Start the Django development server:
```bash
python manage.py runserver
```

### Start the Redis Server
In a separate terminal, start the Redis server:
```bash
redis-server
```


### Start the Celery Worker
In a separate terminal, start the Celery worker:
```bash
celery -A notification_manager worker -l info
```

## API Documentation

### Swagger API Documentation
To view the Swagger API documentation, navigate to:
- Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- ReDoc UI: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
- Swagger JSON: [http://localhost:8000/swagger.json](http://localhost:8000/swagger.json)
- Swagger YAML: [http://localhost:8000/swagger.yaml](http://localhost:8000/swagger.yaml)

The Swagger UI provides an interactive documentation interface where you can try out the API endpoints directly from the browser.

### Endpoints
Provide a list of available API endpoints with their respective HTTP methods, URI, request parameters, request body, response body, and response status codes.

### Examples
Include `curl` command examples or sample requests and responses for each endpoint.

