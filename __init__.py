# -*- coding: ISO-8859-15 -*-
# (C) Copyright 2005 Nuxeo SARL <http://nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id: zopecal.py 24305 2005-06-22 14:39:11Z lregebro $

""" CPSonFive

This product is the container for any reusable integration between CPS and Five.
"""
from types import StringTypes
from zope.schema.interfaces import ITitledTokenizedTerm
from zope.i18nmessageid.messageid import MessageID

# Zope3.0.0 doesn't translates dropdownboxes (that's a bug)
def textForValue(self, term):
    """Extract a string from the term.

    The term must be a vocabulary tokenized term.

    This can be overridden to support more complex term objects. The token
    is returned here since it's the only thing known to be a string, or
    str()able."""
    if ITitledTokenizedTerm.providedBy(term):
        return self.translate(term.title)
    return self.translate(term.token)


from zope.i18n.interfaces import IUserPreferredCharsets
from zope.interface import implements

class ISO15Charset(object):
    # This object implements the selector function for IUserPreferredCharsets
    # but doesn't care what the user prefer, It returns ISO-8859-15 anyway.
    # XXX For support of non-european languages, we need to match this with 
    # the selected UI language somehow. 
    implements(IUserPreferredCharsets)

    def __init__(self, request):
        self.request = request
        
    def getPreferredCharsets(self):
        '''See interface IUserPreferredCharsets'''
        return ['iso-8859-15']


try: # Five 1.1
    from Products.Five.form import EditView, Update, applyWidgetsChanges
except ImportError: # Five 1.0
    from Products.Five.browser import EditView, Update
from zope.app.form.interfaces import WidgetsError
from zope.app.form.utility import setUpEditWidgets, applyWidgetsChanges
from zope.app.event.objectevent import ObjectModifiedEvent
try:
    from zope.app.i18n import ZopeMessageFactory as _
except:
    from zope.app.i18n import ZopeMessageIDFactory as _
import transaction, datetime

def EditViewUpdate(self):
    if self.update_status is not None:
        # We've been called before. Just return the status we previously
        # computed.
        return self.update_status

    status = ''

    content = self.adapted

    if Update in self.request.form.keys():
        changed = False
        try:
            changed = applyWidgetsChanges(self, self.schema,
                target=content, names=self.fieldNames)
            # We should not generate events when an adapter is used.
            # That's the adapter's job.
            if changed and self.context is self.adapted:
                notify(ObjectModifiedEvent(content))
        except WidgetsError, errors:
            self.errors = errors
            status = _("An error occured.")
            transaction.abort()
        else:
            setUpEditWidgets(self, self.schema, source=self.adapted,
                             ignoreStickyValues=True,
                             names=self.fieldNames)
            if changed:
                self.changed()
                # It's going to be very nice to drop Five 1.0.x support:
                localizer = getattr(self.context, 'Localizer', None)
                if localizer is not None:
                    
                    status = localizer.default("Updated on %(date_time)s")
                    format = str(localizer.default('date_medium'))
                    date = datetime.datetime.now().strftime(format)
                    status = status % {'date_time': date}
                else:
                    status = _("Updated on ${date_time}")
                    status.mapping = {'date_time': str(datetime.utcnow())}

    self.update_status = status
    return status

# XXX: Five 1.2b and 1.3b and Zope 2.9 betas have a bug the local site 
# configuration, which can result in one class getting listed twice in the 
# list of classes that have a site hook. This monkey avoids that, and can be 
# removed once the final versions have been released:
from Products.Five.site import metaconfigure
from Products.Five.site.localsite import FiveSite
from zope.app.component.interfaces import IPossibleSite
from zope.configuration.exceptions import ConfigurationError
from zope.interface import classImplements

def installSiteHook(_context, class_, site_class=None):
    if class_ in metaconfigure._localsite_monkies:
        return # This is the workaround
    if site_class is None:
        if not IPossibleSite.implementedBy(class_):
            # This is not a possible site, we need to monkey-patch it so that
            # it is.
            site_class = FiveSite
    else:
        if not IPossibleSite.implementedBy(site_class):
            raise ConfigurationError('Site class does not implement '
                                     'IPossibleClass: %s' % site_class)
    if site_class is not None:
        _context.action(
            discriminator = (class_,),
            callable = metaconfigure.classSiteHook,
            args=(class_, site_class)
            )
        _context.action(
            discriminator = (class_, IPossibleSite),
            callable = classImplements,
            args=(class_, IPossibleSite)
            )
    metaconfigure._localsite_monkies.append(class_)

metaconfigure.installSiteHook = installSiteHook

    
def initialize(context):

    # Zope3monkey
    from zope.app.form.browser.itemswidgets import ItemsWidgetBase
    ItemsWidgetBase.textForValue = textForValue
    # Five monkey
    EditView.update = EditViewUpdate
