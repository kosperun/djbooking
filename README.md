# dj-booking

A Django backend for a lodging reservation application, inspired by `booking.com`. Incorporates some of the best practices from the [HackSoft Django Styleguide](https://github.com/HackSoftware/Django-Styleguide).

Tech Stack
Core Frameworks & Libraries

- `Django`
- `Django Rest Framework (DRF)` & `drf-nested-routers` - for building RESTful APIs
- `drf-spectacular` - for OpenAPI documentation (`swagger`)
- `djangorestframework-simplejwt` - JWT authentication
- `Stripe` & `dj-stripe` - payments processing, refunds and bookkeeping
- `Celery` - for asynchronous and scheduled tasks (e.g., email notifications)
- `Redis` - Celery backend for task management
- `SendGrid` - email provider

Code Quality & Testing

- `pytest`
- `factory-boy` & `faker`  - generating realistic test data
- `pylint`, `black`, `flake8`, `isort` - code formatting and linting
- `pre-commit` - ensures clean, properly formatted commits
