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

"""File for operating on a Azure AD Instance.

AzureAdInstance is the only class defined in this file.

AzureAdInstance:     Derived class from Instance  Base class, representing a
                    Azure Ad Instance, and to perform operations on that instance

AzureAdInstance:
    _restore_in_place     overwrite common in place restore function
"""

from ..exception import SDKException
from ..instance import Instance

from typing import Union, TYPE_CHECKING
if TYPE_CHECKING:
    from ..job import Job
    from ..schedules import Schedules


class AzureAdInstance(Instance):
    """
    Represents an Azure Active Directory (AD) instance.

    This class provides functionality specific to managing Azure AD instances,
    including operations such as restoring data in place. It extends the base
    Instance class to support Azure AD-specific workflows and recovery actions.

    Key Features:
        - In-place restoration of Azure AD instance data
        - Integration with base instance management functionality

    #ai-gen-doc
    """

    def _restore_in_place(self, **kwargs) -> Union['Job', 'Schedules']:
        """Restore Azure AD objects in place using the provided restore options.

        This method initiates an in-place restore operation for Azure Active Directory objects.
        Additional restore options can be specified as keyword arguments, typically passed from a subclient instance.

        Args:
            **kwargs: Additional restore options as key-value pairs. These options customize the restore behavior.

        Returns:
            Job or Schedules: The Job or Schedules object

        Raises:
            Exception: If a restore option is not valid (error code 102).

        #ai-gen-doc
        """

        request_json = self._restore_json(**kwargs)
        if "to_time" in kwargs:
            request_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["browseOption"]["timeRange"]["toTime"] = \
                kwargs['to_time']

            del request_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["browseOption"]["timeRange"]["toTimeValue"]

        if "overwrite" in kwargs['fs_options']:
            request_json["taskInfo"]["subTasks"][0]\
            ["options"]["restoreOptions"]['commonOptions']['unconditionalOverwrite'] = \
            kwargs['fs_options']['overwrite']

        if "azureADOption" in kwargs['restore_option']:
            request_json["taskInfo"]["subTasks"][0]\
            ["options"]["restoreOptions"]['azureADOption'] = \
            kwargs['restore_option']['azureADOption']
        else:
            raise SDKException('Instance', "102", "AzureAD option is not valid")

        return self._process_restore_response(request_json)
