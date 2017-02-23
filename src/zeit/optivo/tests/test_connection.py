import os
import unittest
import zeit.optivo.connection


@unittest.skip('The test account seems to have been deactivated')
class APITest(unittest.TestCase):

    def test_login(self):
        env = os.environ
        api = zeit.optivo.connection.Session(
            env['ZEIT_OPTIVO_USERNAME'], env['ZEIT_OPTIVO_PASSWORD'])
        id = api.login(env['ZEIT_OPTIVO_MANDANT'])
        self.assertNotEqual(None, id)
        api.logout(id)
