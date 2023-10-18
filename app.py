from flask import Flask, render_template, request
import os
from _datetime import datetime

app = Flask(__name__)

# my_skills = ["C++", "HTML & CSS", "MySQL", "JavaScript", "Java", "Python", "Linux", "PostgreSQL"]
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

@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def base():
    user_os = os.name
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('base.html', user_os=user_os, user_agent=user_agent, current_time=current_time)


@app.route('/homepage')
def homepage():
    user_os = os.name
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('homepage.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route('/about_me')
def about_me():
    user_os = os.name
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('about_me.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route('/my_experience')
def my_experience():
    user_os = os.name
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('my_experience.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route('/my_projects')
def my_projects():
    user_os = os.name
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('my_projects.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

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
    user_os = os.name
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('contacts.html', user_os=user_os, user_agent=user_agent, current_time=current_time)


if __name__ == '__main__':
    app.run()
