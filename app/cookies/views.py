from flask import request, render_template, make_response, redirect, flash, url_for
from flask_login import login_required
from . import cookies

session_cookie_keys = ['session', 'pga4_session', 'remember_token']

@cookies.route('/info', methods=['GET'])
@login_required
def info():
    cookies = request.cookies
    return render_template('info.html', cookies=cookies)


def set_cookie(key, value, max_age):
    response = make_response(redirect('info'))
    response.set_cookie(key, value, max_age=max_age)
    return response

def delete_cookie(key):
    response = make_response(redirect('cookies.info'))
    response.delete_cookie(key)
    return response

@cookies.route('/add_cookie', methods=['POST'])
def add_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    max_age = request.form.get('max_age')

    if key != '' and value != '' and max_age != '':
        flash(f"Cookie has been added successfully!", category='flash-success')
        return set_cookie(key, value, int(max_age))

    flash(f"There has been error while adding the cookie", category='flash-error')
    return redirect(url_for('info'))

@cookies.route('/remove_cookie/', methods=['GET'])
@cookies.route('/remove_cookie/<key>', methods=['GET'])
@login_required
def remove_cookie(key=None):

    key = request.args.get('key')

    if key:
        response = make_response(redirect(url_for('cookies.info')))
        response.delete_cookie(key)
        flash("Cookie has been deleted successfully.", category='flash-success')
        return response
    else:
        flash("Please provide a key to remove.", category='flash-error')
        return redirect(url_for('cookies.info'))

@cookies.route('/remove_all_cookies', methods=['GET'])
@login_required
def remove_all_cookies():
    response = make_response(redirect('info'))
    cookies = request.cookies

    for key in cookies.keys():
        if key not in session_cookie_keys:
            response.delete_cookie(key)

    flash("All cookies removed successfully!", category='flash-success')
    return response
