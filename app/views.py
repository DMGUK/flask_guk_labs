import json
import random
from http.cookies import SimpleCookie

from flask import render_template, request, redirect, url_for, session, make_response, jsonify
from platform import system as os_name
from datetime import datetime

from app import app

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

@app.route('/')
def base():
    return render_template('base.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2])


@app.route('/homepage')
def homepage():
    return render_template('homepage.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2])

@app.route('/about_me')
def about_me():
    return render_template('about_me.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2])

@app.route('/my_experience')
def my_experience():
    return render_template('my_experience.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2])

@app.route('/my_projects')
def my_projects():
    return render_template('my_projects.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2])

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
    return render_template('contacts.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2])

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_failure = False

    with open('app/admin.json') as f:
        admin_data = json.load(f)

    json_username = admin_data['username']
    json_password = admin_data['password']

    if request.method == "POST":
        form_username = request.form.get("username")
        form_password = request.form.get("password")
        if form_username == json_username and form_password == json_password:
            user_id = random.randint(1, 10000)
            session['userId'] = user_id
            session['username'] = form_username
            session['password'] = form_password
            return redirect(url_for("info"))
        else:
            login_failure = True
    return render_template("login.html", user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2], login_failed=login_failure)

@app.route('/info', methods=['GET'])
def info():
    cookies = request.cookies
    return render_template('info.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2], cookies=cookies)

@app.route('/logout')
def logout():
    session.pop('userId')
    session.pop('username')
    session.pop('password')
    return redirect(url_for('login'))

def set_cookie(key, value, max_age):
    response = make_response(render_template('cookie_added_page.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2]))
    response.set_cookie(key, value, max_age=max_age)
    return response

def delete_cookie(key):
    response = make_response(render_template('cookie_deleted_page.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2]))
    response.delete_cookie(key)
    return response

@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    max_age = int(request.form.get('max_age'))

    return set_cookie(key, value, max_age)

@app.route('/remove_cookie/', methods=['GET'])
@app.route('/remove_cookie/<key>', methods=['GET'])
def remove_cookie():

    key = request.args.get('key')

    if key:
        response = make_response(render_template('cookie_deleted_page.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2]))
        response.delete_cookie(key)
        return response
    else:
        response = make_response(render_template('cookie_deleted_error_page.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2]))
        return response

@app.route('/remove_all_cookies', methods=['GET'])
def remove_all_cookies():
    response = make_response(render_template('all_cookies_deleted_page.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2]))
    cookies = request.cookies

    for key in cookies.keys():
        if key != 'session':
            response.delete_cookie(key)

    return response

@app.route('/change_password', methods=['POST'])
def change_password():
    new_password = request.form.get('new_password')
    session['password'] = new_password
    return render_template('password_changed.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2])