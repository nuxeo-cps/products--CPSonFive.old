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
# $Id: interfaces.py 23798 2005-06-10 16:16:35Z lregebro $

from zope.interface import Interface

class IDocumentNavigation(Interface):
    """Support for popup document navigation windows"""
    
    def getDocumentNavigation(finder, root_uid, current_uid=None, REQUEST=None):
        """Returns a CPSNavigation object

        The navigation popup uses a CPSNavigation object to display a 
        navigation tree."""
        
