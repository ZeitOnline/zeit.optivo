from datetime import datetime
import logging
import pytz
import zeit.optivo.connection
import zeit.optivo.interfaces
import zope.component
import zope.interface


log = logging.getLogger(__name__)


class Optivo(object):

    zope.interface.implements(zeit.optivo.interfaces.IOptivo)

    @classmethod
    def setup(cls, username, password):
        zope.component.provideUtility(
            zeit.optivo.connection.Session(username, password))
        zope.component.provideUtility(
            zeit.optivo.connection.Mailing())
        return cls()

    @property
    def mailing_service(self):
        return zope.component.getUtility(zeit.optivo.interfaces.IMailing)

    @property
    def recipientlist_service(self):
        return zope.component.getUtility(zeit.optivo.interfaces.IRecipientList)

    @property
    def recipient_service(self):
        return zope.component.getUtility(zeit.optivo.interfaces.IRecipient)

    def send(self, mandant, recipientlist, subject, html, text):
        with zeit.optivo.connection.login(mandant):
            log.info('Sending mail with subject "%s"', subject)
            mailing = self._create_mailing(recipientlist, subject, html, text)
            self.mailing_service.start(mailing, datetime.now(pytz.UTC))

    def test(self, mandant, recipientlist, to, subject, html, text):
        with zeit.optivo.connection.login(mandant):
            testlist = self.recipientlist_service.find_list_by_name(
                recipientlist)
            self.recipient_service.create_if_not_exists(testlist, to)
            log.info('Testing mail with subject "%s" to %s', subject, to)
            mailing = self._create_mailing(recipientlist, subject, html, text)
            result = self.mailing_service.sendTestMail(mailing, testlist, to)
            result = self.mailing_service.SEND_TEST_RESULT[result]
            if result != 'success':
                raise zeit.optivo.interfaces.WebServiceError(
                    'Sending test email failed: %s' % result)

    def _create_mailing(self, recipientlist, subject, html, text):
        list_id = self.recipientlist_service.find_list_by_name(
            recipientlist)
        mailing = self.mailing_service.create(
            self.mailing_service.REGULAR, subject, 'multipart/alternative',
            self.mailing_service._create('ArrayOf_xsd_long', [int(list_id)]),
            # XXX Make prefix and sender_name configurable or parameters.
            'Newsletter', 'ZEIT ONLINE', 'UTF-8')
        self.mailing_service.setOpenTrackingEnabled(mailing, True)
        self.mailing_service.setSubject(mailing, subject)
        self._validate_content(mailing, html, 'text/html')
        self._validate_content(mailing, text, 'text/plain')
        return mailing

    def _validate_content(self, mailing, content, mime_type):
        valid = self.mailing_service.validateContent(
            mailing, mime_type, content)
        if valid._value_1 != 'OK':
            raise zeit.optivo.interfaces.WebServiceError(
                'Invalid mailing body: %s' % valid)
        self.mailing_service.encodeTrackingLinks(mailing, content, mime_type)
        self.mailing_service.setContent(mailing, mime_type, content)
