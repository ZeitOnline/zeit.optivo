import zope.interface


class IOptivo(zope.interface.Interface):
    """XXX docme"""

    def send(mandant, recipientlist, subject, html, text):
        """Create and send a mailing.

        A multipart/alternative mailing is created and sending
        to the given recipient list is started.
        """

    def test(mandant, recipientlist, to, subject, html, text):
        """Create a mailing and perform a test sending to the given ``to``
        email address."""


class WebServiceError(Exception):
    """The web service was unable to process a request because of semantic
    problems.
    """


# Utilities representing the individual web services (internal use only)

class ISession(zope.interface.Interface):
    pass


class IMailing(zope.interface.Interface):
    pass


class IRecipientList(zope.interface.Interface):
    pass


class IRecipient(zope.interface.Interface):
    pass
