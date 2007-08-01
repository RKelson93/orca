#!/usr/bin/python

"""Test of menu, menu navigation, and menu item output using the
   gtk-demo Application Main Window demo.
"""

from macaroon.playback.keypress_mimic import *

sequence = MacroSequence()

########################################################################
# We wait for the demo to come up and for focus to be on the tree table
#
sequence.append(WaitForWindowActivate("GTK+ Code Demos"))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_TREE_TABLE))

########################################################################
# Once gtk-demo is running, invoke the Application Main Window demo
#
sequence.append(KeyComboAction("<Control>f"))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_TEXT))
sequence.append(TypeAction("Application main window", 1000))
sequence.append(KeyComboAction("Return", 500))

########################################################################
# When the demo comes up, go to the Bold check menu item in the
# Preferences menu.
#
#sequence.append(WaitForWindowActivate("Application Window",None))
sequence.append(WaitForFocus("Open", acc_role=pyatspi.ROLE_PUSH_BUTTON))
sequence.append(KeyComboAction("F10"))

sequence.append(WaitForFocus("File",
                             acc_role=pyatspi.ROLE_MENU))
sequence.append(KeyComboAction("Down"))

sequence.append(WaitForFocus("New",
                             acc_role=pyatspi.ROLE_MENU_ITEM))
sequence.append(KeyComboAction("Down"))

sequence.append(WaitForFocus("Open",
                             acc_role=pyatspi.ROLE_MENU_ITEM))
sequence.append(KeyComboAction("Right"))

sequence.append(WaitForFocus("Color",
                             acc_role=pyatspi.ROLE_MENU))
sequence.append(KeyComboAction("Right"))

sequence.append(WaitForFocus("Red",
                             acc_role=pyatspi.ROLE_CHECK_MENU_ITEM))
sequence.append(KeyComboAction("Down"))

sequence.append(WaitForFocus("Green",
                             acc_role=pyatspi.ROLE_CHECK_MENU_ITEM))
sequence.append(KeyComboAction("Down"))

sequence.append(WaitForFocus("Blue",
                             acc_role=pyatspi.ROLE_CHECK_MENU_ITEM))
sequence.append(KeyComboAction("Left"))

sequence.append(WaitForFocus("Color",
                             acc_role=pyatspi.ROLE_MENU))
sequence.append(KeyComboAction("Down"))

sequence.append(WaitForFocus("Shape",
                             acc_role=pyatspi.ROLE_MENU))
sequence.append(KeyComboAction("Right"))

sequence.append(WaitForFocus("Square",
                             acc_role=pyatspi.ROLE_CHECK_MENU_ITEM))
sequence.append(KeyComboAction("Down"))

sequence.append(WaitForFocus("Rectangle",
                             acc_role=pyatspi.ROLE_CHECK_MENU_ITEM))
sequence.append(KeyComboAction("Down"))

sequence.append(WaitForFocus("Oval",
                             acc_role=pyatspi.ROLE_CHECK_MENU_ITEM))
sequence.append(KeyComboAction("Left"))

sequence.append(WaitForFocus("Shape",
                             [1, 0, 3, 1, 2],
                             acc_role=pyatspi.ROLE_MENU))
sequence.append(KeyComboAction("Down"))

sequence.append(WaitForFocus("Bold",
                             acc_role=pyatspi.ROLE_CHECK_MENU_ITEM))
sequence.append(KeyComboAction("Right"))

sequence.append(WaitForFocus("About",
                             acc_role=pyatspi.ROLE_MENU_ITEM))

########################################################################
# Dismiss the menu and close the Application Window demo window
#
sequence.append(KeyComboAction("F10"))
sequence.append(WaitForFocus("Open", acc_role=pyatspi.ROLE_PUSH_BUTTON))
sequence.append(KeyComboAction("<Alt>F4", 500))

########################################################################
# Go back to the main gtk-demo window and reselect the
# "Application main window" menu.  Let the harness kill the app.
#
#sequence.append(WaitForWindowActivate("GTK+ Code Demos",None))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_TREE_TABLE))

# Just a little extra wait to let some events get through.
#
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_INVALID, timeout=3000))

sequence.start()
