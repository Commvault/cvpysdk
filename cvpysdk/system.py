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
