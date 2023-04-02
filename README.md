# Demo API project using Django Rest Framework

This is a demo API project which is built using Django Rest Framework. 

## Requirements

- Python 3.10
* Django 4.1.7
+ Djangorestframework 3.14.0

## Installation

After you cloned the repository, you want to create a virtual environment, so you have a clean python installation. You can do this by running the command

```shell
python -m venv env
```

After this, it is necessary to activate the virtual environment, you can get more information about this [here](https://docs.python.org/3/tutorial/venv.html)

You can install all the required dependencies by running 

```shell
pip install -r requirements.txt
```

## Use

First, we have to start up Django's development server. To do so, run the following command.

```shell
python manage.py runserver
```

Another way to run this project is to run it in Docker container. To do so, you first need to install Docker in your machine, and run the following commands

```shell
docker build -t <container-name> .
```

Once it is built, you can run the following command to run the docker container

```shell
docker run -p 8000:8000 <container-name>
```

The Django server will be live on port 8000. 

We can test the API using curl, Postman, or you can choose the platform of your own choice.

## Structure

In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PUT, DELETE. In this demo, we have implemented two HTTP methods, i.e., GET and POST, and our demo API exposes 3 endpoints as explained below.

|     Endpoint  | HTTP Method   |  Result  |
| ------------- | ------------- |----------|
| `who-made-me`   | GET           |Returns information of the creator and fun-fact about him/her|
| `number-to-word`| POST          |Takes an integer input between 0-9 and returns the corresponding string|
| `get-word`      | GET           |Calls a [English Dictionary](https://dictionaryapi.dev/) public API to get information about verb examples and word definitions|

## Architecture

![alt text](https://raw.githubusercontent.com/syedmuhamaddanish/Demo-Api/main/App%20Architecture.jpg)

## Test

The tests are written in Django Test Framework. You can use the following command to run Django tests

```shell
python manage.py test
```
