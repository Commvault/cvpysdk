# -*- coding: utf-8 -*-
# ————————————————————————–
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
# ————————————————————————–

"""File for operating on a Microsoft Office 365 Teams subclient

TeamsSubclient is the only class defined in this file.

TeamsSubclient: Derived class from Subclient Base class, representing a Microsoft Office 365 Teams subclient,
and to perform operations on that subclient

TeamsSubclient:
    discover()              --  Launches Discovery and returns the discovered teams.
    content()               --  Add teams, discover() must be called before teams added using this method.
    backup()                --  Backup a single or mulitple teams.
    out_of_place_restore()  --  Restore a single team or multiple teams.

"""

from __future__ import unicode_literals
from ...exception import SDKException
from ..casubclient import CloudAppsSubclient

import time
from copy import copy, deepcopy

from cvpysdk.job import Job
from ..cloudapps.teams_constants import TeamsConstants as const


class TeamsSubclient(CloudAppsSubclient):
    """Derived class from Subclient Base class, representing a Microsoft Office 365 Teams subclient
    and to perform operations on that subclient.
    """

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

        return self._instance_object.discover(refresh_cache=refresh_cache)

    def content(self, teams, o365_plan):
        """Add teams, discover() must be called before teams added using this method.
            Args:
                teams       (list)  --  List of team Email IDs.
                o365_plan   (str)   --  Name of the Office 365 plan.

            Raises:
                SDKException:
                    If content failed to be set.
                    If response is empty.
                    If response is not success.

        """

        discovered_teams = self._instance_object.discover()
        teams = [discovered_teams[team] for team in teams]

        url = self._services['SET_USER_POLICY_ASSOCIATION']

        for team in teams:

            subclient_entity_json = copy(const.ADD_SUBCLIENT_ENTITY_JSON)
            subclient_entity_json['instanceId'] = int(self._instance_object.instance_id)
            subclient_entity_json['subclientId'] = int(self._subclient_id)
            subclient_entity_json['clientId'] = int(self._client_object.client_id)
            subclient_entity_json['applicationId'] = int(self._subClientEntity['applicationId'])

            user_json = copy(const.ADD_USER_JSON)
            user_json['_type_'] = team['user']['_type_']
            user_json['userGUID'] = team['user']['userGUID']

            user_account_json = deepcopy(const.ADD_TEAM_JSON)
            user_account_json['displayName'] = team['displayName']
            user_account_json['smtpAddress'] = team['smtpAddress']
            user_account_json['msTeamsInfo']['teamsCreatedTime'] = team['msTeamsInfo']['teamsCreatedTime']
            user_account_json['user'] = user_json

            request_json = deepcopy(const.ADD_REQUEST_JSON)
            request_json['cloudAppAssociation']['subclientEntity'] = subclient_entity_json
            request_json['cloudAppAssociation']['cloudAppDiscoverinfo']['userAccounts'].append(user_account_json)

            request_json['cloudAppAssociation']['plan']['planId'] = int(self._commcell_object.plans.get(o365_plan).plan_id)
            flag, response = self._cvpysdk_object.make_request('POST', url, request_json)

            if not flag:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

    def backup(self, teams):
        """Run an Incremental backup.
            Args:
                teams               (list)  --  List of team Email IDs.

            Returns:
                obj   --  Instance of job.

            Raises:
                SDKException:

                    If backup failed to run.
                    If response is empty.
                    If response is not success.

        """

        discovered_teams = self._instance_object.discover()
        teams = [discovered_teams[team] for team in teams]

        url = self._services['CREATE_TASK']

        team_json_list = []

        for team in teams:

            team_json = copy(const.BACKUP_TEAM_JSON)
            team_json['displayName'] = team['displayName']
            team_json['smtpAddress'] = team['smtpAddress']
            team_json['msTeamsInfo']['teamsCreatedTime'] = team['msTeamsInfo']['teamsCreatedTime']
            team_json['user'] = {"userGUID": team['user']['userGUID']}
            team_json_list.append(team_json)

        associations = copy(const.ASSOCIATIONS)
        associations["subclientId"] = int(self._subClientEntity['subclientId'])
        associations["applicationId"] = int(self._subClientEntity['applicationId'])
        associations["clientName"] = self._subClientEntity['clientName']
        associations["displayName"] = self._subClientEntity['displayName']
        associations["backupsetId"] = self._subClientEntity['backupsetId']
        associations["instanceId"] = self._subClientEntity['instanceId']
        associations["subclientGUID"] = self.subclient_guid
        associations["clientId"] = int(self._client_object.client_id)
        associations["clientGUID"] = self._client_object.client_guid
        associations["subclientName"] = self.subclient_name
        associations["backupsetName"] = self._subClientEntity['backupsetName']
        associations["instanceName"] = self._subClientEntity['instanceName']
        associations["_type_"] = self._subClientEntity['_type_']

        backup_subtask_json = copy(const.BACKUP_SUBTASK_JSON)
        backup_subtask_json['options']['backupOpts']['cloudAppOptions']['userAccounts'] = team_json_list

        request_json = deepcopy(const.BACKUP_REQUEST_JSON)
        request_json['taskInfo']['associations'].append(associations)
        request_json['taskInfo']['subTasks'].append(backup_subtask_json)

        flag, response = self._cvpysdk_object.make_request('POST', url, request_json)

        if flag:

            if response.json():

                if 'jobIds' in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])

                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    raise SDKException('Subclient', '102', f"Backup failed, error message : {error_message}")

            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def out_of_place_restore(self, team, destination_team):
        """Restore a team to another location.
            Args:
                team                (str)   --  The email ID of the team that needs to be restored.
                destination_team    (str)   --  The email ID of the team to be restored to.

            Returns:
                obj   --  Instance of job.

            Raises:
                SDKException:

                    If restore failed to run.
                    If response is empty.
                    If response is not success.

        """

        self._instance_object._restore_association = self._subClientEntity
        return self._instance_object.restore_out_of_place(source_team=team, destination_team=destination_team)


