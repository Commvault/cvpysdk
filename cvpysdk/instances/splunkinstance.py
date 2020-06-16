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
from cvpysdk.instances.bigdataappsinstance import BigDataAppsInstance

class SplunkInstance(BigDataAppsInstance):
    """
    Class  representing a splunk instance, and to perform operations on
    that instance
    """

    def _restore_json(self, **kwargs):
        """
        Creates json required for restore job

        Args:
            kwargs              (dict)  --  dictionary containing optional key word arguments,
            if it is a restore out of place destination_entity dictionary is expected which
            has information about the destination.

            destination_entity  (dict)  --  {
                                                "clientId": ,
                                                "clientName": ,
                                                "instanceName": ,
                                                "appName": ,
                                                "instanceId": ,
                                                "applicationId": ,
                                            }

        Returns:
            parameter_dict  (dict)  --  dictionary with parameters set required for a
            retore job
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
