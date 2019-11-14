from zope.cachedescriptors.property import Lazy as cachedproperty
import contextlib
import threading
import zeep
import zeep.exceptions
import zeit.optivo.interfaces
import zope.interface


class WebService(object):
    """This class handles the configuration of URL and authentication
    information, and provides better error handling for errors returned by the
    web service.
    """

    base_url = 'https://api.broadmail.de/soap11'

    def __init__(self):
        self.lock = threading.Lock()

    @cachedproperty
    def client(self):
        # We intenionally don't cache the WSDL file, since that leads to
        # intransparent behaviour when debugging.
        # This means it is downloaded afresh every time, but that doesn't
        # occur often, as the utility is instantiated only once, so it's
        # not performance critical other otherwise bad.
        return zeep.Client(self.wsdl)

    @property
    def wsdl(self):
        return '%s/Rpc%s?wsdl' % (self.base_url, self.__class__.__name__)

    def call(self, method_name, *args, **kw):
        with self.lock:
            try:
                method = getattr(self.client.service, method_name)
                result = method(*args, **kw)
                return result
            except zeep.exceptions.Fault as e:
                raise zeit.optivo.interfaces.WebServiceError(e.message)


class Session(WebService):

    zope.interface.implements(zeit.optivo.interfaces.ISession)

    def __init__(self, username, password):
        super(Session, self).__init__()
        self.username = username
        self.password = password
        self._threadlocal = threading.local()

    @property
    def current_session(self):
        if not hasattr(self._threadlocal, 'session_id'):
            return None
        return self._threadlocal.session_id

    @current_session.setter
    def current_session(self, value):
        self._threadlocal.session_id = value

    def login(self, mandant):
        if not self.current_session:
            id = self.call('login', mandant, self.username, self.password)
            self.current_session = id
        return self.current_session

    def logout(self, session):
        self.current_session = None
        return self.call('logout', session)


@zope.interface.implementer(zeit.optivo.interfaces.ISession)
def session_from_product_config():
    # soft dependency
    import zope.app.appsetup.product
    config = zope.app.appsetup.product.getProductConfiguration(
        'zeit.optivo')
    return Session(config['username'], config['password'])


class LoggedInWebService(WebService):

    def call(self, method_name, *args, **kw):
        session_service = zope.component.getUtility(
            zeit.optivo.interfaces.ISession)
        return super(LoggedInWebService, self).call(
            method_name, *((session_service.current_session,) + args), **kw)

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError(name)
        return lambda *args, **kw: self.call(name, *args, **kw)


class Mailing(LoggedInWebService):

    zope.interface.implements(zeit.optivo.interfaces.IMailing)

    REGULAR = 'regular'

    SEND_TEST_RESULT = {
        0: 'success',
        1: 'recipient locked',
        2: 'recipient on opt-out list',
        3: 'recipient not found',
        4: 'recipient list not found',
        5: 'recipient not in focus group',
        6: 'too many bounces',
    }


class RecipientList(LoggedInWebService):

    zope.interface.implements(zeit.optivo.interfaces.IRecipientList)

    def find_list_by_name(self, name):
        for id in self.getAllIds():
            if self.getName(id) == name:
                return id


class Recipient(LoggedInWebService):

    zope.interface.implements(zeit.optivo.interfaces.IRecipient)

    ADD_RESULT = {
        0: 'success',
        1: 'invalid address',
        2: 'on opt-out list',
        3: 'blacklisted',
        4: 'too many bounces',
        5: 'already exists',
        6: 'filtered',
        7: 'unknown error',
    }

    def create_if_not_exists(self, list_id, email):
        if self.contains(list_id, email):
            return
        NO_OPT_IN = 0
        result = self.add2(
            list_id, NO_OPT_IN, email, email, ['lastname'], [email])
        result = self.ADD_RESULT.get(result, 'unknown error')
        if result not in ['success', 'already exists']:
            raise zeit.optivo.interfaces.WebServiceError(
                'Adding recipient %r failed: %s' % (email, result))


@contextlib.contextmanager
def login(mandant):
    session_service = zope.component.getUtility(
        zeit.optivo.interfaces.ISession)
    id = session_service.login(mandant)
    try:
        yield id
    finally:
        session_service.logout(id)
