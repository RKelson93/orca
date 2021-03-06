# Orca
#
# Copyright 2018 Igalia, S.L.
#
# Author: Joanmarie Diggs <jdiggs@igalia.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

"""Custom script utilities for Chromium"""

# Please note: ATK support in Chromium needs much work. Until that work has been
# done, Orca will not be able to provide access to Chromium. These utilities are
# a work in progress.

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2018 Igalia, S.L."
__license__   = "LGPL"

import pyatspi
import time

from orca import debug
from orca import orca_state
from orca.scripts import web


class Utilities(web.Utilities):

    def __init__(self, script):
        super().__init__(script)

    def clearCachedObjects(self):
        super().clearCachedObjects()

    def selectedChildCount(self, obj):
        count = super().selectedChildCount(obj)
        if count or "Selection" in pyatspi.listInterfaces(obj):
            return count

        # HACK: Ideally, we'd use the selection interface to get the selected
        # child count. But that interface is not implemented yet. This hackaround
        # is extremely non-performant.
        for child in obj:
            if child.getState().contains(pyatspi.STATE_SELECTED):
                count += 1

        msg = "CHROMIUM: NO SELECTION INTERFACE HACK: Selected children: %i" % count
        debug.println(debug.LEVEL_INFO, msg, True)
        return count

    def selectedChildren(self, obj):
        result = super().selectedChildren(obj)
        if result or "Selection" in pyatspi.listInterfaces(obj):
            return result

        # HACK: Ideally, we'd use the selection interface to get the selected
        # children. But that interface is not implemented yet. This hackaround
        # is extremely non-performant.
        for child in obj:
            if child.getState().contains(pyatspi.STATE_SELECTED):
                result.append(child)

        return result

    def isMenuWithNoSelectedChild(self, obj):
        if not obj:
            return False

        try:
            role = obj.getRole()
        except:
            msg = "CHROMIUM: Exception getting role for %s" % obj
            debug.println(debug.LEVEL_INFO, msg, True)
            return False

        if role != pyatspi.ROLE_MENU:
            return False

        return not self.selectedChildCount(obj)

    def treatAsMenu(self, obj):
        if not obj:
            return False

        try:
            role = obj.getRole()
            state = obj.getState()
        except:
            msg = "CHROMIUM: Exception getting role and state for %s" % obj
            debug.println(debug.LEVEL_INFO, msg, True)
            return False

        # Unlike other apps and toolkits, submenus in Chromium have the menu item
        # role rather than the menu role, but we can identify them as submenus via
        # the has-popup state.
        if role == pyatspi.ROLE_MENU_ITEM:
            return state.contains(pyatspi.STATE_HAS_POPUP)

        return False

    def isPopupMenuForCurrentItem(self, obj):
        # When a submenu is closed, it has role menu item. But when that submenu
        # is opened/expanded, a menu with that same name appears. It would be
        # nice if there were a connection (parent/child or an accessible relation)
        # between the two....
        if not self.treatAsMenu(orca_state.locusOfFocus):
            return False

        if obj.name and obj.name == orca_state.locusOfFocus.name:
            return obj.getRole() == pyatspi.ROLE_MENU

        return False

    def isFrameForPopupMenu(self, obj):
        try:
            name = obj.name
            role = obj.getRole()
            childCount = obj.childCount
        except:
            msg = "CHROMIUM: Exception getting properties of %s" % obj
            debug.println(debug.LEVEL_INFO, msg, True)
            return False

        # The ancestry of a popup menu appears to be a menu bar (even though
        # one is not actually showing) contained in a nameless frame. It would
        # be nice if these things were pruned from the accessibility tree....
        if name or role != pyatspi.ROLE_FRAME or childCount != 1:
            return False

        if obj[0].getRole() == pyatspi.ROLE_MENU_BAR:
            return True

        return False

    def popupMenuForFrame(self, obj):
        if not self.isFrameForPopupMenu(obj):
            return None

        try:
            menu = pyatspi.findDescendant(obj, lambda x: x and x.getRole() == pyatspi.ROLE_MENU)
        except:
            msg = "CHROMIUM: Exception finding descendant of %s" % obj
            debug.println(debug.LEVEL_INFO, msg, True)
            return None

        msg = "CHROMIUM: HACK: Popup menu for %s: %s" % (obj, menu)
        debug.println(debug.LEVEL_INFO, msg, True)
        return menu

    def grabFocusWhenSettingCaret(self, obj):
        # HACK: Remove this when setting the caret updates focus.
        msg = "CHROMIUM: HACK: Doing focus grab when setting caret on %s" % obj
        debug.println(debug.LEVEL_INFO, msg, True)
        return True
