import os
import http.cookies

cookie_string = os.environ.get("HTTP_COOKIE")

cookies = cookie_string.split('; ')

num_cookies = 0

target_cookies = ["music_genres", "username", "age", "mood"]

for cookie in cookies:
    for cookie_name in target_cookies:
        if cookie_name in cookie:
            num_cookies += 1


print(f"Content-type: text/html\r\n\r\n")
print(f"<html><head><meta charset = 'UTF-8'></head><body><h1>Number of cookies: {num_cookies}</h1>")
print(f"""<form action = delete_cookie.py>    
            <input type="submit" value="Delete all cookies">
        </form></body></html>
       """)