from five import grok
from Acquisition import aq_inner
from AccessControl import Unauthorized
from zope.component import getMultiAdapter

from plone.app.layout.navigation.interfaces import INavigationRoot

from rme.sitecontent import MessageFactory as _


class CallBackRequest(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('callback-request')

    def update(self):
        context = aq_inner(self.context)
        self.errors = {}
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((self.request, context),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            phone = self.request.get('phone', None)
            if phone is None:
                self.errors['phone'] = _(u"Phone number is required")
            else:
                request = self.request
                data = {
                    'phone': phone,
                    'fullname': request.get('fullname', ''),
                    'message': request.get('message', '')
                }
                self.send_request(data)

    def send_request(self, data):
        return ''
