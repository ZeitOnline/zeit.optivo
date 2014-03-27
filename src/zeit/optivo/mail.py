import zeit.optivo.connection
import zeit.optivo.interfaces
import zope.component
import zope.interface


class Optivo(object):

    zope.interface.implements(zeit.optivo.interfaces.IOptivo)

    @classmethod
    def setup(cls, username, password):
        zope.component.provideUtility(
            zeit.optivo.connection.Session(username, password))
        zope.component.provideUtility(
            zeit.optivo.connection.Mailing())
        return cls()

    def send(self, mandant, subject, html, text):
        pass

    def test(self, mandant, to, subject, html, text):
        pass
