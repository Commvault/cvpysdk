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
    refresh_retention_stats()                   -- refresh the retention stats for the client
    refresh_client_level_stats()                -- refresh the client level stats for the client
    backup_stats()                    -- Returns the client level stats for the client
    _process_web_search_response()               -- Helper method to process the web search response
    do_web_search()                             --  Method to perform a web search using the /Search endpoint
    find_teams()                                --  Method to find the list of files and their metadata
    preview_backed_file()                       --  Method to preview the backed up content
    run_restore_for_chat_to_onedrive()  -- Restore user chats to onedrive.
    restore_to_azure_blob()                     --  Restore teams/users to azure blob
    get_associated_users()                      --  Retrieve all associated users (discoverByType 28) for the client
    remove_user_association()                   --  Remove user (type 28) associations from a Teams client
"""

from __future__ import unicode_literals

import base64
from copy import copy, deepcopy
from typing import Any, Dict, List, Optional, Union
from enum import Enum

from cvpysdk.job import Job

from ...exception import SDKException
from ..casubclient import CloudAppsSubclient
from ..cloudapps.teams_constants import TeamsConstants as const


class TeamsSubclient(CloudAppsSubclient):
    """
    Represents a Microsoft Office 365 Teams subclient for managing backup, restore, and content operations.

    This class extends the CloudAppsSubclient to provide specialized functionality for Microsoft Teams
    within the Office 365 suite. It enables discovery, backup, restore, and management of Teams data,
    including team associations, content handling, and advanced restore options. The class supports
    both in-place and out-of-place restore scenarios, content exclusion, and provides utilities for
    previewing and searching backed-up data.

    Key Features:
        - Discover Teams and manage content associations
        - Perform full and incremental backups of Teams data
        - Restore Teams data to original or alternate locations, including file-level and channel-level restores
        - Restore posts as HTML and run chat restores to OneDrive
        - Exclude specific Teams from backup and remove associations as needed
        - Preview backed-up files and perform web-based searches
        - Refresh and retrieve backup and retention statistics
        - Advanced restore options including search processing, destination selection, and cloud app restore settings

    #ai-gen-doc
    """

    def _json_subclient_entity(self) -> dict:
        """Generate the subclientEntity JSON for Teams association operations.

        Returns:
            dict: A dictionary representing the subclientEntity JSON required for Teams association operations.

        Example:
            >>> teams_subclient = TeamsSubclient()
            >>> subclient_entity_json = teams_subclient._json_subclient_entity()
            >>> print(subclient_entity_json)
            # Output will be a dictionary suitable for Teams association API calls

        #ai-gen-doc
        """
        subclient_entity_json = copy(const.ADD_SUBCLIENT_ENTITY_JSON)
        subclient_entity_json['instanceId'] = int(self._instance_object.instance_id)
        subclient_entity_json['subclientId'] = int(self._subclient_id)
        subclient_entity_json['clientId'] = int(self._client_object.client_id)
        subclient_entity_json['applicationId'] = int(self._subClientEntity['applicationId'])
        return subclient_entity_json

    def discover(self, discovery_type: int = 8, refresh_cache: bool = True) -> dict:
        """Launch a discovery operation and return the discovered Microsoft Teams.

        Args:
            discovery_type: The type of discovery to perform.
                Common values include:
                    8  - Teams
                    7  - Users
                    22 - Groups
                Default is 8 (Teams).
            refresh_cache: If True, refreshes the discovery cache before performing the operation.
                Default is True.

        Returns:
            dict: A dictionary where each key is a team email ID and each value is a dictionary of team properties.

        Raises:
            SDKException: If the discovery fails to launch, the response is empty, or the response is not successful.

        Example:
            >>> subclient = TeamsSubclient()
            >>> teams = subclient.discover(discovery_type=8, refresh_cache=True)
            >>> print(f"Discovered {len(teams)} teams")
            >>> for team_email, team_props in teams.items():
            ...     print(f"Team: {team_email}, Properties: {team_props}")

        #ai-gen-doc
        """

        return self._instance_object.discover(discovery_type, refresh_cache=refresh_cache)

    def content(self, entities: 'Union[list, dict]', o365_plan: str, discovery_type: 'Enum') -> None:
        """Add teams to the Teams subclient content.

        This method adds teams, users, or groups to the Teams subclient. The `discover()` method must be called
        before using this method to ensure that the entities to be added are available for selection.

        Args:
            entities: A list of team, user, or group email IDs, or a dictionary specifying custom category conditions.
            o365_plan: The name of the Office 365 plan to associate with the content.
            discovery_type: The type of discovery to perform (e.g., Teams, Users, Groups), specified as an Enum.

        Raises:
            SDKException: If the content could not be set, if the response is empty, or if the response indicates failure.

        Example:
            >>> # Add a list of teams to the subclient
            >>> teams = ['team1@domain.com', 'team2@domain.com']
            >>> subclient.content(teams, 'O365_Default_Plan', DiscoveryType.TEAMS)
            >>>
            >>> # Add content using custom category conditions
            >>> custom_conditions = {'category': 'Education', 'location': 'US'}
            >>> subclient.content(custom_conditions, 'O365_Edu_Plan', DiscoveryType.USERS)

        #ai-gen-doc
        """

        url = self._services['SET_USER_POLICY_ASSOCIATION']
        subclient_entity_json = self._json_subclient_entity()
        request_json = deepcopy(const.ADD_REQUEST_JSON)
        request_json['cloudAppAssociation']['subclientEntity'] = subclient_entity_json
        useraccounts = []
        groups = []
        request_json['cloudAppAssociation']['plan']['planId'] = int(
            self._commcell_object.plans.get(o365_plan).plan_id)

        if discovery_type.value == 13:
            groups.append({
                "name": "All teams"
            })
            request_json['cloudAppAssociation']['cloudAppDiscoverinfo']['groups'] = groups

        elif discovery_type.value == 29:
            groups.append({
                "name": "All Users"
            })
            request_json['cloudAppAssociation']['cloudAppDiscoverinfo']['groups'] = groups

        elif discovery_type.value == 12:
            is_team_instance = True
            if isinstance(entities[0], str):
                is_team_instance = False
                discovered_teams = self.discover(discovery_type=const.ClOUD_APP_EDISCOVER_TYPE['Teams'])
                entities = [discovered_teams[team] for team in entities]
            for team in entities:
                user_json = copy(const.ADD_USER_JSON)
                user_json['_type_'] = 13 if is_team_instance else team['user']['_type_']
                user_json['userGUID'] = team.guid if is_team_instance else team['user']['userGUID']

                user_account_json = deepcopy(const.ADD_TEAM_JSON)
                user_account_json['displayName'] = team.name if is_team_instance else team['displayName']
                user_account_json['smtpAddress'] = team.mail if is_team_instance else team['smtpAddress']
                user_account_json['msTeamsInfo']['teamsCreatedTime'] = team.teamsCreatedTime if is_team_instance else \
                    team['msTeamsInfo']['teamsCreatedTime']
                user_account_json['user'] = user_json
                useraccounts.append(user_account_json)
            request_json['cloudAppAssociation']['cloudAppDiscoverinfo']['userAccounts'] = useraccounts

        elif discovery_type.value == 28:
            discovered_teams = self.discover(discovery_type=const.ClOUD_APP_EDISCOVER_TYPE['Users'])
            entities = [discovered_teams[team] for team in entities]
            for user in entities:
                user_json = copy(const.ADD_USER_JSON)
                user_json['_type_'] = user['user']['_type_']
                user_json['userGUID'] = user['user']['userGUID']

                user_account_json = deepcopy(const.ADD_TEAM_JSON)
                user_account_json['displayName'] = user['displayName']
                user_account_json['smtpAddress'] = user['smtpAddress']
                if 'teamsCreatedTime' in user_account_json['msTeamsInfo']:
                    del user_account_json['msTeamsInfo']['teamsCreatedTime']
                user_account_json['user'] = user_json
                useraccounts.append(user_account_json)
            request_json['cloudAppAssociation']['cloudAppDiscoverinfo']['userAccounts'] = useraccounts
            request_json['cloudAppAssociation']['cloudAppDiscoverinfo']['discoverByType'] = discovery_type.value

        elif discovery_type.value == 27:
            discovered_teams = self.discover(discovery_type=const.ClOUD_APP_EDISCOVER_TYPE['Groups'])
            entities = [discovered_teams[team] for team in entities]
            for Group in entities:
                user_account_json = deepcopy(const.ADD_GROUP_JSON)
                user_account_json['name'] = Group['name']
                user_account_json['id'] = Group['id']
                groups.append(user_account_json)
            request_json['cloudAppAssociation']['cloudAppDiscoverinfo']['groups'] = groups

        elif discovery_type.value == 100:
            url = self._services['CUSTOM_CATEGORY'] % (subclient_entity_json['subclientId'])
            custom_category_json = deepcopy(const.CUSTOM_CATEGORY_JSON)
            custom_category_json['subclientEntity']['subclientId'] = subclient_entity_json['subclientId']
            custom_category_json['planEntity']['planId'] = int(self._commcell_object.plans.get(o365_plan).plan_id)
            custom_category_json['categoryName'] = entities['name']
            custom_category_json['categoryQuery']['conditions'] = entities['conditions']
            custom_category_json['office365V2AutoDiscover']['clientId'] = subclient_entity_json['clientId']
            custom_category_json['office365V2AutoDiscover']['instanceId'] = subclient_entity_json['instanceId']
            request_json = custom_category_json

        flag, response = self._cvpysdk_object.make_request('POST', url, request_json)

        if not flag:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def backup(self, teams: Optional[List[str]] = None, convert_job_to_full: bool = False, discovery_type: int = 13,
               **kwargs: Any) -> 'Job':
        """Run an incremental or full backup for specified Microsoft Teams entities.

        Args:
            teams: Optional list of team email IDs to include in the backup. If None, all teams are considered.
            convert_job_to_full: If True, converts the backup job to a full backup. Defaults to False (incremental backup).
            discovery_type: Integer representing the type of entity to back up (e.g., user, team, group). Default is 13.
            **kwargs: Additional keyword arguments for advanced backup options.
                - items_selection_option (str): Item selection option (e.g., "7" for recently backed up entities).

        Returns:
            Job: An instance representing the initiated backup job.

        Raises:
            SDKException: If the backup fails to run, the response is empty, or the response indicates failure.

        Example:
            >>> # Run an incremental backup for specific teams
            >>> job = teams_subclient.backup(teams=['team1@example.com', 'team2@example.com'])
            >>> print(f"Backup job started with ID: {job.job_id}")
            >>>
            >>> # Run a full backup for all teams
            >>> job = teams_subclient.backup(convert_job_to_full=True)
            >>> print(f"Full backup job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        items_selection_option = kwargs.get('items_selection_option', '')

        url = self._services['CREATE_TASK']
        backup_subtask_json = copy(const.BACKUP_SUBTASK_JSON)
        request_json = deepcopy(const.BACKUP_REQUEST_JSON)
        request_json['taskInfo']['associations'] = [self._json_association()]

        if teams:
            is_team_instance = True
            if isinstance(teams[0], str):
                is_team_instance = False
                discovered_teams = self.discover(refresh_cache=False)
                if not discovered_teams:
                    raise SDKException('Subclient', '102', 'No teams discovered. Please check Azure app details associated with client.')
                teams = [discovered_teams[team] for team in teams]

            team_json_list = []
            selected_items_json = []
            for team in teams:
                team_json = copy(const.BACKUP_TEAM_JSON)
                team_json['displayName'] = team.name if is_team_instance else team['displayName']
                team_json['smtpAddress'] = team.mail if is_team_instance else team['smtpAddress']
                if is_team_instance:
                    team_json['msTeamsInfo']['teamsCreatedTime'] = team.teamsCreatedTime
                else:
                    if team.get('msTeamsInfo',{}).get('teamsCreatedTime'):
                        team_json['msTeamsInfo']['teamsCreatedTime'] = team['msTeamsInfo']['teamsCreatedTime']
                team_json['user'] = {"userGUID": team.guid if is_team_instance else team['user']['userGUID']}
                team_json_list.append(team_json)
                selected_items_json.append({

                        "itemName": team.name if is_team_instance else team['displayName'], "itemType": "User" if discovery_type==7 else "Team"

                })
            backup_subtask_json['options']['commonOpts']['jobMetadata'][0]['selectedItems'] = selected_items_json
            backup_subtask_json['options']['backupOpts']['cloudAppOptions']['userAccounts'] = team_json_list
        else:
            backup_subtask_json['options']['commonOpts']['jobMetadata'][0]['selectedItems'] = [{
                "itemName": "All%20teams", "itemType": "All teams"
            }]
            backup_subtask_json['options']['backupOpts'].pop('cloudAppOptions', None)

        if convert_job_to_full:
            backup_subtask_json['options']['backupOpts']['cloudAppOptions']["forceFullBackup"] = convert_job_to_full
            backup_subtask_json['options']['commonOpts']['jobMetadata'][0]['jobOptionItems'][0]['value'] = "Enabled"

        if items_selection_option != '':
            backup_subtask_json['options']['commonOpts']['itemsSelectionOption'] = items_selection_option

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

    def out_of_place_restore(self, team: str, destination_team: str, **kwargs) -> 'Job':
        """Restore a Microsoft Teams team to a different location (out-of-place restore).

        This method restores the specified source team to a destination team, which may be on a different client or subclient.
        Additional options can be provided via keyword arguments, such as specifying the destination subclient object.

        Args:
            team: The email ID of the source team to be restored.
            destination_team: The email ID of the destination team where the data will be restored.
            **kwargs: Additional keyword arguments for advanced restore options.
                - dest_subclient_object: The subclient object of the destination client.

        Returns:
            Job: An instance representing the restore job.

        Raises:
            SDKException: If the restore operation fails to run, if the response is empty, or if the response indicates failure.

        Example:
            >>> # Restore a team to a different location
            >>> job = teams_subclient.out_of_place_restore(
            ...     team="source_team@domain.com",
            ...     destination_team="dest_team@domain.com",
            ...     dest_subclient_object=destination_subclient
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if not destination_team:
            raise SDKException(
                "Subclient", "101", "Destination team value cannot be none")
        discovered_teams = self.discover()
        team = [discovered_teams[team]]
        if not kwargs.get("dest_subclient_obj"):
            destination_team = discovered_teams[destination_team]
        else:
            dest_discovered_teams = kwargs.get("dest_subclient_obj").discover(refresh_cache=False)
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

    def _json_association(self) -> dict:
        """Generate the association JSON required for Teams restore operations.

        Returns:
            dict: A dictionary representing the association JSON for the restore operation.

        Example:
            >>> teams_subclient = TeamsSubclient()
            >>> association_json = teams_subclient._json_association()
            >>> print(association_json)
            # Output will be a dictionary containing association details for Teams restore

        #ai-gen-doc
        """
        _associtaions_json = self._subClientEntity
        _associtaions_json.pop('csGUID', None)
        _associtaions_json.pop('appName', None)
        _associtaions_json.pop('commCellName', None)
        if 'entityInfo' in _associtaions_json:
            _associtaions_json.pop('multiCommcellId', None)
        _associtaions_json["clientGUID"] = self._client_object.client_guid
        return _associtaions_json

    def _json_restoreoptions_searchprocessinginfo(self) -> dict:
        """Retrieve the search processing information JSON for Teams restore operations.

        Returns:
            dict: A dictionary containing the search processing information required for Teams restore operations.

        Example:
            >>> teams_subclient = TeamsSubclient()
            >>> search_info = teams_subclient._json_restoreoptions_searchprocessinginfo()
            >>> print(search_info)
            >>> # The returned dictionary can be used as part of a Teams restore request

        #ai-gen-doc
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

    def _json_restoreoptions_advsearchgrp(self, teams: list) -> dict:
        """Generate the advSearchGrp JSON structure for Teams restore operations.

        Args:
            teams: A list of Teams or team identifiers to include in the restore operation.

        Returns:
            A dictionary representing the advSearchGrp JSON required for Teams restore.

        Example:
            >>> teams_list = ['TeamA', 'TeamB']
            >>> adv_search_json = subclient._json_restoreoptions_advsearchgrp(teams_list)
            >>> print(adv_search_json)
            {'advSearchGrp': [...]}  # Example output structure

        #ai-gen-doc
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

    def _json_restoreoptions_findquery(self, teams: list) -> dict:
        """Generate the findquery JSON payload for a Teams restore operation.

        Args:
            teams: A list of Teams or team identifiers for which the findquery JSON should be generated.

        Returns:
            A dictionary representing the findquery JSON structure required for the Teams restore operation.

        Example:
            >>> teams_list = ['TeamA', 'TeamB']
            >>> findquery_json = subclient._json_restoreoptions_findquery(teams_list)
            >>> print(findquery_json)
            # Output will be a dictionary suitable for use in a Teams restore API call

        #ai-gen-doc
        """
        _findQuery = {
            "mode": 4,
            "facetRequests": {},
            "advSearchGrp": self._json_restoreoptions_advsearchgrp(teams),
            "searchProcessingInfo": self._json_restoreoptions_searchprocessinginfo()
        }
        return _findQuery

    def _json_restoreoptions_destination(self, destination_team: str, destination_channel: str = None) -> dict:
        """Generate the destination JSON payload for a Teams restore operation.

        Args:
            destination_team: The name of the destination Microsoft Teams team.
            destination_channel: Optional; the name of the destination channel within the team. If not provided, the restore will target the team as a whole.

        Returns:
            A dictionary representing the destination JSON for the Teams restore operation.

        Example:
            >>> subclient = TeamsSubclient()
            >>> dest_json = subclient._json_restoreoptions_destination('MarketingTeam', 'General')
            >>> print(dest_json)
            {'team': 'MarketingTeam', 'channel': 'General'}

        #ai-gen-doc
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

    def _json_restoreoptions_msteamsrestoreoptions(self, teams: list, **kwargs) -> dict:
        """Generate the msTeamsRestoreOptions JSON for a Teams restore operation.

        Args:
            teams: List of team objects to be included in the restore operation.
            **kwargs: Additional keyword arguments for customization of restore options.

        Returns:
            A dictionary representing the msTeamsRestoreOptions JSON for the specified Teams restore operation.

        Example:
            >>> teams_list = [team1, team2]
            >>> options_json = subclient._json_restoreoptions_msteamsrestoreoptions(teams_list)
            >>> print(options_json)
            {'msTeamsRestoreOptions': {...}}

        #ai-gen-doc
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
            "restoreToTeams": kwargs.get("restoreToTeams", True),
            "destLocation": kwargs.get("destination_team").get("displayName") if kwargs.get("destination_team", {}).get(
                "displayName") else "",
            "restorePostsAsHtml": kwargs.get("restorePostsAsHtml", False),
            "restoreUsingFindQuery": False,
            "selectedItemsToRestore": selectedItemsToRestore,
            "findQuery": self._json_restoreoptions_findquery(teams)
        }
        if kwargs.get("restoreToBlob", False):
            _msTeamsRestoreOptions["restoreToBlob"] = True
            _msTeamsRestoreOptions["blobContainerCredId"] = kwargs.get("blobContainerId")
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

    def _json_restoreoptions_cloudappsrestore(self, teams: list, **kwargs) -> dict:
        """Generate the cloudAppsRestoreOptions JSON for a Teams restore operation.

        Args:
            teams: List of team objects to be restored. Each item should be an instance of the team class.
            **kwargs: Additional keyword arguments for customization of the restore options.

        Returns:
            A dictionary representing the cloudAppsRestoreOptions JSON for the Teams restore operation.

        Example:
            >>> teams_list = [team1, team2]
            >>> options = subclient._json_restoreoptions_cloudappsrestore(teams_list, restoreToOriginal=True)
            >>> print(options)
            {'cloudAppsRestoreOptions': {...}}

        #ai-gen-doc
        """
        _cloudAppsRestoreOptions = {
            "instanceType": 36,
            "msTeamsRestoreOptions": self._json_restoreoptions_msteamsrestoreoptions(teams, **kwargs)
        }
        return _cloudAppsRestoreOptions

    def _json_restoreoptions(self, teams: List, **kwargs: Any) -> Dict[str, Any]:
        """Generate the complete restoreOptions JSON for a Teams restore operation.

        Args:
            teams: List of team objects to be restored. Each item should be an instance of the team class.
            **kwargs: Additional keyword arguments for customizing restore options.

        Returns:
            Dictionary representing the restoreOptions JSON for the Teams restore operation.

        Example:
            >>> teams_list = [Team('TeamA'), Team('TeamB')]
            >>> restore_options = subclient._json_restoreoptions(teams_list, restore_to_original=True)
            >>> print(restore_options)
            >>> # The returned dictionary can be used to initiate a restore operation

        #ai-gen-doc
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

    def _json_restore_options(self, teams: list, **kwargs) -> dict:
        """Generate the options JSON for a Teams restore operation.

        Args:
            teams: List of team objects to be restored. Each item should be an instance of the team class.
            **kwargs: Additional keyword arguments for customizing the restore options.

        Returns:
            A dictionary representing the options JSON required for the Teams restore operation.

        Example:
            >>> teams_list = [team1, team2]
            >>> options_json = subclient._json_restore_options(teams_list, restore_to_original=True)
            >>> print(options_json)
            {'teams': [...], 'restore_to_original': True, ...}

        #ai-gen-doc
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

    def restore_posts_to_html(self, teams: list, destination_team: str = None) -> object:
        """Restore posts from specified Microsoft Teams as HTML files.

        This method initiates a restore operation that exports posts from the given Teams
        (identified by their email IDs) as HTML files. Optionally, you can specify a
        destination team email ID to restore the posts to a different team.

        Args:
            teams: List of email IDs representing the Teams whose posts need to be restored.
            destination_team: Optional; the email ID of the team to which the posts should be restored.
                If not provided, posts are restored to their original teams.

        Returns:
            An object representing the job instance for the restore operation.

        Raises:
            SDKException: If the restore operation fails to run, if the response is empty,
                or if the response indicates failure.

        Example:
            >>> teams_list = ['team1@example.com', 'team2@example.com']
            >>> job = subclient.restore_posts_to_html(teams_list)
            >>> print(f"Restore job started with ID: {job.job_id}")

            >>> # Restore posts to a different team
            >>> job = subclient.restore_posts_to_html(['team3@example.com'], destination_team='archive_team@example.com')
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
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

    def get_team(self, team: str) -> Dict[str, Any]:
        """Retrieve a Team object using the team's email address.

        Args:
            team: The email address of the team to retrieve.

        Returns:
            A dictionary containing the properties of the specified team. If the team is not found, returns None.

        Example:
            >>> subclient = TeamsSubclient()
            >>> team_info = subclient.get_team('devteam@company.com')
            >>> print(f"Team information: {team_info}")

        #ai-gen-doc
        """
        discovered_teams = self.discover()
        return discovered_teams[team] if team in discovered_teams else None

    def _json_cloud_app_association(self, plan_name: str) -> dict:
        """Generate the cloudAppAssociation JSON for Teams association operations.

        Args:
            plan_name: The name of the plan to associate with the Teams subclient.

        Returns:
            A dictionary representing the cloudAppAssociation JSON required for Teams association operations.

        Example:
            >>> subclient = TeamsSubclient()
            >>> association_json = subclient._json_cloud_app_association("DefaultPlan")
            >>> print(association_json)
            # Output: {'planName': 'DefaultPlan', ...}

        #ai-gen-doc
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

    def set_all_users_content(self, plan_name: str) -> None:
        """Add all Teams users to the subclient content using the specified plan.

        Args:
            plan_name: The name of the plan to associate with the "All Teams" content.

        Example:
            >>> subclient = TeamsSubclient()
            >>> subclient.set_all_users_content("DefaultTeamsPlan")
            >>> print("All Teams users have been added to the subclient content.")

        #ai-gen-doc
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

    def _json_get_associations(self, **kwargs: dict) -> dict:
        """Generate the JSON payload for retrieving associations for a team.

        This method constructs and returns the request JSON required to fetch
        associations related to a team, using any additional keyword arguments provided.

        Args:
            **kwargs: Arbitrary keyword arguments to customize the associations request.

        Returns:
            dict: The JSON payload for the associations request.

        Example:
            >>> subclient = TeamsSubclient()
            >>> payload = subclient._json_get_associations(team_id='12345')
            >>> print(payload)
            {'team_id': '12345', ...}

        #ai-gen-doc
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

    def get_associated_teams(self, pagingInfo: Optional[dict] = None, **kwargs: dict) -> list:
        """Retrieve all associated teams for the client.

        Args:
            pagingInfo: Optional dictionary specifying pagination information, such as page number and page size.
                Example: {'pageNumber': 1, 'pageSize': 50}
            **kwargs: Additional keyword arguments for advanced filtering or query customization.

        Returns:
            A list containing details of all user associations and their corresponding teams.

        Example:
            >>> teams = subclient.get_associated_teams(pagingInfo={'pageNumber': 1, 'pageSize': 100})
            >>> print(f"Number of associated teams: {len(teams)}")
            >>> # Each item in the list contains details about a team association

        #ai-gen-doc
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

    def remove_team_association(self, user_assoc: list) -> bool:
        """Remove user associations from a Teams client.

        Args:
            user_assoc: List of user association objects to be removed from the Teams client.

        Returns:
            True if the associations were removed successfully, False otherwise.

        Example:
            >>> users_to_remove = [user1_assoc, user2_assoc]
            >>> result = teams_subclient.remove_team_association(users_to_remove)
            >>> print(f"Associations removed: {result}")

        #ai-gen-doc
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

    def get_associated_users(self) -> list:
        """Retrieve all associated users (discoverByType 28) for the client."""
        request_json = {
            "cloudAppAssociation": {
                "subclientEntity": {"subclientId": int(self._subclient_id)}
            },
            "bIncludeDeleted": False,
            "discoverByType": 28,
            "searchInfo": {"isSearch": 0, "searchKey": ""},
            "sortInfo": {
                "sortColumn": "O365Field_AUTO_DISCOVER", "sortOrder": 0
            }
        }
        url = self._services['USER_POLICY_ASSOCIATION']
        flag, response = self._cvpysdk_object.make_request('POST', url, request_json)
        if flag:
            resp = response.json()
            if resp:
                if 'errorMessage' in resp:
                    raise SDKException('Subclient', '102',
                                       f'Failed to get associated users\nError: "{resp.get("errorMessage")}"')
                return resp.get('associations')
        else:
            raise SDKException('Response', '101', response.text)

    def remove_user_association(self, user_assoc: list) -> None:
        """Remove user (type 28) associations from a Teams client.
        Args:
            user_assoc: List of user association objects to be removed from the Teams client.

        Example:
            >>> users_to_remove = [user1_assoc, user2_assoc]
            >>> result = teams_subclient.remove_user_association(users_to_remove)
            >>> print(f"Associations removed: {result}")
        """
        request_json = {
            "LaunchAutoDiscovery": False,
            "cloudAppAssociation": {
                "accountStatus": "DELETED",
                "subclientEntity": self._json_subclient_entity(),
                "cloudAppDiscoverinfo": {
                    "userAccounts": user_assoc,
                    "groups": [],
                    "discoverByType": 28
                }
            }
        }
        self._process_remove_association(request_json)

    def remove_all_users_content(self) -> bool:
        """Remove all user content from a Teams client.

        This method removes all user-associated content from the Teams client managed by this subclient.

        Returns:
            bool: True if all user content was removed successfully, False otherwise.

        Example:
            >>> subclient = TeamsSubclient()
            >>> result = subclient.remove_all_users_content()
            >>> print(f"All user content removed: {result}")

        #ai-gen-doc
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

    def exclude_teams_from_backup(self, user_assoc: list) -> bool:
        """Exclude specified user associations from a Teams client backup.

        Args:
            user_assoc: List of users whose associations should be excluded from the Teams backup.

        Returns:
            True if the user associations were successfully excluded; False otherwise.

        Example:
            >>> subclient = TeamsSubclient()
            >>> users_to_exclude = ['user1@example.com', 'user2@example.com']
            >>> result = subclient.exclude_teams_from_backup(users_to_exclude)
            >>> print(f"Exclusion successful: {result}")

        #ai-gen-doc
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

    def _process_restore(self, request_json: str) -> 'Job':
        """Helper method to restore a team using the provided request JSON.

        This method initiates a restore operation for a team based on the given request JSON.
        It returns an instance of the Job representing the restore process.

        Args:
            request_json: The request JSON string containing restore parameters.

        Returns:
            Job: An instance representing the initiated restore job.

        Raises:
            SDKException: If the request_json is empty or invalid.
            SDKException: If the restore operation fails to run.
            SDKException: If the response is empty or not successful.

        Example:
            >>> teams_subclient = TeamsSubclient()
            >>> request_json = '{"teamId": "12345", "restoreOptions": {...}}'
            >>> restore_job = teams_subclient._process_restore(request_json)
            >>> print(f"Restore job started: {restore_job}")

        #ai-gen-doc
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

    def _process_remove_association(self, request_json: dict) -> None:
        """Change the association of a Teams client using the provided request JSON.

        This helper method processes the removal of an association for a Teams client
        based on the input JSON payload.

        Args:
            request_json: Dictionary containing the input JSON for the association change.

        Raises:
            SDKException: If the response is not successful or contains errors.

        Example:
            >>> request_payload = {
            ...     "clientId": 12345,
            ...     "associationType": "remove"
            ... }
            >>> teams_subclient._process_remove_association(request_payload)
            >>> # If the operation fails, an SDKException will be raised

        #ai-gen-doc
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

    def restore_out_of_place_to_file_location(
            self,
            source_team_mail: str,
            dest_client: str,
            dest_path: str,
            selected_items: list,
            values: list
    ) -> 'Job':
        """Restore a Microsoft Teams team to a specified file location on a destination client.

        This method initiates an out-of-place restore of a team, allowing you to restore selected items
        from the source team to a specific path on a different client.

        Args:
            source_team_mail: The email ID of the team to be restored.
            dest_client: The name of the destination client where the data will be restored.
            dest_path: The file system path on the destination client where the data will be restored.
            selected_items: A list of dictionaries, each containing properties of the selected items to restore.
            values: A list of content IDs corresponding to the selected items.

        Returns:
            Job: An instance representing the restore job that was initiated.

        Raises:
            SDKException: If the restore operation fails to run, if the response is empty, or if the response indicates failure.

        Example:
            >>> selected_items = [
            ...     {"item_name": "Channel1", "item_type": "channel"},
            ...     {"item_name": "Channel2", "item_type": "channel"}
            ... ]
            >>> values = [12345, 67890]
            >>> job = teams_subclient.restore_out_of_place_to_file_location(
            ...     source_team_mail="team@example.com",
            ...     dest_client="DestinationClient",
            ...     dest_path="C:\\Restores\\Teams",
            ...     selected_items=selected_items,
            ...     values=values
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
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

    def _json_restoreoptions_searchprocessinginfo_with_extra_queryparameters(self, source_team: dict) -> dict:
        """Generate query parameters JSON for Teams restore operation with extra search processing information.

        Args:
            source_team: Dictionary containing properties of the team to be restored, typically obtained from the `discover()` method.

        Returns:
            Dictionary representing the query parameters JSON required for the Teams restore operation.

        Example:
            >>> team_properties = subclient.discover()['TeamA']
            >>> query_params = subclient._json_restoreoptions_searchprocessinginfo_with_extra_queryparameters(team_properties)
            >>> print(query_params)
            >>> # Use the returned query_params in a restore operation

        #ai-gen-doc
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

    def _json_restore_destinationTeamInfo(self, destination_team: dict, channel: object) -> dict:
        """Generate the destinationTeamInfo JSON structure for a Teams restore operation.

        Args:
            destination_team: Dictionary containing properties of the destination team, typically obtained from the discover() method.
            channel: An instance of the channel object representing the Teams channel to be restored.

        Returns:
            A dictionary representing the destinationTeamInfo JSON required for the Teams restore operation.

        Example:
            >>> team_info = subclient._json_restore_destinationTeamInfo(destination_team, channel)
            >>> print(team_info)
            {'teamId': '...', 'channelId': '...', ...}

        #ai-gen-doc
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

    def restore_files_to_out_of_place(
            self,
            source_team_mail: str,
            destination_team_mail: str,
            destination_channel: object,
            selected_files_ids: list,
            values: list,
            selected_files: list
    ) -> object:
        """Restore selected files from one Microsoft Teams team to another (out-of-place restore).

        Args:
            source_team_mail: The email ID of the source team from which files will be restored.
            destination_team_mail: The email ID of the destination team where files will be restored.
            destination_channel: The channel object in the destination team to which files will be restored.
            selected_files_ids: List of dictionaries containing properties (including content IDs) of the selected files.
            values: List of content IDs for the selected files to be restored.
            selected_files: List of dictionaries containing file names and their types.

        Returns:
            An object representing the restore job instance.

        Raises:
            SDKException: If the restore operation fails to run, if the response is empty, or if the response indicates failure.

        Example:
            >>> source_team = "source_team@domain.com"
            >>> dest_team = "destination_team@domain.com"
            >>> dest_channel = channel_obj  # Channel object for the destination team
            >>> selected_files_ids = [{"contentId": "12345", "name": "file1.docx"}]
            >>> values = ["12345"]
            >>> selected_files = [{"name": "file1.docx", "type": "docx"}]
            >>> job = teams_subclient.restore_files_to_out_of_place(
            ...     source_team, dest_team, dest_channel, selected_files_ids, values, selected_files
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
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

    def restore_to_original_location(self, team_email_id: str, skip_items: bool = True,
                                     restore_posts_as_html: bool = False) -> 'Job':
        """Restore a Microsoft Teams team to its original location.

        Args:
            team_email_id: The email ID of the team to be restored.
            skip_items: Whether to skip restoring items. Defaults to True.
            restore_posts_as_html: If True, restores posts as HTML files under the Files tab. Defaults to False.

        Returns:
            Job: An instance representing the restore job.

        Raises:
            SDKException: If the restore operation fails to run, if the response is empty, or if the response indicates failure.

        Example:
            >>> subclient = TeamsSubclient()
            >>> job = subclient.restore_to_original_location('team@example.com', skip_items=False, restore_posts_as_html=True)
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
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

    def restore_to_azure_blob(self, teams: list, blob_name: str) -> 'Job':
        """
        Restore to Azure Blob
        Args:
            teams : Team's Email Id
            blob_name: Name of the Azure Blob credential to which the restore will be performed.

        Returns:
            Job: A Job object representing the restore operation.
        """
        discovered_teams = self.discover()
        teams = [discovered_teams[team] for team in teams]
        credential = self._commcell_object.credentials.get(blob_name)
        request_json = {
            "taskInfo": {
                "task": const.RESTORE_TASK_JSON,
                "associations": [
                    self._json_association()
                ],
                "subTasks": [
                    {
                        "subTask": const.RESTORE_SUBTASK_JSON,
                        "options":self._json_restore_options(
                            teams, restorePostsAsHtml=True, restoreToTeams=False, restoreToBlob=True, blobContainerId=credential.credential_id)
                    }
                ]
            }
        }
        return self._process_restore(request_json)

    def refresh_retention_stats(self) -> None:
        """Refresh the retention statistics for the Teams client.

        This method updates the retention statistics, ensuring that the latest data is available
        for the Teams client associated with this subclient.

        Example:
            >>> subclient = TeamsSubclient()
            >>> subclient.refresh_retention_stats()
            >>> print("Retention statistics refreshed successfully.")

        #ai-gen-doc
        """
        request_json = {
            "appType": const.INDEX_APP_TYPE,
            "subclientId": int(self._subclient_id)
        }
        refresh_retention = self._services['OFFICE365_PROCESS_INDEX_RETENTION_RULES']
        flag, response = self._cvpysdk_object.make_request('POST', refresh_retention, request_json)

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json().get('errorCode')
                if error_code != 0:
                    error_message = response.json().get('errorMessage')
                    output_string = f'Failed to refresh retention stats \nError: {error_message}'
                    raise SDKException('Subclient', '102', output_string)
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def refresh_client_level_stats(self) -> None:
        """Refresh the client-level statistics for the Teams client.

        This method updates the stored statistics for the associated Teams client,
        ensuring that the latest data is available for reporting or analysis.

        Example:
            >>> teams_subclient = TeamsSubclient()
            >>> teams_subclient.refresh_client_level_stats()
            >>> print("Client-level stats refreshed successfully.")

        #ai-gen-doc
        """
        request_json = {
            "appType": const.INDEX_APP_TYPE,
            "teamsIdxStatsReq":
                [{
                    "subclientId": int(self._subclient_id), "type": 0}]
        }
        refresh_backup_stats = self._services['OFFICE365_POPULATE_INDEX_STATS']
        flag, response = self._cvpysdk_object.make_request('POST', refresh_backup_stats, request_json)

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json().get('errorCode')
                if error_code != 0:
                    error_message = response.json().get('errorMessage')
                    output_string = f'Failed to refresh client level stats \nError: {error_message}'
                    raise SDKException('Subclient', '102', output_string)
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def backup_stats(self) -> dict:
        """Get the client-level backup statistics for the Teams subclient.

        Returns:
            dict: A dictionary containing the backup statistics for the client.

        Example:
            >>> teams_subclient = TeamsSubclient()
            >>> stats = teams_subclient.backup_stats
            >>> print(f"Backup stats: {stats}")

        #ai-gen-doc
        """
        backupset_id = int(self._subClientEntity.get('backupsetId'))
        get_backup_stats = self._services['OFFICE365_OVERVIEW_STATS'] % backupset_id
        flag, response = self._cvpysdk_object.make_request('GET', get_backup_stats)

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json().get('errorCode')
                if error_code != 0:
                    error_message = response.json().get('errorMessage')
                    output_string = f'Failed to get client level stats \nError: {error_message}'
                    raise SDKException('Subclient', '102', output_string)
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

        return response.json()

    def _process_web_search_response(self, flag: bool, response: dict) -> dict:
        """Process the response from a web search operation.

        Args:
            flag: Indicates whether the web search response was successful (True) or not (False).
            response: The JSON response dictionary received from the server for the web search request.

        Returns:
            A dictionary containing all the paths found in the web search, along with additional metadata retrieved from the browse operation.

        Example:
            >>> subclient = TeamsSubclient()
            >>> response = {
            ...     "status": "success",
            ...     "data": [{"path": "/team/site", "metadata": {"size": 1024}}]
            ... }
            >>> result = subclient._process_web_search_response(True, response)
            >>> print(result)
            {'/team/site': {'size': 1024}}

        #ai-gen-doc
        """
        if flag:
            response_json = response.json()

            _search_result = response_json.get("searchResult")
            return _search_result.get("resultItem")

        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def do_web_search(self, **kwargs: dict) -> dict:
        """Perform a web search using the /Search endpoint for O365 agents.

        This method allows you to perform a web search operation using the default browse endpoint
        for new O365 agents. Additional search parameters can be provided as keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments representing search parameters to be used for the browse.

        Returns:
            dict: The response from the web search operation, typically containing search results and metadata.

        Example:
            >>> subclient = TeamsSubclient()
            >>> results = subclient.do_web_search(query="project files", limit=10)
            >>> print(results)
            {'results': [...], 'count': 10}

        #ai-gen-doc
        """
        self._TEAMS_BROWSE = self._commcell_object._services['DO_WEB_SEARCH']
        _browse_options = kwargs
        _parent_guid = kwargs.get("parent_guid", "00000000000000000000000000000001")

        _browse_req = {
            "mode": 4,
            "advSearchGrp": {
                "commonFilter": [
                    {
                        "filter": {
                            "interFilterOP": 0,
                            "filters": [

                            ]
                        }
                    }
                ],
                "fileFilter": [
                    {
                        "interGroupOP": 2,
                        "filter": {
                            "interFilterOP": 2,
                            "filters": [
                                {
                                    "field": "HIDDEN",
                                    "intraFieldOp": 4,
                                    "fieldValues": {
                                        "values": [
                                            "true"
                                        ]
                                    }
                                },
                                {
                                    "field": "PARENT_GUID",
                                    "intraFieldOp": 0,
                                    "fieldValues": {
                                        "values": [
                                            _parent_guid
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ],
                "emailFilter": [],
                "galaxyFilter": [
                    {
                        "appIdList": [
                            int(self.subclient_id)
                        ]
                    }
                ]
            },
            "searchProcessingInfo": {
                "resultOffset": 0,
                "pageSize": 100,
                "queryParams": [
                    {
                        "param": "ENABLE_MIXEDVIEW",
                        "value": "true"
                    },
                    {
                        "param": "RESPONSE_FIELD_LIST",
                        "value": "DATA_TYPE,CONTENTID,CV_OBJECT_GUID,PARENT_GUID,CV_TURBO_GUID,AFILEID,AFILEOFFSET,COMMCELLNO,MODIFIEDTIME,SIZEINKB,BACKUPTIME,CISTATE,DATE_DELETED,TEAMS_ITEM_ID,TEAMS_ITEM_NAME,TEAMS_NAME,TEAMS_SMTP,TEAMS_ITEM_TYPE,TEAMS_CHANNEL_TYPE,TEAMS_TAB_TYPE,TEAMS_GROUP_VISIBILITY,TEAMS_GUID,TEAMS_CONV_ITEM_TYPE,TEAMS_CONV_MESSAGE_TYPE,TEAMS_CONV_SUBJECT,TEAMS_CONV_IMPORTANCE,TEAMS_CONV_SENDER_TYPE,TEAMS_CONV_SENDER_NAME,TEAMS_CONV_HAS_REPLIES,CI_URL,TEAMS_DRIVE_FOLDER_TYPE,TEAMS_USER_ID"
                    },
                    {
                        "param": "DO_NOT_AUDIT",
                        "value": "false"
                    },
                    {
                        "param": "COLLAPSE_FIELD",
                        "value": "CV_OBJECT_GUID"
                    },
                    {
                        "param": "COLLAPSE_SORT",
                        "value": "BACKUPTIME DESC"
                    }
                ],
                "sortParams": [
                    {
                        "sortDirection": 0,
                        "sortField": "TEAMS_ITEM_NAME"
                    }
                ]
            }
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._TEAMS_BROWSE, _browse_req)

        return self._process_web_search_response(flag, response)

    def find_teams(self) -> (set, dict):
        """Find all files and their metadata within the Teams subclient.

        This method serves as an alternative to the `find()` method, specifically for Teams subclients.
        It locates all files and gathers their associated metadata.

        Returns:
            A tuple containing:
                - result_set: A set of all file paths found within the Teams subclient.
                - result_dict: A dictionary mapping each file path to its metadata.

        Example:
            >>> teams_subclient = TeamsSubclient()
            >>> file_set, file_metadata = teams_subclient.find_teams()
            >>> print(f"Found {len(file_set)} files in Teams subclient")
            >>> for file_path in file_set:
            ...     print(f"File: {file_path}, Metadata: {file_metadata[file_path]}")

        #ai-gen-doc
        """
        parent = ["00000000000000000000000000000001"]
        result_dict = {}
        result_set = set()
        while parent:
            p = parent.pop()
            items = self.do_web_search(parent_guid=p)
            for item in items:
                result_set.add(item["filePath"])
                result_dict[item["filePath"]] = item
                parent.append(item["cvObjectGuid"])

        return result_set, result_dict

    def preview_backedup_file(self, metadata: dict) -> str:
        """Retrieve the HTML preview content for a backed-up file in the subclient.

        Args:
            metadata: A dictionary containing metadata information required to locate and preview the backed-up file.

        Returns:
            The HTML content of the file preview as a string.

        Raises:
            SDKException: If the file is not found, the response is empty, or the response indicates failure.

        Example:
            >>> metadata = {
            ...     "file_path": "/Documents/Report.docx",
            ...     "version": "latest"
            ... }
            >>> html_content = teams_subclient.preview_backedup_file(metadata)
            >>> print(html_content)
            >>> # The output will be the HTML representation of the file's preview

        #ai-gen-doc
        """
        if metadata is None:
            raise SDKException('Subclient', '123')

        if metadata["dataType"] != 1:
            raise SDKException('Subclient', '124')

        if metadata["sizeKB"] == 0:
            raise SDKException('Subclient', '125')

        self._GET_VARIOUS_PREVIEW = self._services['GET_VARIOUS_PREVIEW']
        item_path_base_64 = base64.b64encode(metadata["filePath"].encode()).decode()
        request_json = {
            "filters": [
                {
                    "field": "APP_TYPE",
                    "fieldValues": {
                        "values": [
                            "200128"
                        ]
                    }
                },
                {
                    "field": "SUBCLIENT_ID",
                    "fieldValues": {
                        "values": [
                            str(self.subclient_id)
                        ]
                    }
                },
                {
                    "field": "CONTENTID",
                    "fieldValues": {
                        "values": [
                            metadata["documentId"]
                        ]
                    }
                },
                {
                    "field": "ARCHIVE_FILE_ID",
                    "fieldValues": {
                        "values": [
                            str(metadata["aFileId"])

                        ]
                    }
                },
                {
                    "field": "ARCHIVE_FILE_OFFSET",
                    "fieldValues": {
                        "values": [
                            str(metadata["aFileOffset"])
                        ]
                    }
                },
                {
                    "field": "COMMCELL_ID",
                    "fieldValues": {
                        "values": [
                            str(metadata["commcellNo"])
                        ]
                    }
                },
                {
                    "field": "CV_TURBO_GUID",
                    "fieldValues": {
                        "values": [
                            metadata["turboGuid"]
                        ]
                    }
                },
                {
                    "field": "ITEM_SIZE",
                    "fieldValues": {
                        "values": [
                            str(metadata["sizeKB"])
                        ]
                    }
                },
                {
                    "field": "ITEM_PATH_BASE64_ENCODED",
                    "fieldValues": {
                        "values": [
                            item_path_base_64
                        ]
                    }
                }

            ]
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._GET_VARIOUS_PREVIEW, request_json)

        if flag:
            if "Preview not available" not in response.text:
                return response.text
            else:
                raise SDKException('Subclient', '127')
        else:
            raise SDKException('Subclient', '102', self._update_response_(response.text))

    def run_restore_for_chat_to_onedrive(self, user_email: str) -> 'Job':
        """Run a restore operation for Teams chat data to the user's OneDrive.

        Args:
            user_email: The email address of the user whose Teams chat data should be restored to OneDrive.

        Returns:
            Job: An instance representing the restore job that was initiated.

        Example:
            >>> subclient = TeamsSubclient()
            >>> restore_job = subclient.run_restore_for_chat_to_onedrive("user@example.com")
            >>> print(f"Restore job started with ID: {restore_job.job_id}")

        #ai-gen-doc
        """
        discovered_teams = self.discover(discovery_type=const.ClOUD_APP_EDISCOVER_TYPE['Users'])
        if user_email not in discovered_teams:
            raise SDKException('Subclient', '102', f"User {user_email} not found in discovered teams")
        source_user = discovered_teams[user_email]
        request_json = copy(const.USER_ONEDRIVE_RESTORE_JSON)
        request_json["taskInfo"]["associations"] = [self._subClientEntity]
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]['selectedItemsToRestore'] = [{
            "itemId": source_user['user']['userGUID'].lower(),
            "itemType": 50,
            "isDirectory": True,
            "entityGUID": source_user['user']['userGUID'].lower()
        }]

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]['destLocation'] = f"{source_user['displayName']}/"
        destionation_onedrive_info = copy(const.DESTINATION_ONEDRIVE_INFO)
        destionation_onedrive_info['userSMTP'] = source_user['smtpAddress']
        destionation_onedrive_info['userGUID'] = source_user['user']['userGUID']
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'cloudAppsRestoreOptions']["msTeamsRestoreOptions"]['destinationOneDriveInfo'] = destionation_onedrive_info
        request_json['taskInfo']['subTasks'][0]["options"]["restoreOptions"]["destination"]["destPath"] = \
            [source_user['displayName'] + "/"]
        request_json['taskInfo']['subTasks'][0]["options"]["restoreOptions"]["destination"]["destClient"] = {
            "clientId": self._subClientEntity['clientId'],
            "clientName": self._subClientEntity['displayName']
        }
        request_json['taskInfo']['subTasks'][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"] \
            ["msTeamsRestoreOptions"]["findQuery"]["advSearchGrp"]["galaxyFilter"] = \
            [{"appIdList": [self._subClientEntity["subclientId"]]}]

        url = self._services['CREATE_TASK']
        flag, response = self._cvpysdk_object.make_request('POST', url, request_json)

        if flag:
            response_json = response.json()
            if response_json:
                if 'jobIds' in response_json:
                    return Job(self._commcell_object, response_json['jobIds'][0])

                elif "errorCode" in response_json:
                    error_message = response_json['errorMessage']

            raise SDKException('Response', '102')

        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)
