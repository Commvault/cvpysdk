# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
    """
    Class for performing system-related operations within the Commcell environment.

    This class provides an interface to manage and configure system-level settings
    for a Commcell instance. It is initialized with a Commcell object and offers
    methods to adjust system parameters such as GUI timeout values.

    Key Features:
        - Initialization with a Commcell object for context-specific operations
        - Ability to set the GUI timeout value for system interactions

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize the System class with a Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> system = System(commcell)
            >>> print("System object initialized successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object

    def set_gui_timeout(self, value: int) -> None:
        """Set the GUI timeout value in minutes.

        Setting the timeout value determines how long a GUI session remains active before timing out due to inactivity.
        If the value is set to 0, GUI connections will not time out.

        Args:
            value: The GUI timeout value in minutes. Use 0 to disable GUI session timeouts.

        Example:
            >>> system = System()
            >>> system.set_gui_timeout(30)  # Set GUI timeout to 30 minutes
            >>> system.set_gui_timeout(0)   # Disable GUI timeout

        #ai-gen-doc
        """
        self._commcell_object._set_gxglobalparam_value(
            {
                "name": "Gui timeout",
                "value": str(value)
            }
        )
