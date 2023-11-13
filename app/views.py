import os
import random
import secrets
from os.path import basename, splitext, isfile

from flask import render_template, request, redirect, url_for, make_response, flash
from platform import system as os_name
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from app import app, db, bcrypt
from app.forms import LoginForm, ChangePasswordForm, ToDoForm, FeedbackForm, SignUpForm, UpdateAccountForm
from flask_migrate import Migrate

from app.models import Todo, Feedback, Users
from config import ALLOWED_EXTENSIONS, MAX_IMAGE_SIZE, UPLOAD_FOLDER

migrate = Migrate(app, db)


session_cookie_keys = ['session', 'pga4_session', 'remember_token']

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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def file_exists(file_path):
    full_path = os.path.normpath(os.path.join(app.root_path, file_path.lstrip('/')))
    e = isfile(full_path)
    return isfile(full_path)


app.jinja_env.filters['file_exists'] = file_exists


def user_details():
    user_os = os_name()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return [user_os, user_agent, current_time]


def resize_and_save_image(file, destination_folder, target_size):
    img = Image.open(file)
    img.thumbnail(target_size)

    random_string = secrets.token_hex(10)
    original_filename, file_extension = os.path.splitext(secure_filename(file.filename))
    new_filename = f"{random_string}{file_extension}"
    image_path = os.path.join(destination_folder, new_filename)

    try:
        img.save(image_path)
        return image_path
    except Exception as e:
        flash(f"Error saving image: {e}", category="flash-error")
        return None

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
    if current_user.is_authenticated:
        return redirect(url_for('account'))

    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        image_file = form.image_file.data

        if image_file and allowed_file(image_file.filename):
            image_path = resize_and_save_image(image_file, UPLOAD_FOLDER, MAX_IMAGE_SIZE)
            image_path = os.path.basename(image_path)
        else:
            image_path = None

        new_user = Users(username=username, email=email, password=password, image_file=image_path)
        db.session.add(new_user)
        db.session.commit()

        flash("You have successfully signed up.", category="flash-success")
        return redirect(url_for("login"))

    return render_template("signup.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and user.validate_password(form.password.data):
            if form.remember.data == True:
                login_user(user, form.remember.data)
                flash("You have logged in.", category="flash-success")
                return redirect(url_for("account"))
            flash("You didn't remember yourself in the site. Please, check your input again.", category="flash-error")
            return redirect(url_for("login"))
        flash("You didn't put correct user credentials. Please, check them again.", category="flash-error")
        return redirect(url_for("login"))
    return render_template("login.html", form=form)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user_id = random.randint(1, 10000)
    user_image_file = current_user.image_file

    update_account_form = UpdateAccountForm(
        username=current_user.username,
        email=current_user.email,
    )

    if update_account_form.validate_on_submit():
        old_image_path = current_user.image_file
        old_file_name = os.path.basename(old_image_path)
        full_old_image_path = os.path.join(app.static_folder, 'profile_images', old_file_name)
        new_image_file = update_account_form.image.data
        if new_image_file :
            image_path = resize_and_save_image(new_image_file, UPLOAD_FOLDER, MAX_IMAGE_SIZE)
            if image_path:
                current_user.image_file = os.path.basename(image_path)
                if full_old_image_path and os.path.isfile(full_old_image_path) and user_image_file != 'default.jpg':
                    os.remove(full_old_image_path)

        current_user.username = update_account_form.username.data
        current_user.email = update_account_form.email.data
        current_user.bio = update_account_form.bio.data
        db.session.commit()
        flash("Account information updated successfully!", category='flash-success')
        return redirect(url_for('account', form=update_account_form))

    update_account_form.username.data = current_user.username
    update_account_form.email.data = current_user.email
    update_account_form.bio.data = current_user.bio
    return render_template('account.html', user_id=user_id, update_account_form=update_account_form)

@app.after_request
def after_request(response):
    if request.endpoint != 'signup' and current_user.is_authenticated:
        current_user.last_seen = datetime.now().replace(microsecond=0)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Error while updating last_seen: {str(e)}', 'flash-error')

    return response

@app.route('/users')
@login_required
def users():
    all_users = Users.query.all()

    user_data = []

    for user in all_users:
        user_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'profile_image_path': user.image_file
        })

    return render_template('users.html', user_data=user_data)


@app.route('/info', methods=['GET'])
@login_required
def info():
    cookies = request.cookies
    form = ChangePasswordForm()
    return render_template('info.html', cookies=cookies, form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have logged out.", category="flash-success")
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
@login_required
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
@login_required
def remove_all_cookies():
    response = make_response(redirect('info'))
    cookies = request.cookies

    for key in cookies.keys():
        if key not in session_cookie_keys:
            response.delete_cookie(key)

    flash("All cookies removed successfully!", category='flash-success')
    return response

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data
        if new_password != '':
            if new_password == confirm_new_password:
                current_user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                db.session.commit()

                flash("Password has been changed successfully", category='flash-success')
                return redirect(url_for('change_password'))

            flash("Error changing your password", category='flash-error')
            return redirect(url_for('change_password'))

    return render_template('change_password.html', form=form)

@app.route('/todo')
@login_required
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
@login_required
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo"))

@app.route("/delete_todo/<int:todo_id>")
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo"))


@app.route('/feedback')
@login_required
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
@login_required
def delete_feedback(todo_id):
    todo = Feedback.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash("Feedback has been successfully deleted", category='flash-success')
    return redirect(url_for("feedback"))
