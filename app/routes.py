from flask import render_template, redirect, url_for, request, flash, request
from app import app, db
from app.forms import LoginForm, TaskFrom, RegistrationForm
from werkzeug.urls import url_parse
from app.models import User, Task

from flask_login import current_user, login_user, logout_user, login_required


# Lists of incomplete and completed tasks
@app.route('/', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
@login_required
def index():
    itasks = Task.query.filter_by(completed=False).all()
    ctasks = Task.query.filter_by(completed=True).all()
    form = TaskFrom()
    if form.validate_on_submit():
        task = Task(body=form.task.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', form=form, itasks=itasks, ctasks=ctasks)


# logging into the application
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# logging out of the application
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Registering with the application in order to login
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Regiser', form=form)

# complete a task so that it appears in the completed task list
@app.route('/complete/<int:id>', methods=('GET', 'POST'))
@login_required
def complete(id):
    task = Task.query.get(int(id))
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

# Delete a task from the database
@app.route('/delete/<int:id>', methods=('GET', 'POST'))
@login_required
def delete(id):
    task = Task.query.get(int(id))
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Update a todo
@app.route('/update/<string:id>', methods=('GET', 'POST'))
def update(id):
    task = Task.query.get(id)
    form = TaskFrom()
    if form.validate_on_submit():
        task.body = form.task.data
        db.session.commit()
        flash('Task updated!')
        return redirect(url_for('index'))
    return render_template('update.html', form=form, task=task)

