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
    _json_subclient_entity()    --  Get subclientEntity json for teams association operation
    discover()                  --  Launches Discovery and returns the discovered teams.
    content()                   --  Add teams, discover() must be called before teams added using this method.
    backup()                    --  Backup a single or mulitple teams.
    out_of_place_restore()      --  Restore a single team or multiple teams.
    _json_association()         --  Get association json for teams restore operation
    _json_restoreoptions_searchprocessinginfo() -- Get searchprocessingginfo json for teams restore operation
    _json_restoreoptions_advsearchgrp()         -- Get advSearchGrp json for teams restore operation
    _json_restoreoptions_findquery()            -- Get findquery json for teams restore operation
    _json_restoreoptions_destination()          -- Get destination json for teams restore operation
    _json_restoreoptions_msteamsrestoreoptions()-- Get msTeamsRestoreOptions json for teams restore operation
    _json_restoreoptions_cloudappsrestore()     -- Get cloudAppsRestoreOptions json for teams restore operation
    _json_restoreoptions()                      -- Get complete restoreOptions json for teams restore operation
    _json_restore_options()                     -- Get options json for teams restore operation
    restore_posts_to_html()                     -- Restore posts of a team as HTML
    get_team()                                  -- Get team object from team email address
    _json_cloud_app_association()               -- Get cloudAppAssociation json for teams association operation
    set_all_users_content()                     -- Add all teams to content
    _json_get_associations()                    -- Get associations json for a team
    get_associated_teams()                      -- Get all associated teams for a client
    remove_team_association()                   -- Removes user association from a teams client
    remove_all_users_content()                  -- Removes all user content from a teams client
    get_content_association()                   -- Get all associated contents for a client
    exclude_teams_from_backup()                 -- Excludes user association from a teams client
    _process_restore_posts_to_html()            -- Helper method to restore a team posts as HTML to another location
    _process_remove_association()               -- Helper method to change association of a teams client
     restore_out_of_place_to_file_location()     -- Restore a team to file location
    _json_restoreoptions_searchprocessinginfo_with_extra_queryparameters() -- Get searchprocessinginfo with extra query
                                                                           parameters json for teams restore operation.
    _json_restore_destinationTeamInfo()         -- Get destinationTeamInfo json for teams restore operation.
    restore_files_to_out_of_place()             -- Restore  files to another team.
    restore_to_original_location()              -- Restore team to original location.
"""

from __future__ import unicode_literals
from ...exception import SDKException
from ..casubclient import CloudAppsSubclient

import time
from copy import copy, deepcopy

from cvpysdk.job import Job
from ..cloudapps.teams_constants import TeamsConstants as const
import json


class TeamsSubclient(CloudAppsSubclient):
    """Derived class from Subclient Base class, representing a Microsoft Office 365 Teams subclient
    and to perform operations on that subclient.
    """

    def _json_subclient_entity(self):
        """Get subclientEntity json for teams association operation.
                Returns:
                    subclientEntity json for teams association operation
        """
        subclient_entity_json = copy(const.ADD_SUBCLIENT_ENTITY_JSON)
        subclient_entity_json['instanceId'] = int(self._instance_object.instance_id)
        subclient_entity_json['subclientId'] = int(self._subclient_id)
        subclient_entity_json['clientId'] = int(self._client_object.client_id)
        subclient_entity_json['applicationId'] = int(self._subClientEntity['applicationId'])
        return subclient_entity_json

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

        discovered_teams = self.discover()
        teams = [discovered_teams[team] for team in teams]

        url = self._services['SET_USER_POLICY_ASSOCIATION']

        for team in teams:

            subclient_entity_json = self._json_subclient_entity()

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

            request_json['cloudAppAssociation']['plan']['planId'] = int(
                self._commcell_object.plans.get(o365_plan).plan_id)
            flag, response = self._cvpysdk_object.make_request('POST', url, request_json)

            if not flag:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

    def backup(self, teams=None):
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
        url = self._services['CREATE_TASK']
        backup_subtask_json = copy(const.BACKUP_SUBTASK_JSON)
        request_json = deepcopy(const.BACKUP_REQUEST_JSON)
        request_json['taskInfo']['associations'] = [self._json_association()]

        if teams:
            discovered_teams = self.discover(refresh_cache=False)
            teams = [discovered_teams[team] for team in teams]
            team_json_list = []
            selected_items_json = []
            for team in teams:
                team_json = copy(const.BACKUP_TEAM_JSON)
                team_json['displayName'] = team['displayName']
                team_json['smtpAddress'] = team['smtpAddress']
                team_json['msTeamsInfo']['teamsCreatedTime'] = team['msTeamsInfo']['teamsCreatedTime']
                team_json['user'] = {"userGUID": team['user']['userGUID']}
                team_json_list.append(team_json)
                selected_items_json.append({
                    'selectedItems': {
                        "itemName": team['displayName'], "itemType": "Team"
                    }
                })
            backup_subtask_json['options']['commonOpts']['selectedItems'] = selected_items_json
            backup_subtask_json['options']['backupOpts']['cloudAppOptions']['userAccounts'] = team_json_list
        else:
            backup_subtask_json['options']['commonOpts']['selectedItems']= [{
                "itemName": "All%20teams", "itemType": "All teams"
            }]
            backup_subtask_json['options']['backupOpts'].pop('cloudAppOptions', None)
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

    def out_of_place_restore(self, team, destination_team, **kwargs):
        """Restore a team to another location.
            Args:
                team                (str)   --  The email ID of the team that needs to be restored.
                destination_team    (str)   --  The email ID of the team to be restored to.
                kwargs              (dict)
                    dest_subclient_object --    The subclient object of the destination client

            Returns:
                obj   --  Instance of job.

            Raises:
                SDKException:

                    If restore failed to run.
                    If response is empty.
                    If response is not success.

        """
        if not destination_team:
            raise SDKException(
                "Subclient", "101", "Destination team value cannot be none")
        discovered_teams = self.discover()
        team = [discovered_teams[team]]
        if not kwargs.get("dest_subclient_obj"):
            destination_team = discovered_teams[destination_team]
        else:
            dest_discovered_teams = kwargs.get("dest_subclient_obj").discover()
            destination_team = dest_discovered_teams[destination_team]
        request_json = {
            "taskInfo": {
                "task": const.RESTORE_TASK_JSON,
                "associations": [
                    self._json_association()
                ],
                "subTasks": [
                    {
                        "subTask": const.RESTORE_SUBTASK_JSON,
                        "options": self._json_restore_options(
                            team, **dict(kwargs, destination_team=destination_team,
                                         dest_subclient_obj=kwargs.get("dest_subclient_obj")))
                    }
                ]
            }
        }
        return self._process_restore(request_json)

    def _json_association(self):
        """Get association json for teams restore operation.
                Returns:
                    association json for restore oepration
        """
        _associtaions_json = self._subClientEntity
        _associtaions_json.pop('csGUID', None)
        _associtaions_json.pop('appName', None)
        _associtaions_json.pop('commCellName', None)
        if 'entityInfo' in _associtaions_json:
            _associtaions_json.pop('multiCommcellId', None)
        _associtaions_json["clientGUID"] = self._client_object.client_guid
        return _associtaions_json

    def _json_restoreoptions_searchprocessinginfo(self):
        """Get searchprocessingginfo json for teams restore operation.
                Returns:
                    searchprocessingginfo json for teams restore operation
        """
        return {
            "resultOffset": 0,
            "pageSize": 1,
            "queryParams": [
                {
                    "param": "ENABLE_MIXEDVIEW",
                    "value": "true"
                },
                {
                    "param": "RESPONSE_FIELD_LIST",
                    "value": "DATA_TYPE,CONTENTID,CV_OBJECT_GUID,PARENT_GUID,CV_TURBO_GUID,AFILEID,AFILEOFFSET,"
                             "COMMCELLNO,MODIFIEDTIME,SIZEINKB,BACKUPTIME,CISTATE,DATE_DELETED,TEAMS_ITEM_ID,"
                             "TEAMS_ITEM_NAME,TEAMS_NAME,TEAMS_SMTP,TEAMS_ITEM_TYPE,TEAMS_CHANNEL_TYPE,TEAMS_TAB_TYPE,"
                             "TEAMS_GROUP_VISIBILITY,TEAMS_GUID,TEAMS_CONV_ITEM_TYPE,TEAMS_CONV_MESSAGE_TYPE,"
                             "TEAMS_CONV_SUBJECT,TEAMS_CONV_IMPORTANCE,TEAMS_CONV_SENDER_TYPE,TEAMS_CONV_SENDER_NAME,"
                             "TEAMS_CONV_HAS_REPLIES,CI_URL,TEAMS_DRIVE_FOLDER_TYPE"
                }
            ],
            "sortParams": [
                {
                    "sortDirection": 0,
                    "sortField": "SIZEINKB"
                }
            ]
        }

    def _json_restoreoptions_advsearchgrp(self, teams):
        """Get advSearchGrp json for teams restore operation.
                Returns:
                    advSearchGrp json for teams restore operation
        """
        _advSearchGrp = {
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
                                    "values": [
                                        "1"
                                    ]
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
                                    "values": [team['user']['userGUID'].lower() for team in teams] if teams else []
                                }
                            }
                        ]
                    }
                }
            ],
            "galaxyFilter": [
                {
                    "appIdList": [
                        int(self._subclient_id)
                    ]
                }
            ]
        }
        return _advSearchGrp

    def _json_restoreoptions_findquery(self, teams):
        """Get findquery json for teams restore operation.
                Returns:
                    findquery json for teams restore operation
        """
        _findQuery = {
            "mode": 4,
            "facetRequests": {},
            "advSearchGrp": self._json_restoreoptions_advsearchgrp(teams),
            "searchProcessingInfo": self._json_restoreoptions_searchprocessinginfo()
        }
        return _findQuery

    def _json_restoreoptions_destination(self, destination_team, destination_channel=None):
        """Get destination json for teams restore operation.
                Args:
                    destination_team  (str) -- Name of destination team
                    destination_channel (str) -- Instance of channel object
                         Default : None
                Returns:
                    destination json for teams restore operation
        """
        _destination_team_json = {
            "destAppId": int(self._subClientEntity['applicationId']),
            "inPlace": destination_team == None,
            "destPath": [destination_team["displayName"]] if destination_team else [""],
            "destClient": {
                "clientId": int(self._client_object.client_id),
                "clientName": self._subClientEntity['clientName']
            }
        }
        if destination_channel:
            _destination_team_json['destPath'] = [destination_team["displayName"] + destination_channel.name]
        return _destination_team_json

    def _json_restoreoptions_msteamsrestoreoptions(self, teams, **kwargs):
        """Get msTeamsRestoreOptions json for teams restore operation.
                Args:
                    teams (list)  -- List of objects of team class
                Returns:
                    msTeamsRestoreOptions json for teams restore operation
        """
        selectedItemsToRestore = []
        for team in teams:
            selectedItemsToRestore.append({
                "itemId": team['user']['userGUID'].lower(),
                "path": "",
                "itemType": 1,
                "isDirectory": True
            })

        _msTeamsRestoreOptions = {
            "restoreAllMatching": False,
            "overWriteItems": kwargs.get("unconditionalOverwrite", False),
            "restoreToTeams": True,
            "destLocation": kwargs.get("destination_team").get("displayName") if kwargs.get("destination_team", {}).get("displayName") else "",
            "restorePostsAsHtml": kwargs.get("restorePostsAsHtml", False),
            "restoreUsingFindQuery": False,
            "selectedItemsToRestore": selectedItemsToRestore,
            "findQuery": self._json_restoreoptions_findquery(teams)
        }
        if kwargs.get("destination_team", None):
            _msTeamsRestoreOptions["destinationTeamInfo"] = {
                "tabId": "",
                "teamName": kwargs.get("destination_team")['displayName'],
                "tabName": "",
                "folder": "",
                "teamId": kwargs.get("destination_team")['user']['userGUID'].lower(),
                "destination": 1,
                "channelName": "",
                "channelId": ""
            }
        return _msTeamsRestoreOptions

    def _json_restoreoptions_cloudappsrestore(self, teams, **kwargs):
        """Get cloudAppsRestoreOptions json for teams restore operation.
                Args:
                    teams (list)  -- List of objects of team class
                Returns:
                    cloudAppsRestoreOptions json for teams restore operation
        """
        _cloudAppsRestoreOptions = {
            "instanceType": 36,
            "msTeamsRestoreOptions": self._json_restoreoptions_msteamsrestoreoptions(teams, **kwargs)
        }
        return _cloudAppsRestoreOptions

    def _json_restoreoptions(self, teams, **kwargs):
        """Get complete restoreOptions json for teams restore operation.
                Args:
                    teams (list)  -- List of objects of team class
                Returns:
                    restoreOptions json for teams restore operation
        """

        if kwargs.get("skip", False) and kwargs.get("unconditionalOverwrite", False):
            raise SDKException('Subclient', '102', "Both skip and unconditionalOverwrite cannot be True")
        selectedItems = []
        for team in teams:
            selectedItems.append({
                "itemName": team['user']['userGUID'].lower(),
                "itemType": "Team"
            })

        if kwargs.get("dest_subclient_obj"):
            dest_subclient_obj = kwargs.get("dest_subclient_obj")
            if isinstance(dest_subclient_obj, TeamsSubclient):
                dest_details = dest_subclient_obj._json_restoreoptions_destination(kwargs.get("destination_team", None))
            else:
                raise SDKException('Subclient', '102', "Wrongly supplied subclient object")
        else:
            dest_details = self._json_restoreoptions_destination(kwargs.get("destination_team", None))
        _restore_options = {
            "browseOption": {
                "timeRange": {}
            },
            "commonOptions": {
                "skip": kwargs.get("skip", True),
                "overwriteFiles": kwargs.get("unconditionalOverwrite", False),
                "unconditionalOverwrite": kwargs.get("unconditionalOverwrite", False)
            },
            "destination": dest_details,
            "fileOption": {
                "sourceItem": [
                    ""
                ]
            },
            "cloudAppsRestoreOptions": self._json_restoreoptions_cloudappsrestore(teams, **kwargs)
        }
        return _restore_options

    def _json_restore_options(self, teams, **kwargs):
        """Get options json for teams restore operation.
                Args:
                    teams (list)  -- List of objects of team class
                Returns:
                    options json for teams restore operation
        """
        selectedItems = []
        for team in teams:
            selectedItems.append({
                "itemName": team["displayName"],
                "itemType": "Team"
            })
        _options_json = {
            "commonOpts": {
                "notifyUserOnJobCompletion": False,
                "selectedItems": selectedItems
            },
            "restoreOptions": self._json_restoreoptions(teams, **kwargs)
        }
        return _options_json

    def restore_posts_to_html(self, teams, destination_team=None):
        """Restore posts of a team as HTML.
                Args:
                    team                (list)   --  The email ID of the teams that needs to be restored.
                    destination_team    (str)   --  The email ID of the team to be restored to.

                Returns:
                    obj   --  Instance of job.

                Raises:
                    SDKException:
                        If restore failed to run.
                        If response is empty.
                        If response is not success.

        """
        discovered_teams = self.discover()
        teams = [discovered_teams[team] for team in teams]
        if len(teams) == 1 and destination_team:
            destination_team = discovered_teams[destination_team]
        else:
            destination_team = None
        request_json = {
            "taskInfo": {
                "task": const.RESTORE_TASK_JSON,
                "associations": [
                    self._json_association()
                ],
                "subTasks": [
                    {
                        "subTask": const.RESTORE_SUBTASK_JSON,
                        "options": self._json_restore_options(
                            teams, destination_team=destination_team, restorePostsAsHtml=True
                        ) if destination_team else self._json_restore_options(
                            teams, restorePostsAsHtml=True)
                    }
                ]
            }
        }
        return self._process_restore(request_json)

    def get_team(self, team):
        """Get team object from team email address.
                Args:
                    team                (str)   --  The email ID of the teams that needs.

                Returns:
                    obj   --  Instance of Team.
        """
        discovered_teams = self.discover()
        return discovered_teams[team] if team in discovered_teams else None

    def _json_cloud_app_association(self, plan_name):
        """Get cloudAppAssociation json for teams association operation.
                Returns:
                    cloudAppAssociation json for teams association operation
        """
        if not plan_name:
            raise SDKException('Subclient', '102', "Plan name cannot be empty")
        plan_obj = self._commcell_object.plans.get(plan_name)
        if not plan_obj:
            raise SDKException('Subclient', '102', "Error in getting plan. Make sure the plan name is valid")

        _cloudAppAssociation = {
            "accountStatus": 0,
            "subclientEntity": self._json_subclient_entity(),
            "cloudAppDiscoverinfo":
                {
                    "userAccounts": [],
                    "groups":
                        [
                            {
                                "name": "All teams",
                                "id": ""
                            }
                        ],
                    "discoverByType": 13
                },
            "plan": {
                "planId": int(plan_obj.plan_id)
            }
        }
        return _cloudAppAssociation

    def set_all_users_content(self, plan_name):
        """Add all teams to content
                Args:
                    plan_name(str): Name of the plan to be associated with All teams content
        """
        request_json = {
            "LaunchAutoDiscovery": True,
            "cloudAppAssociation": self._json_cloud_app_association(plan_name)
        }
        url = self._services['SET_USER_POLICY_ASSOCIATION']
        flag, response = self._cvpysdk_object.make_request(
            'POST', url, request_json
        )
        if flag:
            if response.json():
                if 'response' in response.json():
                    response = response.json().get('response', [])
                    if response:
                        error_code = response[0].get('errorCode', -1)
                        if error_code != 0:
                            error_string = response.json().get('response', {})
                            raise SDKException(
                                'Subclient', '102', 'Failed to set all teams content \nError: "{0}"'.format(
                                    error_string)
                            )
                elif 'errorMessage' in response.json():
                    error_string = response.json().get('errorMessage', "")
                    o_str = 'Failed to set all teams content for association\nError: "{0}"'.format(error_string)
                    raise SDKException('Subclient', '102', o_str)
        else:
            raise SDKException('Response', '101', response.text)

    def _json_get_associations(self, **kwargs):
        """Get associations json for a team
            Returns:
                request json for associations for teams
        """
        return {
            "cloudAppAssociation": {
                "subclientEntity": {"subclientId": int(self._subclient_id)}
            },
            "bIncludeDeleted": False,
            "discoverByType": 5 if kwargs.get('AllContentType', False) else 12,
            "searchInfo": {"isSearch": 0, "searchKey": ""},
            "sortInfo": {
                "sortColumn": "O365Field_AUTO_DISCOVER", "sortOrder": 0
            }
        }

    def get_associated_teams(self, pagingInfo=None, **kwargs):
        """Get all associated teams for a client
                Args:
                    pagingInfo  (dict): Dict of Page number and pageSize

                Returns:
                    List of all user associations and their details
        """
        request_json = self._json_get_associations(**kwargs)
        if pagingInfo:
            request_json["pagingInfo"] = pagingInfo
        url = self._services['USER_POLICY_ASSOCIATION']
        flag, response = self._cvpysdk_object.make_request(
            'POST', url, request_json
        )
        if flag:
            resp = response.json()
            if resp:
                if 'errorMessage' in resp:
                    error_string = response.json().get('errorMessage', "")
                    o_str = 'Failed to get all associated Teams\nError: "{0}"'.format(error_string)
                    raise SDKException('Subclient', '102', o_str)
                if 'resp' in resp and 'errorCode' in resp['resp']:
                    raise SDKException(
                        'Subclient', '102', 'Failed to get all teams content. Check the input payload'
                    )
                return (resp['associations']) if 'associations' in resp else None
        else:
            raise SDKException('Response', '101', response.text)

    def remove_team_association(self, user_assoc):
        """Removes user association from a teams client
                Args:
                    user_assoc   (list): List of input users assoication object whose association is to be removed
                Returns
                    Boolean if the association was removed successfully

        """
        request_json = {
            "LaunchAutoDiscovery": False,
            "cloudAppAssociation": {
                "accountStatus": "DELETED",
                "subclientEntity": self._json_subclient_entity(),
                "cloudAppDiscoverinfo": {
                    "userAccounts": user_assoc,
                    "groups": [],
                    "discoverByType": 12
                }
            }
        }
        self._process_remove_association(request_json)

    def remove_all_users_content(self):
        """Removes all user content from a teams client
            Returns
                    Boolean if the association was removed successfully
        """
        contents = self.get_associated_teams(AllContentType=True)
        group = {}
        if contents:
            for content in contents:
                if content['groups'] and content['groups']['name'] == 'All teams':
                    group = content['groups']
                    break
            request_json = {
                "LaunchAutoDiscovery": True,
                "cloudAppAssociation": {
                    "accountStatus": "DELETED",
                    "subclientEntity": self._json_subclient_entity(),
                    "cloudAppDiscoverinfo": {
                        "userAccounts": [],
                        "groups": [group],
                        "discoverByType": 13
                    }
                }
            }
            self._process_remove_association(request_json)

    def exclude_teams_from_backup(self, user_assoc):
        """Excludes user association from a teams client
                Args:
                    users   (list): List of input users whose association is to be excluded

                Returns
                    Boolean if the association was removed successfully
        """
        request_json = {
            "LaunchAutoDiscovery": False,
            "cloudAppAssociation": {
                "accountStatus": "DISABLED",
                "subclientEntity": self._json_subclient_entity(),
                "cloudAppDiscoverinfo": {
                    "userAccounts": user_assoc,
                    "groups": [],
                    "discoverByType": 12
                }
            }
        }
        self._process_remove_association(request_json)

    def _process_restore(self, request_json):
        """Helper method to restore a team.

            Args:
                request_json        (str)   --  The request json to be passed.

            Returns:
                obj   --  Instance of Restore job.

            Raises:
                SDKException:
                    If request_json is empty or invalid
                    If restore failed to run.
                    If response is empty.
                    If response is not success.

        """
        if not request_json:
            raise SDKException('Subclient', '102', 'Request json is invalid')
        url = self._services['CREATE_TASK']
        flag, response = self._cvpysdk_object.make_request('POST', url, request_json)
        if flag:
            resp = response.json()
            if resp:
                if 'jobIds' in resp:
                    return Job(self._commcell_object, resp['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    raise SDKException('Subclient', '102', f"Restore failed, error message : {error_message}")
            else:
                raise SDKException('Response', '102', self._update_response_(response.text))
        else:
            raise SDKException('Response', '102', self._update_response_(response.text))

    def _process_remove_association(self, request_json):
        """Helper method to change association of a teams client
                Args:
                    request_json   (dict): Dictionary of input json.

                Raises:
                    SDKException:
                        If response is not success.
                        If response has errors
        """
        url = self._services['UPDATE_USER_POLICY_ASSOCIATION']
        flag, response = self._cvpysdk_object.make_request(
            'POST', url, request_json
        )
        if flag:
            resp = response.json()
            if "resp" in resp and 'errorCode' in resp['resp']:
                raise SDKException('Subclient', '102', 'Failed to remove association from Teams Client')
            if 'errorMessage' in response.json():
                error_string = response.json()['errorMessage']
                o_str = 'Failed to remove association from teams client\nError: "{0}"'.format(error_string)
                raise SDKException('Subclient', '102', o_str)
        else:
            raise SDKException('Response', '102', self._update_response_(response.text))

    def restore_out_of_place_to_file_location(self, source_team_mail, dest_client, dest_path, selected_items, values):
        """Restore a team to file location.

                    Args:
                        source_team_mail      (str)      --  The email ID of the team that needs to be restored.
                        dest_client           (str)      --  The name of the client to be restored to.
                        dest_path             (str)      --  The path of the client to be restored to.
                        selected_items        (list)     --  List of dictonary of properties of selected items.
                        values                (list)     --  Content id's of a selected items.
                    Returns:
                        obj   --  Instance of Restore job.

                    Raises:
                        SDKException:
                            If restore failed to run.
                            If response is empty.
                            If response is not success.

                """

        self._instance_object._restore_association = self._subClientEntity
        discovered_teams = self.discover()
        source_team = discovered_teams[source_team_mail]
        request_json = self._instance_object._restore_json()

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions'] = self._instance_object._cloud_apps_restore_json(source_team=source_team,
                                                                                        destination_team=source_team)
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]["findQuery"]["advSearchGrp"]["commonFilter"][0][
            "filter"]["filters"].append({
            "field": "IS_VISIBLE",
            "fieldValues": {
                "isMoniker": False,
                "isRange": False,
                "values": [
                    "true"
                ]
            },
            "intraFieldOp": 0,
            "intraFieldOpStr": "None"
        })

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]["findQuery"]["advSearchGrp"]["fileFilter"][0][
            "filter"]["filters"][0]["field"] = "CONTENTID"

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]["findQuery"]["searchProcessingInfo"] = \
            self._json_restoreoptions_searchprocessinginfo_with_extra_queryparameters(source_team)
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]["restoreToTeams"] = False
        request_json["taskInfo"]["subTasks"][0]['options']["restoreOptions"]["destination"] = {
            "destAppId": 33,
            "destClient": {
                "clientName": dest_client
            },
            "destPath": [
                dest_path
            ],
            "inPlace": False
        }

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]['selectedItemsToRestore'] = selected_items

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]["findQuery"]["advSearchGrp"]["fileFilter"][0][
            "filter"][
            "filters"][0]["fieldValues"]["values"] = values

        request_json['taskInfo']['subTasks'][0]['options']['commonOpts'] = {
            "notifyUserOnJobCompletion": False,
            "selectedItems": [
                {
                    "itemName": "Files",
                    "itemType": "Files"
                },
                {
                    "itemName": "Posts",
                    "itemType": "Posts",
                }
            ]
        }

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

    def _json_restoreoptions_searchprocessinginfo_with_extra_queryparameters(self, source_team):
        """
               Args:
                    source_team         (dict)   --  Dictionary of properties from discover() for team that is to be
                    restored.
               Returns:
                   queryparameters json for teams restore operation
               """

        _searchprocessinginfo = self._json_restoreoptions_searchprocessinginfo()
        _searchprocessinginfo["queryParams"].extend([
            {
                "param": "COLLAPSE_FIELD",
                "value": "CV_OBJECT_GUID"
            },
            {
                "param": "COLLAPSE_SORT",
                "value": "BACKUPTIME DESC"
            },
            {
                "param": "INDEX_ROUTING_KEY",
                "value": source_team['user']['userGUID'].lower()
            }
        ]
        )
        _searchprocessinginfo["pageSize"] = 20
        return _searchprocessinginfo

    def _json_restore_destinationTeamInfo(self, destination_team, channel):
        """Get destinationTeamInfo json for teams restore operation.
               Args:
                    destination_team      (dict)   --  Dictionary of properties from discover() for team that is to be
                    channel               (obj)    --  Instance of channel object.
               Returns:
                   destinationTeamInfo json for teams restore operation
               """
        _destinationteaminfo = {
            "tabId": "",
            "teamName": destination_team['displayName'],
            "tabName": "",
            "folder": "/" if channel else "",
            "teamId": destination_team['user']['userGUID'].lower(),
            "destination": 5 if channel else 1,
            "channelName": channel.name if channel else "",
            "channelId": channel.channel_id if channel else ""
        }
        return _destinationteaminfo

    def restore_files_to_out_of_place(self, source_team_mail, destination_team_mail, destination_channel,
                                      selected_files_ids, values, selected_files):
        """Restore  files to another team

                   Args:
                       source_team_mail         (str)      --  The email ID of the team that needs to be restored.
                       destination_team_mail    (str)      --  The name of the client to be restored to.
                       channel                  (obj)      --  The object of the channel to be restored.
                       selected_files_ids       (list)     --  List of dictonaries of properties of selected files with
                                                               contentids.
                       values                   (list)     --  Content id's of a selected files.
                       selected_files           (list)     --  List of dictonaries of files name and their type.
                   Returns:
                       obj   --  Instance of Restore job.

                   Raises:
                       SDKException:
                           If restore failed to run.
                           If response is empty.
                           If response is not success.

               """
        self._instance_object._restore_association = self._subClientEntity
        discovered_teams = self.discover()
        source_team = discovered_teams[source_team_mail]
        destination_team = discovered_teams[destination_team_mail]

        request_json = self._instance_object._restore_json()
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions'] = self._instance_object._cloud_apps_restore_json(source_team=source_team,
                                                                                        destination_team=
                                                                                        destination_team)
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]["findQuery"]["advSearchGrp"]["commonFilter"][0][
            "filter"]["filters"].append({
            "field": "IS_VISIBLE",
            "fieldValues": {
                "isMoniker": False,
                "isRange": False,
                "values": [
                    "true"
                ]
            },
            "intraFieldOp": 0,
            "intraFieldOpStr": "None"
        })

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]["findQuery"]["advSearchGrp"]["fileFilter"][0][
            "filter"]["filters"][0]["field"] = "CONTENTID"

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]["findQuery"]["searchProcessingInfo"] = \
            self._json_restoreoptions_searchprocessinginfo_with_extra_queryparameters(source_team)

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]['selectedItemsToRestore'] = selected_files_ids

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]["findQuery"]["advSearchGrp"]["fileFilter"][0][
            "filter"][
            "filters"][0]["fieldValues"]["values"] = values
        request_json['taskInfo']['subTasks'][0]['options']['commonOpts'] = {
            "notifyUserOnJobCompletion": False,
            "selectedItems": selected_files
        }
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]['destinationTeamInfo'] = \
            self._json_restore_destinationTeamInfo(destination_team, destination_channel)
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination'] = \
            self._json_restoreoptions_destination(destination_team, destination_channel)
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]['destLocation'] = destination_team['displayName'] + \
                                                                                  destination_channel.name

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

    def restore_to_original_location(self, team_email_id, skip_items=True, restore_posts_as_html=False):
        """Restore a team to original location.
                    Args:
                        team_email_id                (str)   --  The email ID of the team that needs to be restored.
                        skip_items                (bool)  --  To skip the items.
                             Default - True
                        restore_posts_as_html  (bool)  --  To restore pots as html under Files tab.
                             Default - False

                    Returns:
                        obj   --  Instance of job.

                    Raises:
                        SDKException:

                            If restore failed to run.
                            If response is empty.
                            If response is not success.

                """

        discovered_teams = self.discover()
        team = [discovered_teams[team_email_id]]
        unconditional_overwrite = False
        if not skip_items:
            unconditional_overwrite = True
        request_json = {
            "taskInfo": {
                "task": const.RESTORE_TASK_JSON,
                "associations": [
                    self._json_association()
                ],
                "subTasks": [
                    {
                        "subTask": const.RESTORE_SUBTASK_JSON,
                        "options": self._json_restore_options(
                            team, skip=skip_items, unconditionalOverwrite=unconditional_overwrite,
                            restorePostsAsHtml=restore_posts_as_html)
                    }
                ]
            }
        }

        return self._process_restore(request_json)
