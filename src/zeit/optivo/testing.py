import logging
import zeit.optivo.interfaces
import zope.interface


log = logging.getLogger(__name__)


@zope.interface.implementer(zeit.optivo.interfaces.IOptivo)
class Optivo:

    def __init__(self):
        self.reset()

    def reset(self):
        self.calls = []

    def send(self, mandant, recipientlist, subject, html, text):
        self.calls.append(
            ('send', mandant, recipientlist, subject, html, text))
        log.info('Optivo.send(%s)', dict(
            mandant=mandant, subject=subject, html=html, text=text))

    def test(self, mandant, recipientlist, to, subject, html, text):
        self.calls.append(
            ('test', mandant, recipientlist, to, subject, html, text))
        log.info('Optivo.test(%s)', dict(
            mandant=mandant, to=to,
            subject=subject, html=html, text=text))
