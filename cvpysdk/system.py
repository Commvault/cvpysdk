# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing system related operations on Commcell.

System is the only class defined in this file

System: Class for performing system related operations on the commcell

System:
=======

    __init__(commcell_object)       --  initialise object of System class

    set_gui_timeout()               --  To set GUI timeout value in minutes

"""


class System:
    """Class for performing system related operations in the commcell"""

    def __init__(self, commcell_object):
        """Initialize the System class

            Args:
                commcell_object    (object)    --  instance of the Commcell class

        """
        self._commcell_object = commcell_object

    def set_gui_timeout(self, value):
        """Sets GUI timeout value in minutes

        Args:
            value   (str)   -- GUI timeout value in minutes

        **Note** setting value to 0 will disable GUI connections to timeout

        """
        self._commcell_object._set_gxglobalparam_value(
            {
                "name": "Gui timeout",
                "value": str(value)
            }
        )
