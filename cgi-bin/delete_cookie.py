headerString = (f"""Content-type: text/html\n
    <title>Result</title>
    <meta charset="UTF-8">
    <script>alert("Cookies have been successfully deleted. Redirecting....");</script>
    <meta http-equiv="refresh" content="0;url=http://localhost:9999/" />
    <center>
""")


print("Set-Cookie: languageradio=This could be anything. The important part is the key name xml_edit_tool;expires=Wed, 28 Aug 2013 18:30:00 GMT")
print("Set-Cookie: username=This could be anything;expires=Wed, 28 Aug 2013 18:30:00 GMT")
print("Set-Cookie: language=anything;expires=Wed, 28 Aug 2013 18:30:00 GMT")
print('Content-Type: text/html')
redirectURL = "http://localhost:9999/"
print(headerString)
print('Location: %s' % redirectURL)

print('Redirecting... <a href="%s">Click here if you are not redirected</a>' % redirectURL)

