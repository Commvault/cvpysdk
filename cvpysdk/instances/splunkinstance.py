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

"""
File for operating on Splunk Instance

SplunkInstance is the only class defined in this file.

SplunkInstance: Derived class from BigDataAppsInstance, representing a
splunk instance, and to perform operations on that instance

SplunkInstance
==============

    _restore_json() --  Method which creates json for a restore job
"""

from .bigdataappsinstance import BigDataAppsInstance


class SplunkInstance(BigDataAppsInstance):
    """
    Represents a Splunk instance and provides operations for managing and interacting with it.

    This class is designed to encapsulate the functionality required to operate on a Splunk instance,
    including internal methods for restoring configuration or state from JSON data.

    Key Features:
        - Encapsulation of Splunk instance operations
        - Internal support for restoring instance state from JSON

    #ai-gen-doc
    """

    def _restore_json(self, **kwargs) -> dict:
        """Create the JSON dictionary required for initiating a restore job.

        This method constructs the parameter dictionary needed to start a restore job.
        If performing a restore out of place, a `destination_entity` dictionary should be provided
        in the keyword arguments, containing information about the destination client and instance.

        Keyword Args:
            destination_entity (dict, optional): Dictionary specifying the destination for an out-of-place restore.
                Example format:
                    {
                        "clientId": <int>,
                        "clientName": <str>,
                        "instanceName": <str>,
                        "appName": <str>,
                        "instanceId": <int>,
                        "applicationId": <int>,
                    }
            Additional keyword arguments may be provided as needed for restore customization.

        Returns:
            dict: Dictionary containing all parameters required to initiate a restore job.

        Example:
            >>> restore_params = splunk_instance._restore_json(
            ...     destination_entity={
            ...         "clientId": 123,
            ...         "clientName": "DestinationClient",
            ...         "instanceName": "SplunkInstance2",
            ...         "appName": "Splunk",
            ...         "instanceId": 456,
            ...         "applicationId": 789,
            ...     },
            ...     some_other_option=True
            ... )
            >>> print(restore_params)
            # The returned dictionary can be used to submit a restore job

        #ai-gen-doc
        """

        instance_properties = self.properties
        client_id = instance_properties["instance"]["clientId"]
        application_id = instance_properties["instance"]["applicationId"]

        rest_json = super(SplunkInstance, self)._restore_json(**kwargs)

        rest_json["taskInfo"]["subTasks"][0]["options"] \
            ["restoreOptions"]["browseOption"]["backupset"]["clientId"] = int(client_id)

        rest_json["taskInfo"]["subTasks"][0]["options"] \
            ["restoreOptions"]["commonOptions"]["unconditionalOverwrite"] = True

        rest_json["taskInfo"]["subTasks"][0]["options"] \
            ["restoreOptions"]["commonOptions"]["skip"] = False

        rest_json["taskInfo"]["subTasks"][0]["options"] \
            ["restoreOptions"]["destination"] \
            ["destClient"]["clientId"] = int(kwargs.get('destination_entity', {}). \
                                             get('clientId', self._instance['clientId']))

        rest_json["taskInfo"]["subTasks"][0]["options"] \
            ["restoreOptions"]["destination"]["destinationInstance"] = kwargs. \
            get('destination_entity', self._instance)

        rest_json["taskInfo"]["subTasks"][0]["options"] \
            ["restoreOptions"]["distributedAppsRestoreOptions"] = {"distributedRestore": True}

        if kwargs.get('destination_entity') is not None:
            rest_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["distributedAppsRestoreOptions"] \
                ["splunkRestoreOptions"] = {"outofPlaceRestore": True}

        else:
            rest_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["distributedAppsRestoreOptions"] \
                ["splunkRestoreOptions"] = {"outofPlaceRestore": False}

        rest_json["taskInfo"]["subTasks"][0]["options"] \
            ["restoreOptions"]["qrOption"] = {
                "destAppTypeId": int(application_id)
            }

        rest_json["taskInfo"]["subTasks"][0]["options"]["commonOpts"] = {
            "notifyUserOnJobCompletion": False,
            "subscriptionInfo": "<Api_Subscription subscriptionId =\"521\"/>"
        }

        return rest_json
