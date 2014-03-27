import logging
import zeit.optivo.interfaces
import zope.interface


log = logging.getLogger(__name__)


settings = {
    'username': 'stefan.ehlers@zeit.de',
    'password': 'zeitonline2014',
    'mandant': '74276897418',
}


class Optivo(object):

    zope.interface.implements(zeit.optivo.interfaces.IOptivo)

    def __init__(self):
        self.reset()

    def reset(self):
        self.calls = []

    def send(self, mandant, subject, html, text):
        self.calls.append(('send', mandant, subject, html, text))
        log.info('Optivo.send(%s)', dict(
            mandant=mandant, subject=subject, html=html, text=text))

    def test(self, mandant, to, subject, html, text):
        self.calls.append(('test', mandant, to, subject, html, text))
        log.info('Optivo.test(%s)', dict(
            mandant=mandant, to=to,
            subject=subject, html=html, text=text))
