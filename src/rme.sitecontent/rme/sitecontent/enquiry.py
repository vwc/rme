from five import grok
from Acquisition import aq_inner
from AccessControl import Unauthorized
from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.statusmessages.interfaces import IStatusMessage
from plone.app.layout.navigation.interfaces import INavigationRoot

from rme.sitecontent import MessageFactory as _


class EnquiryView(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('expert-enquiry')

    def update(self):
        context = aq_inner(self.context)
        self.errors = {}
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            fullname = self.request.get('form.name.fullname', None)
            email = self.request.get('form.name.email', None)
            project = self.request.get('form.name.project', None)
            tasks = self.request.get('form.name.tasks', None)
            # timeframe = self.request.get('form.name.timeframe', None)
            if not email or email is None:
                self.errors['email'] = _(u"A valid E-mail address is required")
            elif not project or project is None:
                self.errors['project'] = _(u"Please describe your project")
            else:
                data = {
                    'email': email,
                    'fullname': fullname,
                    'project': project,
                    'tasks': tasks
                }
                self._send_request(data)

    def _send_request(self, data):
        context = aq_inner(self.context)
        mto = 'hallo@vorwaerts-werbung.de'
        envelope_from = 'enquiry@rent-my-expert.de'
        subject = _(u"Rent my Expert: Enquiry")
        options = dict(email=data['email'],
                       name=data['fullname'],
                       project=data['project'],
                       tasks=data['tasks'])
        body = ViewPageTemplateFile('enquiryemail.pt')(self, **options)
        mailhost = getToolByName(context, 'MailHost')
        mailhost.send(body,
                      mto=mto,
                      mfrom=envelope_from,
                      subject=subject,
                      charset='utf-8')
        IStatusMessage(self.request).addStatusMessage(
            _(u"Your request has been forwarded"),
            type="info")
        target_url = context.absolute_url() + '/@@enquiry-dispatched'
        return self.request.response.redirect(target_url)


class EnquirySent(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('enquiry-dispatched')

    def redirect_url(self):
        pstate = getMultiAdapter(
                    (self.context, self.request),
                    name=u"plone_portal_state"
                    )
        portal_url = pstate.portal_url()
        return portal_url()
