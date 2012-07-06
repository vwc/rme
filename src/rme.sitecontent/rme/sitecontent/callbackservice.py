from five import grok
from Acquisition import aq_inner
from AccessControl import Unauthorized
from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.statusmessages.interfaces import IStatusMessage
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
            authenticator = getMultiAdapter((context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            fullname = self.request.get('form.name.fullname', None)
            phone = self.request.get('form.name.phone', None)
            timeframe = self.request.get('form.name.timeframe', None)
            if not phone or phone is None:
                self.errors['phone'] = _(u"Phone number is required")
            else:
                data = {
                    'phone': phone,
                    'fullname': fullname,
                    'timeframe': timeframe
                }
                self._send_request(data)

    def _send_request(self, data):
        context = aq_inner(self.context)
        mto = 'hallo@vorwaerts-werbung.de'
        envelope_from = 'callback@rent-my-expert.de'
        subject = _(u"Rent my Expert: Callback Request")
        options = dict(phone=data['phone'],
                       name=data['fullname'],
                       time=data['timeframe'])
        body = ViewPageTemplateFile('callbackserviceemail.pt')(self, **options)
        mailhost = getToolByName(context, 'MailHost')
        mailhost.send(body,
                      mto=mto,
                      mfrom=envelope_from,
                      subject=subject,
                      charset='utf-8')
        IStatusMessage(self.request).addStatusMessage(
            _(u"Your request has been forwarded"),
            type="info")
        target_url = context.absolute_url() + '/@@callback-request-dispatched'
        return self.request.response.redirect(target_url)


class CallBackSent(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('callback-request-dispatched')

    def redirect_url(self):
        pstate = getMultiAdapter(
                    (self.context, self.request),
                    name=u"plone_portal_state"
                    )
        portal_url = pstate.portal_url()
        return portal_url()
