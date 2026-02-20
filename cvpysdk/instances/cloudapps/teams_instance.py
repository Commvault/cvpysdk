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
    update_instance()               --  Update Instance properties.

"""

from __future__ import unicode_literals
import time

from ...exception import SDKException
from ..cainstance import CloudAppsInstance
from ...job import Job

class TeamsInstance(CloudAppsInstance):
    """
    Represents an instance of Office 365 Teams within a cloud application environment.

    This class provides comprehensive management and operational capabilities for Office 365 Teams instances,
    including property retrieval, discovery, restoration, and instance updates. It is designed to facilitate
    backup, recovery, and configuration tasks for Teams environments in cloud-based infrastructures.

    Key Features:
        - Retrieve instance properties and their JSON representations
        - Discover Teams instances with support for cache refresh
        - Generate restore JSON data for Teams instances
        - Perform out-of-place restoration from a source team to a destination team
        - Update Teams instance configuration using JSON requests

    #ai-gen-doc
    """

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this TeamsInstance.

        This method fetches the current configuration and properties for the TeamsInstance
        from the Commcell server. It updates the instance's internal state with the latest
        information. If the response from the server is empty, unsuccessful, or if the access
        node is not configured, an SDKException is raised.

        Raises:
            SDKException: If the response is empty, not successful, or if the access node is not configured.

        Example:
            >>> teams_instance = TeamsInstance(commcell_object, instance_name)
            >>> teams_instance._get_instance_properties()
            >>> # The instance properties are now refreshed and available for use

        #ai-gen-doc
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

    def _get_instance_properties_json(self) -> dict:
        """Retrieve the instance properties as a JSON dictionary.

        Returns:
            dict: A dictionary containing the properties of the Teams instance.

        Example:
            >>> teams_instance = TeamsInstance()
            >>> properties = teams_instance._get_instance_properties_json()
            >>> print(properties)
            >>> # Output will be a dictionary with instance property details

        #ai-gen-doc
        """

        return {'instanceProperties': self._properties}

    def discover(self, discovery_type: int, refresh_cache: bool = True) -> dict:
        """Launch a discovery operation and return the discovered Microsoft Teams.

        Args:
            discovery_type: The type of discovery to perform. For example, use 12 for Teams, or specify other values for users.
            refresh_cache: Whether to refresh the discovery cache before running the operation. Defaults to True.

        Returns:
            dict: A dictionary where each key is a team email ID and each value is a dictionary of team properties.

        Example:
            >>> teams_instance = TeamsInstance()
            >>> discovered_teams = teams_instance.discover(discovery_type=12)
            >>> for team_email, team_props in discovered_teams.items():
            ...     print(f"Team: {team_email}, Properties: {team_props}")

        Raises:
            SDKException: If the discovery fails to launch, the response is empty, or the response is not successful.

        #ai-gen-doc
        """

        DISCOVERY_TYPE = discovery_type
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
                    elif 'groups' in resp:
                        self.discovered_users = {team['name']: team for team in resp['groups']}
                        return self.discovered_users
                    elif not resp:
                        if retry == max_retries - 1:
                            raise SDKException('Response', '102', 'Please check Azure app details associated with client. Discovery has returned invalid response')
                        time.sleep(30)
                        continue

                    if retry == max_retries-1:
                        raise SDKException('Response', '102', 'Please check Azure app details associated with client. Discovery has returned invalid response')

                    time.sleep(30)
                    continue  # TO AVOID RAISING EXCEPTION

                raise SDKException('Response', '102', 'Please check Azure app details associated with client. Discovery has returned invalid response')

            if response.json():
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

            raise SDKException('Response', '102')

    def _restore_json(self) -> dict:
        """Generate the JSON request payload for the Teams restore API based on user-selected options.

        Returns:
            dict: The JSON request dictionary to be sent to the API for restoring Teams data.

        Example:
            >>> teams_instance = TeamsInstance()
            >>> restore_payload = teams_instance._restore_json()
            >>> print(restore_payload)
            >>> # Use the returned dictionary as the payload for the restore API call

        #ai-gen-doc
        """

        request_json = super(TeamsInstance, self)._restore_json(restore_option=self._restore_association)
        request_json['taskInfo']['associations'][0]["clientGUID"] = self._agent_object._client_object.client_guid
        return request_json

    def _cloud_apps_restore_json(self, source_team: dict, destination_team: dict) -> dict:
        """Generate the JSON payload for restoring Microsoft Teams data using Cloud Apps.

        This method constructs a JSON request containing the necessary properties for restoring
        a Teams instance from a source team to a destination team. The input dictionaries should
        be obtained from the `discover()` method and contain all required team metadata.

        Args:
            source_team: Dictionary of properties for the team to be restored, as returned by `discover()`.
            destination_team: Dictionary of properties for the destination team, as returned by `discover()`.

        Returns:
            dict: JSON request payload to be sent to the API for initiating the restore operation.

        Example:
            >>> source = teams_instance.discover('TeamA')
            >>> destination = teams_instance.discover('TeamB')
            >>> restore_json = teams_instance._cloud_apps_restore_json(source, destination)
            >>> print(restore_json)
            >>> # Use the generated JSON to initiate a restore via the API

        #ai-gen-doc
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

    def restore_out_of_place(self, source_team: str, destination_team: str) -> 'Job':
        """Restore a Microsoft Teams team to a different team (out-of-place restore).

        Args:
            source_team: The email ID of the source team to be restored.
            destination_team: The email ID of the destination team where the source team will be restored.

        Returns:
            Job: An instance representing the restore job that was initiated.

        Raises:
            SDKException: If the restore operation fails to run, if the response is empty, or if the response indicates failure.

        Example:
            >>> teams_instance = TeamsInstance()
            >>> restore_job = teams_instance.restore_out_of_place(
            ...     source_team="source_team@domain.com",
            ...     destination_team="destination_team@domain.com"
            ... )
            >>> print(f"Restore job started: {restore_job}")

        #ai-gen-doc
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

    def update_instance(self, request_json: dict) -> dict:
        """Update the properties of the Teams instance.

        Args:
            request_json: A dictionary containing the instance properties to update.

        Returns:
            dict: The response from the update request, typically containing status and details of the operation.

        Raises:
            SDKException: If the update fails, the response is empty, or the response indicates failure.

        Example:
            >>> update_data = {
            ...     "instanceProperties": {
            ...         "description": "Updated Teams instance",
            ...         "isActive": True
            ...     }
            ... }
            >>> response = teams_instance.update_instance(update_data)
            >>> print(response)
            {'status': 'success', 'details': {...}}

        #ai-gen-doc
        """

        url = self._services['INSTANCE_PROPERTIES'] % (self.instance_id)
        flag, response = self._cvpysdk_object.make_request('POST', url, request_json)
        if response.json():

            if 'processinginstructioninfo' in response.json():
                return response.json()

            elif "errorCode" in response.json():
                error_message = response.json()['errorMessage']
                raise SDKException('Subclient', '102', f"Update failed, error message : {error_message}")

            raise SDKException('Response', '102')

        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)