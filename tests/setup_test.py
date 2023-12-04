import unittest

from tests.base import BaseTestCase


class SetupTest(BaseTestCase):
    def test_setup(self):
        """
        Test the setup of the test case by verifying the presence of the app, client, and context.
        """
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)

if __name__ == '__main__':
    unittest.main()