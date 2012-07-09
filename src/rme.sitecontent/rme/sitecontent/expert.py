from five import grok
from Acquisition import aq_inner
from AccessControl import Unauthorized
from zope.component import getMultiAdapter
from plone.directives import dexterity, form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from Products.statusmessages.interfaces import IStatusMessage

from rme.sitecontent import MessageFactory as _


# Interface class; used to define content-type schema.

class IExpert(form.Schema):
    """
    A specific expert type inlcuding a request form
    """


class Expert(dexterity.Item):
    grok.implements(IExpert)


class View(grok.View):
    grok.context(IExpert)
    grok.require('zope2.View')
    grok.name('view')

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
            # timeframe = self.request.get('form.name.timeframe', None)
            if not email or email is None:
                self.errors['email'] = _(u"A valid E-mail address is required")
            elif not project or project is None:
                self.errors['project'] = _(u"Please describe your project")
            else:
                data = {
                    'email': email,
                    'fullname': fullname,
                    'project': project
                }
                self._send_request(data)

    def _send_request(self, data):
        context = aq_inner(self.context)
        mto = 'hallo@vorwaerts-werbung.de'
        envelope_from = 'enquiry@rent-my-expert.de'
        subject = _(u"Rent my Expert: Enquiry")
        options = dict(email=data['email'],
                       name=data['fullname'],
                       project=data['project'])
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
        target_url = context.absolute_url()
        return self.request.response.redirect(target_url)
