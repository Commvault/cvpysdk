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

"""File for operating on a Teams Instance.
TeamsInstance is the only class defined in this file.

TeamsInstance: Derived class from CloudAppsInstance Base class, representing Office 365 Teams.

TeamsInstance:
    _get_instance_properties()      --  Gets the properties of this machine.
    _get_instance_properties_json() --  Returns the instance properties json.
    discover()                      --  Launches Discovery and returns the discovered teams.
    _restore_json()                 --  Returns JSON request to pass to API as per the options selected by the user.
    _cloud_apps_restore_json()      --  Returns JSON for Cloud Apps related properties.
    restore_out_of_place()          --  Restore a team to another location.

"""

from __future__ import unicode_literals

from ...exception import SDKException
from ..cainstance import CloudAppsInstance
from cvpysdk.job import Job

import time

class TeamsInstance(CloudAppsInstance):
    """Class for representing an Instance of Office 365 Teams."""

    def _get_instance_properties(self):
        """Gets the properties of this instance.
            Args:
                None

            Returns:
                None

            Raises:
                SDKException:
                    if response is empty.
                    if response is not success.
                    if access node is not configured.

        """
        super(TeamsInstance, self)._get_instance_properties()

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance['instanceType']

            if 'generalCloudProperties' in cloud_apps_instance:
                if 'proxyServers' in cloud_apps_instance['generalCloudProperties']:
                    self._proxy_client = cloud_apps_instance.get(
                        'generalCloudProperties', {}).get('proxyServers', [{}])[0].get('clientName')
                else:
                    if 'clientName' in cloud_apps_instance.get(
                            'generalCloudProperties', {}).get('memberServers', [{}])[0].get('client'):
                        self._proxy_client = cloud_apps_instance.get('generalCloudProperties', {}).get(
                            'memberServers', [{}])[0].get('client', {}).get('clientName')
                    else:
                        self._proxy_client = cloud_apps_instance.get('generalCloudProperties', {}).get(
                            'memberServers', [{}])[0].get('client', {}).get('clientGroupName')

                if self._proxy_client is None:
                    raise SDKException('Instance', '102', 'Access Node has not been configured')

    def _get_instance_properties_json(self):
        """Returns the instance properties json.
            Returns:
                dict    --  Dictionary of the instance properties.

        """

        return {'instanceProperties': self._properties}

    def discover(self, refresh_cache=True):
        """Launches Discovery and returns the discovered teams.
            Args:
                refresh_cache   --  Refreshes Discover cache information.
                    default:    True

            Returns:
                dict    --  Returns dictionary with team email ID as key and team properties as value.

            Raises:
                SDKException:
                    If discovery failed to launch.
                    If response is empty.
                    If response is not success.

        """

        DISCOVERY_TYPE = 8
        max_retries = 5
        url = f"{self._services['GET_CLOUDAPPS_USERS'] % (self.instance_id, self._agent_object._client_object.client_id, DISCOVERY_TYPE)}&pageSize=0"

        for retry in range(max_retries):

            flag, response = self._cvpysdk_object.make_request('GET', f"{url}&refreshCache=1" if refresh_cache else url)

            # NEED TO REFRESH CACHE ONLY THE FIRST TIME
            refresh_cache = False

            if flag:

                if response.json():
                    resp = response.json()
                    if 'userAccounts' in resp:
                        self.discovered_users = {team['smtpAddress']: team for team in resp['userAccounts']}
                        return self.discovered_users

                    # IF OUR RESPONSE IS EMPTY OR WE HAVE REACHED MAXIMUM NUMBER OF ATTEMPTS WITHOUT DESIRED RESPONSE
                    elif not resp or retry == max_retries-1:
                        raise SDKException('Response', '102')

                    time.sleep(30)
                    continue  # TO AVOID RAISING EXCEPTION

                raise SDKException('Response', '102')

            if response.json():
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

            raise SDKException('Response', '102')

    def _restore_json(self):
        """Returns JSON request to pass to API as per the options selected by the user.

            Returns:
                dict - JSON request to pass to the API.
        """

        request_json = super(TeamsInstance, self)._restore_json(restore_option=self._restore_association)
        request_json['taskInfo']['associations'][0]["clientGUID"] = self._agent_object._client_object.client_guid
        return request_json

    def _cloud_apps_restore_json(self, source_team, destination_team):
        """Returns JSON for Cloud Apps related properties.

            Args:
                source_team         (dict)   --  Dictionary of properties from discover() for team that is to be restored.
                destination_team    (dict)   --  Dictionary of properties from discover() of team to be restored to.

            Returns:
                dict - JSON request to pass to the API
        """

        ca_json = {
            "instanceType":  int(self._properties['cloudAppsInstance']['instanceType']),
            "msTeamsRestoreOptions": {
                "restoreAllMatching": False,
                "sourceTeamItemType": 1,
                "overWriteItems": False,
                "restoreToTeams": True,
                "destLocation": destination_team['displayName'],
                "restoreUsingFindQuery": False,
                "findQuery": {
                    "mode": 4,
                    "facetRequests": {},
                    "advSearchGrp": {
                        "commonFilter": [
                            {
                                "filter": {
                                    "interFilterOP": 2,
                                    "filters": [
                                        {
                                            "groupType": 0,
                                            "field": "CISTATE",
                                            "intraFieldOp": 0,
                                            "fieldValues": {
                                                "values": ["1"]
                                            }
                                        }
                                    ]
                                }
                            }
                        ],
                        "fileFilter": [
                            {
                                "filter": {
                                    "interFilterOP": 2,
                                    "filters": [
                                        {
                                            "field": "CV_OBJECT_GUID",
                                            "intraFieldOp": 0,
                                            "fieldValues": {
                                                "values": [source_team['user']['userGUID'].lower()]
                                            }
                                        }
                                    ]
                                }
                            }
                        ],
                        "galaxyFilter": [
                            {
                                "appIdList": [int(self._restore_association['subclientId'])]
                            }
                        ]
                    },
                    "searchProcessingInfo": {
                        "resultOffset": 0,
                        "pageSize": 1,
                        "queryParams": [
                            {
                                "param": "ENABLE_MIXEDVIEW", "value": "true"
                            },
                            {
                                "param": "RESPONSE_FIELD_LIST",
                                "value": "DATA_TYPE,CONTENTID,CV_OBJECT_GUID,PARENT_GUID,CV_TURBO_GUID,AFILEID,"
                                         "AFILEOFFSET,COMMCELLNO,MODIFIEDTIME,SIZEINKB,BACKUPTIME,CISTATE,DATE_DELETED,"
                                         "TEAMS_ITEM_ID,TEAMS_ITEM_NAME,TEAMS_NAME,TEAMS_SMTP,TEAMS_ITEM_TYPE,"
                                         "TEAMS_CHANNEL_TYPE,TEAMS_TAB_TYPE,TEAMS_GROUP_VISIBILITY,TEAMS_GUID,"
                                         "TEAMS_CONV_ITEM_TYPE,TEAMS_CONV_MESSAGE_TYPE,TEAMS_CONV_SUBJECT,"
                                         "TEAMS_CONV_IMPORTANCE,TEAMS_CONV_SENDER_TYPE,TEAMS_CONV_SENDER_NAME,"
                                         "TEAMS_CONV_HAS_REPLIES,CI_URL"}
                        ],
                        "sortParams": [
                            {
                                "sortDirection": 0,
                                "sortField": "SIZEINKB"
                            }
                        ]
                    }
                },
                "selectedItemsToRestsore": [
                    {
                        "itemId": source_team['user']['userGUID'].lower(),
                        "path": "", "itemType": 1,
                        "isDirectory": True
                    }
                ],
                "destinationTeamInfo": {
                    "tabId": "",
                    "teamName": destination_team['displayName'],
                    "tabName": "",
                    "folder": "",
                    "teamId": destination_team['user']['userGUID'].lower(),
                    "destination": 1,
                    "channelName": "",
                    "channelId": ""
                }
            }
        }

        return ca_json

    def restore_out_of_place(self, source_team, destination_team):
        """Restore a team to another location.

            Args:
                source_team         (str)   --  The email ID of the team that needs to be restored.
                destination_team    (str)   --  The email ID of the team to be restored to.

            Returns:
                obj   --  Instance of Restore job.

            Raises:
                SDKException:
                    If restore failed to run.
                    If response is empty.
                    If response is not success.

        """

        discovered_teams = self.discover()
        source_team = discovered_teams[source_team]
        destination_team = discovered_teams[destination_team]

        request_json = self._restore_json()
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination']['inPlace'] = False
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['cloudAppsRestoreOptions'] = self._cloud_apps_restore_json(source_team=source_team, destination_team=destination_team)

        url = self._services['CREATE_TASK']

        flag, response = self._cvpysdk_object.make_request('POST', url, request_json)

        if flag:

            if response.json():

                if 'jobIds' in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])

                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    raise SDKException('Subclient', '102', f"Restore failed, error message : {error_message}")

                raise SDKException('Response', '102')

            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
