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
    File for operating on a Dynamics 365 CRM Subclient.

MSDynamics365Subclient is the only class defined in this file.

MSDynamics365Subclient:             Derived class from CloudAppsSubclient Base class, representing a
                                    Dynamics 365 subclient, and to perform operations on that subclient

MSDynamics365Subclient:

    *****************                       Methods                      *****************

    _get_subclient_properties()             --  gets the properties of MS Dynamics 365 Subclient

    _get_subclient_properties_json()        --  gets the properties JSON of MS Dynamics 365 Subclient

    get_discovered_tables()                 --  Method to run a discovery for tables and get them
    get_discovered_environments()           --  Method to run a discovery for environments and return them
    _get_associated_content()               --  Get content associated with a Dynamics 365 subclient
    get_associated_tables()                 --  Get list of associated tables
    get_associated_environments()           --  Get list of associated environments
    associate_tables()                      --  Associate tables to a Dynamics 365 subclient
    associate_environment()                 --  Associate list of environments to the sub   client
    backup_tables()                         --  Backup the specified tables
    backup_environments()                   --  Backup the specified environments
    restore_in_place()                      --  Run in-place restore for the specified content


    *****************                       Properties                      *****************

    discovered_environments                 --  Dictionary of environments discovered by the subclient
    discovered_tables                       --  Dictionary of tables discovered by the subclient

"""

from ...exception import SDKException

from ..casubclient import CloudAppsSubclient


class MSDynamics365Subclient(CloudAppsSubclient):
    """
        Class representing a MS Dynamics 365 subclient.
            Class has been derived from the CloudAppsSubclient.
    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Subclient object for the given MSDynamics365 Subclient.

            Args:
                backupset_object    (object)    --  instance of the backup-set class

                subclient_name      (str)       --  subclient name

                subclient_id        (int)       --  subclient id

        """
        super(MSDynamics365Subclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

        self._instance_object = backupset_object._instance_object
        self._client_object = self._instance_object._agent_object._client_object
        self._associated_tables: dict = dict()
        self._associated_environments: dict = dict()
        self._discovered_environments: dict = dict()
        self._discovered_tables: dict = dict()
        self._instance_type: int = 35
        self._app_id: int = 134
        # App ID for cloud apps
        self._Dynamics365_SET_USER_POLICY_ASSOCIATION = self._commcell_object._services['SET_USER_POLICY_ASSOCIATION']

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of a MS Dynamics 365 subclient"""
        super(MSDynamics365Subclient, self)._get_subclient_properties()

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """

        return {'subClientProperties': self._subclient_properties}

    def discover_tables(self):
        """
            Method to get the tables discovered from the MS Dynamics 365 CRM subclient

            Returns:
                discovered_tables       (dict)--    Dictionary of returned tables

        """
        self._discovered_tables = self._instance_object.discover_content(environment_discovery=False)
        return self._discovered_tables

    def discover_environments(self):
        """
            Method to get the environments discovered from the Dynamics 365 CRM subclient

            Returns:
                discovered_environments       (dict)--    Dictionary of discovered environments

        """
        self._discovered_environments = self._instance_object.discover_content(environment_discovery=True)
        return self._discovered_environments

    @property
    def discovered_environments(self):
        """
            Property to get the environments discovered by the Dynamics 365 subclient.

            If updated list is required, call refresh method prior to using this property.

            Returns:
                discovered_environments       (dict)--    Dictionary of discovered environments
        """
        if not bool(self._discovered_environments):
            self.discover_environments()
        return self._discovered_environments

    @property
    def discovered_tables(self):
        """
            Property to get the tables discovered by the Dynamics 365 subclient.

            If updated list is required, call refresh method prior to using this property.

            Returns:
                discovered_tables      (dict)--    Dictionary of discovered tables
        """
        if not bool(self._discovered_tables):
            self.discover_tables()
        return self._discovered_tables

    def _get_associated_content(self, is_environment=False):
        """
            Method to get the content associated with a Dynamics 365 CRM subclient

            Arguments:
                is_environment      (bool)--    Whether to get the associated environments or tables
                    Default Value:
                        False
                            Returns the associated tables

            Returns:
                associated_content_list     (list)--    List of content associated with the client
                    Format:
                        Each list element will be a dictionary denoting that particular environment/ table
        """
        discover_by_type: int
        if is_environment is True:
            discover_by_type = 5
        else:
            discover_by_type = 14

        _GET_ASSOCIATED_CONTENT = self._services['USER_POLICY_ASSOCIATION']
        request_json = {
            "discoverByType": discover_by_type,
            "bIncludeDeleted": False,
            "cloudAppAssociation": {
                "subclientEntity": {
                    "subclientId": int(self.subclient_id)
                }
            }
        }
        flag, response = self._cvpysdk_object.make_request(
            'POST', _GET_ASSOCIATED_CONTENT, request_json
        )
        if flag:
            if response and response.json():
                no_of_records = int()
                if 'associations' in response.json():
                    no_of_records = response.json().get('associations', [])[0].get('pagingInfo', {}). \
                        get('totalRecords', -1)

                    associations = response.json().get('associations', [])
                    content_list = list()
                    if discover_by_type == 5:
                        for environment in associations:
                            environment_name = environment.get("groups", {}).get("name")
                            env_dict = {
                                "name": environment_name,
                                "id": environment.get("groups", {}).get("id"),
                                "userAccountInfo": environment.get("userAccountInfo", {}),
                                "plan": environment.get("plan", {}),
                                "is_environment": True
                            }
                            content_list.append(env_dict)

                    elif discover_by_type == 14:
                        for table in associations:
                            table_name = table.get("userAccountInfo", {}).get("displayName")
                            table_dict = {
                                "name": table_name.lower(),
                                "environment_name": table.get("userAccountInfo", {}).get("ParentWebGuid", "").lower(),
                                "userAccountInfo": table.get("userAccountInfo", {}),
                                "plan": table.get("plan", {}),
                                "is_environment": False
                            }
                            content_list.append(table_dict)
                    return content_list
                    # return content_list, no_of_records
            return {}, 0
        raise SDKException('Response', '101', self._update_response_(response.text))

    def get_associated_tables(self, refresh: bool = False):
        """
            Method to get the tables associated with a Dynamics 365 CRM client

            Arguments:
                refresh                     (bool)--    Whether to refresh the dictionary contents
                    If True
                        get associated environments, will fetch the latest associations and return them

            Returns:
                associated_tables     (list)--    List of tables associated with the client
                    Format:
                        Each list element will be a dictionary denoting that particular  table
                        Dictionary keys/ format will be:
                            name : name of the table
                            environment_name : name of the environment to which the table belongs to
                            plan: Dynamics 365 plan used for content association
                            is_environment: False for a Table
                            userAccountInfo:    Metadata info for that table

                    Sample Response:
                        {
                            'name': 'account',
                            'environment_name': 'sample-environment-name',
                            'userAccountInfo':
                                {
                                'aliasName': 'https://<org-url-name>.crm.dynamics.com/api/data/v9.1/account',
                                'displayName': 'Account,
                                'ParentWebGuid': 'org-environment-name',
                                'lastBackupJobRanTime': {'time': <last-backup-time>},
                                'IdxCollectionTime': {'time': <last-index-time>},
                                'user': {
                                    '_type_': 13,
                                     'userGUID': '<table-GUID>>'
                                     }
                                },
                            'plan': {
                                'planName': '<PLAN-NAME>', 'planId': <plan-id>},
                            'is_environment': False
                        }
                    Environment name/ URL in the sample response is for description purpose only

        """
        if refresh is True:
            self._associated_tables = self._get_associated_content(is_environment=False)
        return self._associated_tables

    def get_associated_environments(self, refresh: bool = False):
        """
            Method to get the environments associated with a Dynamics 365 CRM client

            Arguments:
                refresh                     (bool)--    Whether to refresh the dictionary contents
                    If True
                        get associated environments, will fetch the latest associations and return them

            Returns:
                associated_environments     (list)--    List of environments associated with the client
                    Format:
                        Each list element will be a dictionary denoting that particular environment
                        Dictionary keys/ format will be:
                            name :              name of the table
                            plan:               Dynamics 365 plan used for content association
                            is_environment:     True for an environment
                            userAccountInfo:    Metadata info for that environment

                    Sample Response:
                        {
                                'name': 'sample-environment-name',
                                'id': '<environment-ID>>',
                                'userAccountInfo':
                                {
                                    'aliasName': 'https://<org-url-name>.crm.dynamics.com',
                                    'itemType': 0,
                                    'ItemClassification': 0,
                                    'displayName': 'org-environment-display-name',
                                    'BackupSetId': 0,
                                    'isAutoDiscoveredUser': False,
                                    'lastBackupJobRanTime': 'time': <last-backup-time>,
                                    'IdxCollectionTime': {'time': <last-index-playback-time>},
                                    user': {
                                        '_type_': 13,
                                        'userGUID': '<env-GUID>'
                                        }
                                },
                                'plan': {'planName': '<name-of-plan>', 'planId': <id-of-plan>},
                                 'is_environment': True}

        """
        if refresh is True:
            self._associated_environments = self._get_associated_content(is_environment=True)
        return self._associated_environments

    def _set_association_json(self, is_environment: bool = False):
        """
            JSON to set the content association for a Dynamics 365 CRM client

            Arguments:
                is_environment      (bool):     Whether the content to be associated is an environment
                    Default Value:
                        False
            Returns:
                set_content_association_json    (dict)--    Content Association JSON
        """
        set_content_association_json = {"LaunchAutoDiscovery": is_environment,
                                        "cloudAppAssociation": {
                                            "accountStatus": 0,
                                            "cloudAppDiscoverinfo": {
                                                "userAccounts": [
                                                ],
                                                "groups": [],
                                                "discoverByType": 14 if is_environment is False else 15
                                            }
                                            , "subclientEntity": self._subClientEntity}}

        return set_content_association_json

    def _set_content_association(self, content_json: dict):
        """
            Method to associate some content to a Dynamics 365 CRM client...

            Arguments:
                content_json        (dict)--        Association JSON to be used for the content
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._Dynamics365_SET_USER_POLICY_ASSOCIATION, content_json
        )

        if flag:
            try:
                if response.json():
                    if response.json()['resp']['errorCode'] != 0:
                        error_message = response.json()['errorMessage']
                        output_string = 'Failed to Create Association for a Dynamics 365 CRM client\nError: "{0}"'
                        raise SDKException(
                            'Subclient', '102', output_string.format(error_message)
                        )
                    else:
                        self.refresh()
            except ValueError:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _table_association_info_json(self, tables_list: list):
        """
            Private Method to create the association JSON for associating tables
            to a Dynamics 365 CRM client.

            Arguments:
                tables_list     (list)--    List of tables to be associated to the content
                    List Format:
                        Each list element should be a tuple of the format:
                            ("environment_name","table_name")
                                environment_name is the name of the environment to which the table belongs to
                                table_name is the name of the table to be associated

            Returns:
                tables_info     (list)--    List of metadata info for the tables to be used for associating content
        """
        tables_info: list = list()
        _discovered_tables = self.discovered_tables

        if not bool(_discovered_tables):
            raise SDKException('Subclient', '101',
                               "Discovered Tables is Empty.")

        for _table in _discovered_tables:
            _table_name, _parent_env_name = _table["displayName"].lower(), _table["ParentWebGuid"].lower()
            try:
                if (_parent_env_name, _table_name) in tables_list:
                    _table_assoc_info = _table
                    _table_assoc_info["user.userGUID"] = _table.get("user").get("userGUID")
                    tables_info.append(_table_assoc_info)
            except TypeError:
                raise SDKException('Subclient', '101',
                                   "For Associating tables, content list should be a list of tuples")

        if len(tables_info) == 0:
            raise SDKException("Subclient", "101", "None of the input tables were in the list of discovered tables")

        return tables_info

    def set_table_associations(self, tables_list: list, plan_name: str = str()):
        """
            Method to add table associations
            to a Dynamics 365 CRM client.

            Arguments:
                tables_list     (list)--    List of tables to be associated to the content
                    List Format:
                        Each list element should be a tuple of the format:
                            ("environment_name","table_name")
                                environment_name is the name of the environment to which the table belongs to
                                table_name is the name of the table to be associated
                    Sample input:
                        [ ("testenv1" , "account") , ("testenv2","note") , ("testenv1","attachments")]

                plan_name       (str)--     Name of the Dynamics 365 Plan to be used for content association
        """

        plan_id = int(self._commcell_object.plans[plan_name.lower()])

        tables_info = self._table_association_info_json(tables_list=tables_list)

        _table_association_json = self._set_association_json(is_environment=False)
        _table_association_json["cloudAppAssociation"]["plan"] = {
            "planId": plan_id
        }
        _table_association_json["cloudAppAssociation"]["cloudAppDiscoverinfo"]["userAccounts"] = tables_info
        self._set_content_association(content_json=_table_association_json)

    def _environment_association_info_json(self, environments_name: list):
        """
            Method to create the association JSON for associating environments
            to a Dynamics 365 CRM client.

            Arguments:
                environments_name     (list)--    List of environments to be associated to the content
                    List Format:
                        Each list element should be a string of the name of the environment

            Returns:
                environments_info     (list)--    List of metadata info for the environments to
                                                    be used for associating content
        """
        environments_info: list = list()
        _discovered_envs = self.discovered_environments

        if not bool(_discovered_envs):
            raise SDKException('Subclient', '101',
                               "Discovered Environments List is Empty")

        for environment in _discovered_envs:
            if environment["displayName"] in environments_name:
                _env_assoc_info = environment
                _env_assoc_info["user.userGUID"] = environment.get("user").get("userGUID")
                _env_assoc_info["rawCommonFlag"] = environment.get("commonFlags", 0)

                environments_info.append(_env_assoc_info)

        if len(environments_info) == 0:
            raise SDKException("Subclient", "101",
                               "None of the input environments were in the list of discovered environments")

        return environments_info

    def set_environment_associations(self, environments_name: list, plan_name: str = str()):
        """
            Method to add environment associations
            to a Dynamics 365 CRM client.

            Arguments:
                environments_name     (list)--    List of environments to be associated to the content
                    List Format:
                        Each list element should be a string of the name of the environment
                    Sample Values:
                        ['testenv1' , 'testenv2', 'testenv3']

                plan_name       (str)--     Name of the Dynamics 365 Plan to be used for content association
        """
        environments_info: list = self._environment_association_info_json(environments_name=environments_name)

        if self._commcell_object.plans.has_plan(plan_name.lower()):
            plan_id = int(self._commcell_object.plans[plan_name.lower()])

        else:
            raise SDKException("Subclient", "101",
                               "Dynamics 365 Plan does not exist")

        _env_association_json = self._set_association_json(is_environment=True)
        _env_association_json["cloudAppAssociation"]["plan"] = {
            "planId": plan_id
        }
        _env_association_json["cloudAppAssociation"]["cloudAppDiscoverinfo"]["userAccounts"] = environments_info
        self._set_content_association(content_json=_env_association_json)

    def _json_for_backup_task(self, content_list: list, is_environment: bool = False):
        """
            Method to create the association JSON for backing up content for a Dynamics 365 subclient

            Arguments:
                content_list     (list)--    List of content to be backed up
                    List Format, if content to be backed up is tables:
                        Each list element should be a tuple of the format:
                            ("environment_name","table_name")
                                environment_name is the name of the environment to which the table belongs to
                                table_name is the name of the table to be backed up
                    List Format, if content to be associated is environments:
                        Each list element should be a string of the name of the environment

                is_environment  (bool)--    Content passed to be backed up is environment type content or table type

            Returns:
                _backup_task_json     (list)--    JSON for backing up the content
        """
        _backup_task_json = self._backup_json('Full', False, '')
        _sub_client_content_json = self._backup_content_json(content_list=content_list, is_environment=is_environment)

        backup_options = {
            'backupLevel': 2,  # Incremental
            'cloudAppOptions': {
                'userAccounts': _sub_client_content_json
            }
        }
        _backup_task_json['taskInfo']['subTasks'][0]['options']['backupOpts'] = backup_options
        return _backup_task_json

    def _backup_content_json(self, content_list: list, is_environment: bool = False):
        """
            Method to fetch the metadata properties for backing up content for a Dynamics 365 subclient

            Arguments:
                content_list     (list)--    List of content to be backed up
                    List Format, if content to be backed up is tables:
                        Each list element should be a tuple of the format:
                            ("environment_name","table_name")
                                environment_name is the name of the environment to which the table belongs to
                                table_name is the name of the table to be backed up
                    List Format, if content to be associated is environments:
                        Each list element should be a string of the name of the environment

                is_environment  (bool)--    Content passed to be backed up is environment type content or table type

            Returns:
                _bkp_content_json     (list)--    Metadata JSON for backing up that content
        """
        _bkp_content_json = list()

        if is_environment is True:
            for environment in self.get_associated_environments(refresh=True):
                if environment["name"] in content_list:
                    _env_bkp_info = environment["userAccountInfo"]
                    _bkp_content_json.append(_env_bkp_info)

        elif is_environment is False:
            for _table in self.get_associated_tables(refresh=True):
                _table_name, _parent_env_name = _table["name"].lower(), _table["environment_name"].lower()
                try:
                    if (_parent_env_name, _table_name) in content_list:
                        _table_bkp_info = _table["userAccountInfo"]
                        _bkp_content_json.append(_table_bkp_info)
                except TypeError:
                    raise SDKException('Subclient', '101',
                                       "For backing up tables, content list should be a list of tuples")

        return _bkp_content_json

    def _run_backup(self, backup_content: list, is_environment: bool = False):
        """
            Method to run backup for the content of a Dynamics 365 subclient

            Arguments:
                backup_content     (list)--    List of content to be backed up
                    List Format, if content to be backed up is tables:
                        Each list element should be a tuple of the format:
                            ("environment_name","table_name")
                                environment_name is the name of the environment to which the table belongs to
                                table_name is the name of the table to be backed up
                    List Format, if content to be associated is environments:
                        Each list element should be a string of the name of the environment

                is_environment  (bool)--    Content passed to be backed up is environment type content or table type

            Returns:
                backup_job          (Job)--     CVPySDK.Job class instance for that particular backup job
        """
        _backup_json = self._json_for_backup_task(content_list=backup_content, is_environment=is_environment)
        backup_endpoint = self._services['CREATE_TASK']

        flag, response = self._commcell_object._cvpysdk_object.make_request("POST", backup_endpoint, _backup_json)
        return self._process_backup_response(flag, response)

    def backup_tables(self, tables_list: list):
        """
            Method to run backup for the specified tables of a Dynamics 365 subclient

            Arguments:
                tables_list     (list)--    List of tables to be backed up
                    List Format
                        Each list element should be a tuple of the format:
                            ("environment_name","table_name")
                                environment_name is the name of the environment to which the table belongs to
                                table_name is the name of the table to be backed up

                    Sample input:
                        [ ("testenv1" , "account") , ("testenv2","note") , ("testenv1","attachments")]
            Returns:
                backup_job          (Job)--     CVPySDK.Job class instance for that particular backup job
        """
        return self._run_backup(backup_content=tables_list, is_environment=False)

    def backup_environments(self, environments_list: list):
        """
            Method to run backup for the specified environments of a Dynamics 365 subclient

            Arguments:
                environments_list     (list)--    List of environments to be backed up
                    List Format, for backing up specified environments:
                        Each list element should be a string of the name of the environment
                    Sample List:
                        ['testenv1','testenv2','testenv3']

            Returns:
                backup_job          (Job)--     CVPySDK.Job class instance for that particular backup job
        """
        return self._run_backup(backup_content=environments_list, is_environment=True)

    def _restore_content_json(self):
        """
            Restore JSON for restoring content for a Dynamics 365 subclient

            Returns:
                _restore_task_json          (dict)--    JSON to be used for running a restore task
        """
        _restore_task_json = {
            "taskInfo": {
                "associations": [self._subclient_properties['subClientEntity']],
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 2,
                    "policyType": 0
                },
                "subTasks": [
                    {
                        "subTask": {
                            "subTaskType": 3,
                            "operationType": 1001
                        },
                        "options": {
                            "restoreOptions": {
                                "browseOption": {
                                    "timeRange": {}
                                },
                                "commonOptions": {
                                    "skip": True,
                                    "overwriteFiles": False,
                                    "unconditionalOverwrite": False
                                },
                                "destination": {
                                    "destAppId": self._app_id,
                                    "inPlace": True,
                                    "destClient": {
                                        "clientId": int(self._client_object.client_id),
                                        "clientName": self._client_object.client_name
                                    },
                                    "destPath": []
                                },
                                "fileOption": {
                                    "sourceItem": list()
                                },
                                "cloudAppsRestoreOptions": {
                                    "instanceType": self._instance_type,
                                    "d365RestoreOptions": {
                                        "restoreAllMatching": False,
                                        "restoreToDynamics365": True,
                                        "overWriteItems": False,
                                        "destLocation": "",
                                        "restoreUsingFindQuery": False
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }
        return _restore_task_json

    def _get_restore_item_path(self, content_list: list, is_environment: bool = False):
        """
            Get the complete path of the content for running a restore job

            Arguments:
                content_list            (list)--        List of content ot be restored
                    If content is environment,
                        List format:
                            list of strings, with each string corresponding to the environments display name, in lower case

                    If content is tables:
                        List format:
                            list of tuples, with each tuple, of the form: "environment_name","table_name"
                                where environment name if the name of the environment to which the table belongs to
                        Sample input:
                            [ ("testenv1" , "account") , ("testenv2","note") , ("testenv1","attachments")]

                is_environment          (bool)--        Whether the content is environment or tables
            Returns:
                __restore_content_list  (list)--        List of complete path for running restore job for the specifiec content
        """
        __restore_content_list = list()

        if is_environment is True:
            for environment in self.get_associated_environments(refresh=True):
                if environment["name"] in content_list:
                    _restore_id = environment["id"]
                    __restore_content_list.append(_restore_id)

        elif is_environment is False:
            for _table in self.get_associated_tables(refresh=True):
                _table_name, _parent_env_name = _table["name"].lower(), _table["environment_name"].lower()
                try:
                    if (_parent_env_name, _table_name) in content_list:
                        _id = _table.get("userAccountInfo").get("smtpAddress").split('/')
                        _table_id = _id[-1]
                        _env_id = _id[-2]
                        _restore_id = f"{_env_id}/{_table_id}"
                        __restore_content_list.append(_restore_id)

                except TypeError:
                    raise SDKException('Subclient', '101',
                                       "For restoring the tables, content list should be a list of tuples")
        __restore_content_list = list(
            map(lambda _restore_id: f"/tenant/{_restore_id}", __restore_content_list)
        )
        return __restore_content_list

    def _prepare_in_place_restore_json(self,
                                       restore_content: list,
                                       restore_path: list = None,
                                       overwrite: bool = True,
                                       job_id: int = None,
                                       is_environment: bool = False
                                       ):
        """
            Method to prepare JSON/ Python dict for  in- place restore for the content specified.

            Arguments:
                restore_content         (str)--     List of the content to restore
                    If content is environment,
                        List format:
                            list of strings, with each string corresponding to the environments display name, in lower case

                    If content is tables:
                        List format:
                            list of tuples, with each tuple, of the form: "environment_name","table_name"
                                where environment name if the name of the environment to which the table belongs to
                        Sample input:
                            [ ("testenv1" , "account") , ("testenv2","note") , ("testenv1","attachments")]

                restore_path            (list)--    List of the paths of the items to restore
                    Instead of passing, the restore content, restore path can be passed
                    Restore path, is the path for each item, that is to be restored.
                        Path is returned by the browse operation

                is_environment          (bool)--    Whether to content to be restored is a table or an environment
                overwrite               (bool)--    Skip or overwrite content
                job_id                  (int)--     Job ID for point in time restores
            Returns:
                _restore_content_json   (dict)--    Python dict to be used for restore content request
        """
        _restore_content_json = self._restore_content_json()
        if restore_path is None:
            restore_path = self._get_restore_item_path(content_list=restore_content, is_environment=is_environment)

        _restore_content_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["fileOption"][
            "sourceItem"] = restore_path

        if job_id is not None:
            _job = self._commcell_object.job_controller.get(job_id)
            _restore_content_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["browseOption"]["timeRange"][
                "toTime"] = _job.end_timestamp

        if overwrite is True:
            _restore_content_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["commonOptions"]["overwriteFiles"] = True
            _restore_content_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["commonOptions"][
                "skip"] = False
            _restore_content_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["commonOptions"][
                "unconditionalOverwrite"] = True
            _restore_content_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["cloudAppsRestoreOptions"] \
                ["d365RestoreOptions"]["overWriteItems"] = True
        return _restore_content_json

    def restore_in_place(
            self,
            restore_content: list = None,
            restore_path: list = None,
            is_environment: bool = False,
            overwrite: bool = True,
            job_id: int = None):
        """
            Method to run in- place restore for the content specified.

            Arguments:
                restore_content         (str)--     List of the content to restore
                    If content is environment,
                        List format:
                            list of strings, with each string corresponding to the environments display name, in lower case
                        Sample Input:
                            [ 'testenv1' , 'testenv2' , 'testenv3' ]

                    If content is tables:
                        List format:
                            list of tuples, with each tuple, of the form: "environment_name","table_name"
                                where environment name if the name of the environment to which the table belongs to
                        Sample input:
                            [ ("testenv1" , "account") , ("testenv2","note") , ("testenv1","attachments")]

                restore_path            (list)--    List of the paths of the items to restore
                    Instead of passing, the restore content, restore path can be passed
                    Restore path, is the path for each item, that is to be restored.
                        Path is returned by the browse operation

                is_environment          (bool)--    Whether to content to be restored is a table or an environment
                overwrite               (bool)--    Skip or overwrite content
                job_id                  (int)--     Job ID for point in time restores
            Returns:
                restore_job             (job)--     Instance of CVPySDK.Job for the restore job
        """

        if restore_content is None and restore_path is None:
            raise SDKException("Subclient", "101", "Need to have either of restore content or restore path")

        _restore_json = self._prepare_in_place_restore_json(
            restore_content=restore_content,
            restore_path=restore_path,
            is_environment=is_environment,
            job_id=job_id,
            overwrite=overwrite)
        return self._process_restore_response(_restore_json)
