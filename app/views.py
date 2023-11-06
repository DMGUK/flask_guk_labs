import io
import json
import random
from flask import render_template, request, redirect, url_for, session, make_response, flash, send_file
from platform import system as os_name
from datetime import datetime
from app import app, db
from app.forms import LoginForm, ChangePasswordForm, ToDoForm, FeedbackForm, SignUpForm
from flask_migrate import Migrate

from app.models import Todo, Feedback, Users

migrate = Migrate(app, db)

my_skills = [
    {"name": "C++", "logo": "cpp_logo.png"},
    {"name": "HTML & CSS", "logo": "html_css_logo.png"},
    {"name": "MySQL", "logo": "mysql_logo.png"},
    {"name": "JavaScript", "logo": "js_logo.png"},
    {"name": "Java", "logo": "java_logo.png"},
    {"name": "Python", "logo": "python_logo.png"},
    {"name": "Linux", "logo": "linux_logo.png"},
    {"name": "PostgreSQL", "logo": "postgresql_logo.png"}
]

def user_details():
    user_os = os_name()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return [user_os, user_agent, current_time]
@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# @app.route('/')
# def base():
#     return render_template('base.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2])


@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2])

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

@app.route('/my_experience')
def my_experience():
    return render_template('my_experience.html')

@app.route('/my_projects')
def my_projects():
    return render_template('my_projects.html')

@app.route('/skills/')
@app.route('/skills/<int:id>')
def skills(id=None):
    if id is not None:
        if 0 <= id < len(my_skills):
            skill = my_skills[id]["name"]
            logo = my_skills[id]["logo"]
            return render_template('skills.html', skill=skill, logo=logo)
        else:
            return render_template('skills.html')
    else:
        return render_template('skills.html', skills=my_skills, total_skills=len(my_skills))

@app.route('/generate_link', methods=['POST'])
def generate_link():
    skill_id = request.form.get('id')
    return render_template('skills.html', skill_id=skill_id)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        image_file = form.image_file.data
        if password == confirm_password:

            new_user = Users(username=username, email=email, password=password, image_file=image_file)
            db.session.add(new_user)
            db.session.commit()
        flash("You have successfully signed up.", category="flash-success")
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        form_email = form.email.data
        form_password = form.password.data
        form_remember = form.remember.data
        if user and user.validate_password(form_password) and user.email == form.email.data:
            if form_remember == True:
                user_id = random.randint(1, 10000)
                session['userId'] = user_id
                session['username'] = user.username
                session['email'] = form_email
                session['password'] = form_password
                session['remember'] = form_remember
                flash("You have logged in.", category="flash-success")
                return redirect(url_for("info"))
            flash("You didn't remember yourself in the site. Please, check your input again.", category="flash-error")
            return redirect(url_for("login"))
        flash("You didn't put correct user credentials. Please, check them again.", category="flash-error")
        return redirect(url_for("login"))
    return render_template("login.html", form=form)

@app.route('/users')
def users():
    all_users = Users.query.all()
    return render_template('users.html', all_users=all_users)

@app.route('/info', methods=['GET'])
def info():
    cookies = request.cookies
    form = ChangePasswordForm()

    return render_template('info.html', cookies=cookies, form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def set_cookie(key, value, max_age):
    response = make_response(redirect('info'))
    response.set_cookie(key, value, max_age=max_age)
    return response

def delete_cookie(key):
    response = make_response(redirect('info'))
    response.delete_cookie(key)
    return response

@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    max_age = request.form.get('max_age')

    if key != '' and value != '' and max_age != '':
        flash(f"Cookie has been added successfully!", category='flash-success')
        return set_cookie(key, value, int(max_age))

    flash(f"There has been error while adding the cookie", category='flash-error')
    return redirect(url_for('info'))

@app.route('/remove_cookie/', methods=['GET'])
@app.route('/remove_cookie/<key>', methods=['GET'])
def remove_cookie(key=None):

    key = request.args.get('key')

    if key:
        response = make_response(redirect(url_for('info')))
        response.delete_cookie(key)
        flash("Cookie has been deleted successfully.", category='flash-success')
        return response
    else:
        flash("Please provide a key to remove.", category='flash-error')
        return redirect(url_for('info'))

@app.route('/remove_all_cookies', methods=['GET'])
def remove_all_cookies():
    response = make_response(redirect('info'))
    cookies = request.cookies

    for key in cookies.keys():
        if key != 'session':
            response.delete_cookie(key)

    flash("All cookies removed successfully!", category='flash-success')
    return response

@app.route('/change_password', methods=['POST'])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        new_password = form.password.data
        confirm_new_password = form.confirm_password.data
        if new_password != '':
            if new_password == confirm_new_password:
                session['password'] = new_password

                with open('app/admin.json') as f:
                    admin_data = json.load(f)

                new_admin_data = {
                    'username': admin_data['username'],
                    'password': new_password
                }

                new_passwd_json = json.dumps(new_admin_data, indent=2)

                with open("app/admin.json", "w") as outfile:
                    outfile.write(new_passwd_json)

                flash("Password has been changed successfully", category='flash-success')
                return redirect(url_for('info'))

            flash("You didn't confirm your password", category='flash-error')
            return redirect(url_for('info'))

    flash("You didn't put any new passwords nor you confirmed any. Please, try once again", category='flash-error')
    return redirect(url_for('info'))

@app.route('/todo')
def todo():
    todolist = db.session.query(Todo).all()
    todo_form = ToDoForm()
    return render_template("todo.html", todo_list=todolist, active="ToDo", title="ToDo", todo_form=todo_form)

@app.route("/add_todo", methods=["POST"])
def add_todo():
    todo_form = ToDoForm()
    if todo_form.validate_on_submit():
        title = todo_form.title.data
        description = todo_form.description.data
        new_todo = Todo(title=title, description=description, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        flash("Todo task has been successfully added", category='flash-success')
        return redirect(url_for("todo"))
    flash("Error adding todo task", category='flash-error')
    return redirect(url_for("todo"))

@app.route("/update_todo/<int:todo_id>")
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo"))

@app.route("/delete_todo/<int:todo_id>")
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo"))


@app.route('/feedback')
def feedback():
    feedback_list = db.session.query(Feedback).all()
    feedback_form = FeedbackForm()
    return render_template("feedbacks.html", feedback_list=feedback_list, active="ToDo", title="ToDo", feedback_form=feedback_form)

@app.route("/add_feedback", methods=["POST"])
def add_feedback():
    feedback_form = FeedbackForm()
    if feedback_form.validate_on_submit():
        username = feedback_form.username.data
        feedback_body = feedback_form.feedback.data

        existing_user = Feedback.query.filter_by(username=username).first()
        if existing_user:
            flash("Username with its own feedback already exists.", category='flash-error')
            return redirect(url_for("feedback"))

        new_feedback = Feedback(username=username, feedback=feedback_body)
        db.session.add(new_feedback)
        db.session.commit()
        flash("Feedback has been successfully added", category='flash-success')
        return redirect(url_for("feedback"))
    flash("Error adding feedback", category='flash-error')
    return redirect(url_for("feedback"))

@app.route("/delete_feedback/<int:todo_id>")
def delete_feedback(todo_id):
    todo = Feedback.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash("Feedback has been successfully deleted", category='flash-success')
    return redirect(url_for("feedback"))
