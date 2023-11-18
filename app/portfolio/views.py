from flask import render_template, request
from . import portfolio
from platform import system as os_name
from datetime import datetime

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

@portfolio.route('/')
@portfolio.route('/homepage')
def homepage():
    return render_template('homepage.html', user_os=user_details()[0], user_agent=user_details()[1], current_time=user_details()[2])


@portfolio.route('/about_me')
def about_me():
    return render_template('about_me.html')

@portfolio.route('/my_experience')
def my_experience():
    return render_template('my_experience.html')

@portfolio.route('/my_projects')
def my_projects():
    return render_template('my_projects.html')

@portfolio.route('/skills/')
@portfolio.route('/skills/<int:id>')
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

@portfolio.route('/generate_link', methods=['POST'])
def generate_link():
    skill_id = request.form.get('id')
    return render_template('skills.html', skill_id=skill_id)

@portfolio.route('/contacts')
def contacts():
    return render_template('contacts.html')


