# Welcome to Quiz App!

quiz_app is a simple Web Quiz Appliaction written in Django

# Stack 

1) Python 3.11 
2) Django 4.1.3


# Quick start with Docker 

1) Open `docker-compose.yml`

2) Fill in your `DJANGO_SECRET KEY` here:
```
	environment:
      - DEBUG=1
      - DJANGO_SECRET_KEY=""
```

3) `docker compose up --build` in your terminal


# Documentation 

## Authorization 

Basic Django Authorization system is implemented. You can log in / log out of your profile. Registration of new users is planned. 

When initializing project with Docker, a superuser instance with `username=admin` and `password=12345` is automatically created 

## Taking the Quiz 

Once you are logged in, you are allowed to take quizes.

The quiz progress is saved,  when you send a `GET` request to `quiz/{quizId}/question`, the system will load the `i + 1` question, where `i` is index of last question you answered. If `i+1` is not a valid index(`i` index was the last one in the quiz) - you will be redirected to the results page and all of your answers will be transfered into `UserResult` instance, so next time you want to take the quiz, you will start it from the begining.

UPD. You also have a test quiz initialized with docker.

# Local settings 

You are always allowed to create `local_settings.py` at project level (where manage.py is located) and redefine something. 

