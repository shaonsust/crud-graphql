# CRUD_GRAPHQL

This post introduces GraphQL, designs a schema for movies and details how to create the GraphQL API with Graphene and Django.

Aside from the Django application, this repo also includes the following:

* **queries.graphql** - an exmaple of every query and mutation defined in the schema
* **movies.json** - test data

## Reference
I have followed this [blog tutorial](https://stackabuse.com/building-a-graphql-api-with-django/) to make this crud operation of graphql.

## Setting up

Clone this repo, and in the directory follow these steps:

```bash
# Create virtual environment
python3.8 -m venv env
# Activate virtual environment
. env/bin/activate
# Install dependencies
pip install -r requirements.txt
# Run DB migration
python manage.py migrate
# Optional: load test data
python manage.py loaddata movies.json
# Run the application
python manage.py runserver
```

If you go to http://127.0.0.1:8000/graphql/, you'll be able to interact with the API there.

In project folder you will find a file named queries.graphql. In this file you will find some queries that you can use to check the API is working correctly or not.