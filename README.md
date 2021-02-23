![Test and Build](https://github.com/We-Do-Takeaway/wdt_server/workflows/Test%20and%20Build/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=We-Do-Takeaway_wdt_server&metric=alert_status)](https://sonarcloud.io/dashboard?id=We-Do-Takeaway_wdt_server)

# We Do Takeaway - Application Server

The application server is responsible for providing a GraphQL API to We Do Takeaway client application, and a basic admin tool to manage data.

The server is written using Python and Django. The GraphQL API is built with Ariadne.

## Developer instructions

These notes help you build and run the server locally for development.

### Requirements

- Python 3.7 and above
- Access to a Postgres database

Development required Python 3. You can use the one with your OS, install it from the Python site or a package manager like Homebrew.

One reccomended approach used on Mac, and should work on others, is to use a combination of direnv and pyenv.

1: Install direnv
1: Install pyenv
1: Install poetry
1: Tell poetry not to setup virtual environments `poetry config virtualenvs.create false` as direnv will handle that
1: Use pyenv to install the version of Python you wish to use `pyenv install 3.9.1`
1: In your source folder create a .envrc file with the first line set to `layout pyenv 3.9.1`
1: Run `direnv allow`
1: `poetry install`

Dependencies for the project are managed using [Poetry](https://python-poetry.org/). If you do not already have Poetry installed then follow [these instruction](https://python-poetry.org/docs/#installation).

Checkout the code and then install the dependecies using `poetry install`. After that it's up to you how you run stuff. You can use the poetry command line or Pycharm has a Poetry plugin.

The next step is create a database in Postgres for the service and then create a `.env` file or edit `.envrc` and put your connection details in there:

```
# .env (same for .envrc except add export to the start of each line)

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



## VSCode Workspace
This is WIP. Currently you can open this project in a vscode dev container but you will need to manually run the first `poetry install` and also run `pre-commit install`.