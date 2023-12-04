import io
import unittest
from flask import url_for
from flask_login import current_user
from app import db
from app.accounts.models import Users
from tests.base import BaseTestCase


class UserTestCase(BaseTestCase):
    def test_register_user(self):
        """
        Test if a user with specific credentials exists and its password is not plaintext.
        """
        user = Users.query.filter_by(username='dmytro').first()
        assert user.username == 'dmytro'
        assert user.email == 'dmytro@gmail.com'
        assert user.password != 'dmytro_password_111'

    def test_register_post(self):
        """
        Test the registration process by simulating a POST request and checking if a user is created.
        """
        with self.client:
            response = self.client.post(
                url_for('accounts.signup'),
                data=dict(username='test', email='test@gmail.com', password='password', confirm_password='password'),
                follow_redirects=True
            )

            self.assertIn(b'You have successfully signed up.', response.data)
            user = Users.query.filter_by(email='test@gmail.com').first()
            assert response.status_code == 200
            assert user.email == 'test@gmail.com'

    def test_can_login_user(self):
        """
        Test if a user can successfully log in and authentication status is set to True.
        """
        with self.client:
            response = self.client.post(
                url_for('accounts.login'),
                data=dict(email='dmytro@gmail.com', password='dmytro_password_111', remember=True),
                follow_redirects=True
            )
            assert response.status_code == 200
            assert current_user.is_authenticated == True
            self.assertIn(b"You have logged in.", response.data)

    def test_can_login_user_remember_me_error(self):
        """
        Test login functionality with remember me option disabled.
        """
        with self.client:
            response = self.client.post(
                url_for('accounts.login'),
                data=dict(email='dmytro@gmail.com', password='dmytro_password_111'),
                follow_redirects=True
            )
            assert response.status_code == 200
            assert current_user.is_authenticated == False
            self.assertIn(b"Please, check your input again.", response.data)


    def test_register_incorrect_confirm_input_error(self):
        """
        Test registration failure due to incorrect password confirmation input.
        """
        with self.client:
            response = self.client.post(
                url_for('accounts.signup'),
                data=dict(username='test', email='test@gmail.com',
                          password='password', confirm_password='another_password'),
                follow_redirects=True
            )

            assert response.status_code == 200
            self.assertIn(b'The confirmation input is not equal to password input.', response.data)

    def test_register_incorrect_image_file_extension_error(self):
        """
        Test registration failure due to an invalid file extension for image upload.
        """
        with self.client:
            response = self.client.post(
                url_for('accounts.signup'),
                data=dict(username='test', email='test@gmail.com',
                          password='password', confirm_password='password',
                          image_file=(io.BytesIO(b'my file contents'), 'random_file.txt')),
                follow_redirects=True
            )
            assert response.status_code == 200
            self.assertIn(b'File does not have an approved extension', response.data)

    def test_register_invalid_email_error(self):
        """
        Test registration failure due to an invalid email format.
        """
        with self.client:
            response = self.client.post(
                url_for('accounts.signup'),
                data=dict(username='test', email='testgmailcom',
                          password='password', confirm_password='password'),
                follow_redirects=True
            )
            assert response.status_code == 200
            self.assertIn(b'Invalid email', response.data)

    def test_login_invalid_email_error(self):
        """
        Test login failure due to an invalid email format.
        """
        with self.client:
            response = self.client.post(
                url_for('accounts.login'),
                data=dict(email='dmytrogmailcom', password='dmytro_password_111', remember=True),
                follow_redirects=True
            )
            assert response.status_code == 200
            assert current_user.is_authenticated == False
            self.assertIn(b"Invalid email", response.data)

    def test_sign_up_page(self):
        """
        Test if the sign-up page loads properly with a 200 status code and expected content.
        """
        with self.client:
            response = self.client.get(url_for('accounts.signup'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Sign Up form', response.data)

    def test_login_page(self):
        """
        Test if the login page loads properly with a 200 status code and expected content.
        """
        with self.client:
            response = self.client.get(url_for('accounts.login'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login form', response.data)

    def test_get_account_page(self):
        """
        Test if the account page loads after logging in and contains specific user information.
        """
        user = Users(username='test_user', email='test@example.com', password='password123', image_file='image1.png')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post(
                url_for('accounts.login'),  # Log in the user
                data=dict(email='test@example.com', password='password123', remember=True),
                follow_redirects=True
            )
            assert response.status_code == 200
            response = self.client.get('/account', follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'Hi, test_user', response.data)  # Check for a string present on the account page

    def test_update_account_info(self):
        """
        Test if user account information updates properly after simulating an account update.
        """
        user = Users(username='test_user', email='test@example.com', password='password123', image_file='image1.png')
        db.session.add(user)
        db.session.commit()
        with self.client:
            self.client.post(
                url_for('accounts.login'),
                data=dict(email='test@example.com', password='password123', remember=True),
                follow_redirects=True
            )
            new_username = 'updated_username'
            new_email = 'updated@example.com'
            response = self.client.post(
                url_for('accounts.account'),
                data=dict(username=new_username, email=new_email),
                follow_redirects=True
            )
            self.assert200(response)
            self.assertIn(b'Account information updated successfully!', response.data)
            updated_user = Users.query.filter_by(email=new_email).first()
            self.assertIsNotNone(updated_user)
            self.assertEqual(updated_user.username, new_username)


if __name__ == "__main__":
    unittest.main()