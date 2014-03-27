from zope.cachedescriptors.property import Lazy as cachedproperty
import suds.cache
import suds.client
import threading
import urlparse
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
        client = suds.client.Client(
            self.wsdl,
            # disable caching of the WSDL file, since it leads to intransparent
            # behaviour when debugging.
            # This means it is downloaded afresh every time, but that doesn't
            # occur often, as the utility is instantiated only once, so it's
            # not performance critical other otherwise bad.
            cache=suds.cache.NoCache())
        return client

    @property
    def wsdl(self):
        return '%s/Rpc%s?wsdl' % (self.base_url, self.__class__.__name__)

    def call(self, method_name, *args, **kw):
        with self.lock:
            try:
                method = getattr(self.client.service, method_name)
                result = method(*args, **kw)
                return result
            except suds.WebFault, e:
                raise zeit.optivo.interfaces.WebServiceError(
                    e.fault.faultstring)

    @property
    def namespace(self):
        return 'urn:%s/Rpc%s' % (
            urlparse.urlparse(self.base_url).netloc, self.__class__.__name__)

    def create(self, type_):
        return self.client.factory.create('{%s}%s' % (self.namespace, type_))


class Session(WebService):

    zope.interface.implements(zeit.optivo.interfaces.ISession)

    def __init__(self, username, password):
        super(Session, self).__init__()
        self.username = username
        self.password = password

    @classmethod
    @zope.interface.implementer(zeit.optivo.interfaces.ISession)
    def from_product_config(cls):
        # soft dependency
        import zope.app.appsetup.product
        config = zope.app.appsetup.product.getProductConfiguration(
            'zeit.optivo')
        return cls(config['username'], config['password'])

    def login(self, mandant):
        return self.call('login', mandant, self.username, self.password)

    def logout(self, session):
        return self.call('logout', session)


class Mailing(WebService):

    zope.interface.implements(zeit.optivo.interfaces.IMailing)
