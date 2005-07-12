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

from zope.schema.interfaces import ITitledTokenizedTerm

# Zope3.0.0 doesn't translates dropdownboxes (that's a bug)
def textForValue(self, term):
    """Extract a string from the term.

    The term must be a vocabulary tokenized term.

    This can be overridden to support more complex term objects. The token
    is returned here since it's the only thing known to be a string, or
    str()able."""
    # XXX: This is how it should be once we start using Five 1.1, with i18n.
    # if ITitledTokenizedTerm.providedBy(term):
    #     return self.translate(term.title)
    # return self.translate(term.token)

    # XXX: But with Five 1.0.x we need to call Localizer:
    if ITitledTokenizedTerm.providedBy(term):
        return self.context.context.Localizer.default(term.title)
    return self.context.context.Localizer.default(term.token)


def initialize(context):

    # Zope3monkey
    from zope.app.form.browser.itemswidgets import ItemsWidgetBase
    ItemsWidgetBase.textForValue = textForValue
    
    ## Five monkey
    # Hm? Why? Probably this fix has been pushed into Five by now, because 
    # this edit.pt is exactly the same as Fives...
    #from Products.Five.browser import EditView
    #from Products.Five.pagetemplatefile import FivePageTemplateFile
    #EditView.generated_form = FivePageTemplateFile('edit.pt')
    
