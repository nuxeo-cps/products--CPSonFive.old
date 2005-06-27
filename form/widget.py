# -*- coding: ISO-8859-15 -*-
# (C) Copyright 2005 Nuxeo SARL <http://nuxeo.com>
# Author: Lennart Regebro <regebro@nuxeo.com>
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
# $Id: calendar.py 24398 2005-06-24 12:34:57Z lregebro $

from zope.app.form.browser import TextWidget
from zope.app.form.browser.widget import renderElement
from zope.app.datetimeutils import DateTimeError
from zope.app.form.interfaces import ConversionError, WidgetInputError
from zope.app.form.interfaces import InputErrors
from zope.schema.interfaces import ValidationError
from Products.CMFCore.utils import getToolByName

from zope.i18nmessageid import MessageIDFactory
_ = MessageIDFactory("calendar")

class DocumentBrowserWidget(TextWidget):

    displayWidth = 30

    def _toFieldValue(self, input):
        try:
            if not input:
                return input
            input = str(input)
            context = self.context.context
            portal_url = getToolByName(context, 'portal_url')
            portal_path = portal_url.getPortalPath()
            if not input.startswith(portal_path):
                if input[0] != '/':
                    input = '/' + input
                input = portal_path + input
            
            obj = context.unrestrictedTraverse(input)
            return u'/'.join(obj.getPhysicalPath())
        except (AttributeError, KeyError), v:
            raise ConversionError("Selected object not found", v)

    def __call__(self):
        value = self._getFormValue()
        res = renderElement(self.tag,
                            type=self.type,
                            name=self.name,
                            id=self.name,
                            value=value,
                            cssClass=self.cssClass,
                            style=self.style,
                            size=self.displayWidth,
                            extra=self.extra)
        style = "text-decoration:none;border:1px solid black;padding:0.2em 0.3em;"
        js = "window.open('documentnavigation_popup?input_id=" + \
                          self.name + "', 'DirectoryMultiEntryFinder', " \
                          "'toolbar=0, scrollbars=1, location=0, " \
                          "statusbar=0, menubar=0, resizable=1, dependent=1, " \
                          "width=500, height=480')"
        btn = renderElement("input", type="button", style=style, onClick=js, 
                            value=_("..."))
        return res + "&nbsp;" + btn
        