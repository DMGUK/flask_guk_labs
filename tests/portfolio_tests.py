import unittest
from flask import url_for
from tests.base import BaseTestCase


class PortfolioViewsTests(BaseTestCase):

    def test_home_page_loads(self):
        """
        Test if the home page loads with a 200 status code and contains 'Resume Homepage' text.
        """
        with self.client:
            response = self.client.get(url_for('portfolio.homepage'))
            self.assertEqual(response.status_code, 200)

            self.assertIn(b'Resume Homepage', response.data)

    def test_skills_page_loads(self):
        """
        Test if the skills page loads with a 200 status code and contains 'Dmytro Huk' text.
        """
        with self.client:
            response = self.client.get(url_for('portfolio.about_me'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Dmytro Huk', response.data)

    def test_my_experience_page(self):
        """
        Test if the 'My Experience' page loads with a 200 status code and contains 'Python' text.
        """
        with self.client:
            response = self.client.get(url_for('portfolio.my_experience'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Python', response.data)

    def test_my_projects_page(self):
        """
        Test if the 'My Projects' page loads with a 200 status code and contains 'PNUdev' text.
        """
        with self.client:
            response = self.client.get(url_for('portfolio.my_projects'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'PNUdev', response.data)

    def test_contacts_page(self):
        """
        Test if the 'Contacts' page loads with a 200 status code and contains 'Contacts' text.
        """
        with self.client:
            response = self.client.get(url_for('portfolio.contacts'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Contacts', response.data)


if __name__ == "__main__":
    unittest.main()