# -*-coding: utf-8-*-

import cgi
import html
import http.cookies
import os
import datetime

def get_cookie(_match):
    if 'HTTP_COOKIE' in os.environ:
        cookies = os.environ['HTTP_COOKIE']
        cookies = cookies.split('; ')
        for cookie in cookies:
            try:
                (_name, _value) = cookie.split('=')
                if (_match.lower() == _name.lower()):
                    return _value
            except:
                return ('')
    return ('')

def save_cookie(name, value, path="/", expires=None):
    cookie = http.cookies.SimpleCookie()
    cookie[name] = value
    cookie[name]["path"] = path
    if expires:
        expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        cookie[name]["expires"] = expiration.strftime("%a, %d %b %Y %H:%M:%S GMT")
    print(f"Set-Cookie: {cookie.output(header='', sep='')}")

def increment_counter():
    counter = int(get_cookie("counter") or 0)
    counter += 1
    save_cookie("counter", str(counter), expires=True)

form = cgi.FieldStorage()

try:
    username = form.getfirst("username", "")
    age = form.getfirst("age", "")
    username = html.escape(username)
    age = html.escape(age)

    mood = form.getfirst("mood", "You didn't say anything about your mood")

    music_genres = ["jazz", "ambient", "classical", "rap", "hip-hop"]
    music_genres_checkbox = {}
    for genre in music_genres:
        value_choice = form.getvalue(genre, "off")
        music_genres_checkbox[genre] = value_choice

    # Save cookies
    save_cookie("username", username)
    save_cookie("age", age)
    save_cookie("mood", mood)
    save_cookie("music_genres", music_genres_checkbox)

    # Increment counter
    increment_counter()

except (NameError, KeyError) as e:
    message = "You haven't entered any info about you, please take the quiz again"
    lang = None
    print(message)

print("Content-type:text/html\r\n\r\n")

username_cookie = get_cookie("username")
age_cookie = get_cookie("age")
mood_cookie = get_cookie("mood")

username_cookie_value = username_cookie if username_cookie else None
age_cookie_value = age_cookie if age_cookie else None
mood_cookie_value = mood_cookie if mood_cookie else None

selected_genres = [genre for genre, value in music_genres_checkbox.items() if value == "on"]
selected_genres_str = "\n".join([f"<li>{genre}</li>" for genre in selected_genres])

counter_value = get_cookie("counter") or "0"

template_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" charset = "UTF-8" content="width=device-width, initial-scale=1.0">
    <title>Quiz results</title>
</head>
<body>
    <h1> Hi, {username_cookie_value} </h1>
    <h2> Your age is : {age_cookie_value}</h2>
    <h2> Your mood today is : {mood_cookie_value} </h2>
    <h2> Selected Music Genres:</h2>
    <ul>
        <b>{selected_genres_str}</b>
    </ul>
    <h2>Number of times you passed this quiz: {counter_value}</h2>
    <form action = delete_cookie.py>    
        <input type="submit" value="Delete all cookies"><br><br>
    </form>
    <form action = cookie_counter.py>    
        <input type="submit" value="Get the number of cookies"><br><br>
    </form>
</body>
</html>
"""
template_html = template_html.format(selected_genres=selected_genres_str)
print(template_html)
