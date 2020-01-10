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
    _restore_in_palce     overwrite common in place restore function
"""

from cvpysdk.exception import SDKException
from ..instance import Instance

class AzureAdInstance(Instance):
    """
    Class for Azure Ad instance
    """

    def _restore_in_place(self, **kwargs):
        """Restore azure ad objects
            Args:
                kwargs    dict    additional dict passed for restore,
                                    passed from subclient instance
            Return:
                request_json    json    restore json file
            Raise:
                102    restore option is not valid
        """

        request_json = self._restore_json(**kwargs)
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
