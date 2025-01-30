[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/d2zEkl7e)
# CS_2024_project

## Description

The project consist of an application for advicing you a training programme, i.e. a set of exercises united in workout trainings. It supports tracking your progress, helping you track pauses between sets of exercises, and also you can even create your own WorkOut routine and add your own exercises to it, as well as delete them anytime. They will stay saved in the database until you delete them.

## Setup

```
docker-compose up --build

```
After that you can open http://localhost:8080/ and view the application.

You can view the API documentation on http://localhost:8080/api/docs/ .

To add: web app.

## Requirements

Flask
requests
pytest
flask_sqlalchemy
flask-restx
flask-swagger-ui==4.11.1

or

Docker

## Features

* Has a database with already added (by me) exercises and whole workout routines.
* Supports creating your own workout routines and adding or deleting exercises from it.
* Supports a timer that helps track time between sets.
* (to be added) Training mode

## Git

"Master" branch, https://github.com/nup-csai/flask-project-TimaDegt/tree/master

## Success Criteria

* The project can be built without mistakes
* The project's features work
* The project passes the tests
* The project can be used in real life (for trainings)
