# Recipe App API

A backend REST API built with Django and Django REST Framework for managing recipes.  
The application allows authenticated users to create and manage recipes, ingredients, tags, images, and user accounts.

## Features

- User registration and token authentication
- Create, update, delete, and retrieve recipes
- Upload recipe images
- Add ingredients and tags
- Filter recipes by ingredients or tags
- Manage user-specific recipe data
- API documentation using Swagger/OpenAPI
- Dockerized development environment
- Automated testing

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker / Docker Compose
- Swagger (drf-spectacular)
- GitHub Actions (CI/CD)

## API Endpoints

### User
- Create user accounts
- Authenticate using token authentication
- Manage user profiles

### Recipes
- Create recipes
- View recipe details
- Update recipes
- Delete recipes
- Upload recipe images

### Ingredients & Tags
- Create and manage ingredients
- Create and manage tags
- Filter recipes based on assigned items

## Running Locally

Clone the repository:

```bash
git clone https://github.com/HH00254/recipe-app-api.git
```

Move into the project:

```bash
cd recipe-app-api
```

Build Docker containers:

```bash
docker compose build
```

Start the application:

```bash
docker compose up
```

Run migrations:

```bash
docker compose run --rm app sh -c "python manage.py migrate"
```

Run tests:

```bash
docker compose run --rm app sh -c "python manage.py test"
```

## API Documentation

Swagger documentation is available when running the server:

```text
/api/docs/
```

## Project Structure

```text
app/
├── core/          # Database models and core functionality
├── user/          # User authentication API
├── recipe/        # Recipe, tag, ingredient APIs
├── comments/      # Recipe comments functionality
└── app/           # Django project configuration
```

## Purpose

This project was built to strengthen backend development skills including:

- REST API design
- Authentication
- Database modeling
- Docker development workflow
- Automated testing
- Clean Django architecture

## Author

Developed by Hans Hochbaum