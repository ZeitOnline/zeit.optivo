from zeit.optivo.testing import settings
import unittest
import zeit.optivo.connection


class APITest(unittest.TestCase):

    def test_login(self):
        api = zeit.optivo.connection.Session(
            settings['username'], settings['password'])
        id = api.login(settings['mandant'])
        self.assertNotEqual(None, id)
        api.logout(id)
