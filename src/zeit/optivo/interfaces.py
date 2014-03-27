import zope.interface


class IOptivo(zope.interface.Interface):
    """XXX docme"""


class IMailing(zope.interface.Interface):
    """XXX docme"""


class ISession(zope.interface.Interface):
    """XXX docme"""


class WebServiceError(Exception):
    """The web service was unable to process a request because of semantic
    problems.
    """
