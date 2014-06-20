from zeit.optivo.testing import settings
import unittest
import zeit.optivo.connection


@unittest.skip('The test account seems to have been deactivated')
class APITest(unittest.TestCase):

    def test_login(self):
        api = zeit.optivo.connection.Session(
            settings['username'], settings['password'])
        id = api.login(settings['mandant'])
        self.assertNotEqual(None, id)
        api.logout(id)
