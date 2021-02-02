# We Do Takeaway - Application Server
The application server is responsible for providing a GraphQL API to We Do Takeaway client application, and a basic admin tool to manage data.

The server is written using Python and Django. The GraphQL API is built with Ariadne.

## Developer instructions
These notes help you build and run the server locally for development.

### Requirements

* Python 3.7 and above
* Access to a Postgres database

MacOS comes with Python3 already installed (open a terminal and type `python3 --version`). Linux too, though Windows users will have to install Python. Alternatively use a package manager such as [Homebrew](https://brew.sh/) to install Python or goto [Python.org](https://www.python.org/) and follow the instructions to get Python 3 working.

Dependencies for the project are managed using [Poetry](https://python-poetry.org/). If you do not already have Poetry installed then follow [these instruction](https://python-poetry.org/docs/#installation).

Checkout the code and then install the dependecies using `poetry install`. After that it's up to you how you run stuff. You can use the poetry command line or Pycharm has a Poetry plugin.

The next step is create a database in Postgres for the service and then create a `.env` file and put your connection details in there:

```
# .env

DATABASE_URL=postgres://user:password@db-host/db-name
SECRET_KEY=wellputsometinguniqueinhere
```

After this is all done use the standard Django commands to set-up your database

```
manage.py migrate
manage.py loaddata menu/fixtures/data.json
```

Then create a user in django

```
manage.py createsuperuser
```

Finally start up the server

```
manage.py runserver
```