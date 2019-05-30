# Flask Todo List app

This is a simple todo list app in flask. It uses the following dependencies:
1. Flask-login
2. Flask-sqlalchemy
3. SQLite3
4. Flask-migrate
5. Flask-wtf
6. python-dotenv
7. Flask-debugtoolbar

There is a basic CRUD functionality as well as login/logout and registration.

# Installation notes

In order to set up the app after having cloned the repository, do the following to install the required dependencies. Make sure that `pip` and `virtualenv` are installed.

* In the folder run 
```
python3 -m virtualenv venv
```` 
where `venv` is the folder name of the virtual environment.

* Then activate the virtual environment

```
source /venv/bin/activate
```
The command line prompt will then look like
```
(venv) {machine-name}:flask-todolist {username}$
```

* Finally install the requirements
```
pip install
```

