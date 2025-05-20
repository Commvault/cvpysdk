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

"""File for doing operations on an organization.

This module has classes defined for doing operations for organizations:

    #. Add a new organization

    #. Delete an organization

    #. Enabling Auth Code

    #. Disabling Auth Code

    #. Get Auth Code

    #. Get the list of plans associated with the organization

    #. Update the plans associated with the organization

    #. Update the default plan of the organization

    #. Enabling Operator role for a user

    #. Disabling Operator role for a user

This module now also supports remote operations added as part of Ring Routing project

    #. Enable fanout to view all organizations from associated service commcells

    #. Add new organization remotely to a service commcell

    #. Delete an organization in service commcell remotely

    #. Manage operators, tags of the organization remotely

Organizations
=============

    __init__(commcell_object)   --  initializes object of the Organizations class associated
    with the commcell

    __str__()                   --  returns all the organizations associated with the commcell

    __repr__()                  --  returns the string representation of an instance of this class

    __len__()                   --  returns the number of organizations configured on the Commcell

    __getitem__()               --  returns the name of the organization for the organization Id
    or the details for the given organization name

    _get_organizations()        --  returns all organizations added to the commcell

    _get_headers()              --  returns headers required for remote operations

    _get_fl_parameters()        --  Returns the fl parameters to be passed in the mongodb caching api call

    _get_sort_parameters()      --  Returns the sort parameters to be passed in the mongodb caching api call

    _get_fq_parameters()        --  Returns the fq parameters based on the fq list passed

    get_organizations_cache()   --  Gets all the organizations present in CommcellEntityCache DB.

    has_organization()          --  checks whether the organization with given name exists or not

    add()                       --  adds a new organization to the commcell

    add_remote_org()            --  adds a new organization to given service commcell

    get()                       --  returns Organization class object for the specified input name

    get_remote_org()            --  returns RemoteOrganization class object for given input

    delete()                    --  deletes an organization from the commcell or service commcell

    dissociate_plans()          -- disassociates plans from the organization

    refresh()                   --  refresh the list of organizations in given commcell and/or service commcells

Organizations Attributes
------------------------

    **all_organizations**   --  returns the dict consisting of organizations and their details

    **all_organizations_props** -- returns the dict consisting of organizations and their guid's

    **fanout**              --  determines if remote operations will be performed, returns current fanout set

    **all_organizations_cache** --  Returns the dictionary consisting of all the organizations cache present in mongoDB

Organization
============

    __init__()                  --  initializes instance of the Organization class for doing
    operations on the selected Organization

    __repr__()                  --  returns the string representation of an instance of this class

    _get_organization_id()      --  gets the ID of the Organization

    _get_properties()           --  get the properties of the organization

    _get_company_usergroup()    --  get usergroups associated to a organization

    get_security_associations() --  get the security associations for a organization

    _update_properties()        --  update the properties of the organization

    _update_properties_json()   --  update the values of organizationProperties tag
    in the properties JSON

    refresh()                   --  refresh the properties of the organization

    enable_auth_code()          --  enable Auth Code generation for the organization

    disable_auth_code()         --  disable Auth Code generation for the organization

    add_users_as_operator()     --  assigns users as operator

    add_user_groups_as_operator()   -- assigns user groups as operator

    activate()                  --  To activate the organization

    deactivate()                --  To deactivate the organization

    verify_owner_assignment_config() --  Verifies that the ownership assignments settings are configured
    and set properly for company

    enable_auto_discover()      --  Enable autodiscover option for the oraganization

    disable_auto_discover()      --  Diable autodiscover option for the oraganization

    add_service_commcell_associations() -- Adds the organization association on service commcell

    remove_service_commcell_associations()-- Removes the orgainization association on service commcell

    enable_tfa()                --      Enable tfa option for the organization

    disable_tfa()               --      Disable tfa option for the organization

    get_alerts()                --  get all the alerts associated to organization

    add_client_association()        --  Associates a client to an organization

    remove_client_association()     --  Removes the client from an organization

    enable_company_data_privacy()   -- enable company privacy to prevent admin access to company data

    disable_company_data_privacy()  -- To disable company privacy to prevent admin access to company data

    enable_owner_data_privacy()     -- To enable company privacy to allow owner to enable data privacy

    disable_owner_data_privacy()    -- To disable company privacy to allow owner to enable data privacy

    update_security_associations()     -- Updates Security Associations for user or usergroup on Organisation

    update_email_settings()            -- Updates Email settings for the organisation

    retire_offline_laptops()           -- Updates Company Laptops Retire / Delete settings

    passkey()                          -- Handles Enable / Disable / Authorise / Change Passkey functionalities for Organisation

    allow_owners_to_enable_passkey()   -- Enables option to allow owners to enable / disable passkey

Organization Attributes
-----------------------

    Following attributes are available for an instance of the Organization class:

        **organization_id**         --  returns the id of the organization

        **organization_name**       --  returns the name of the organization

        **description**             --  returns the description for the organization

        **email_domain_names**      --  returns the list of email domain names associated with the
        organization

        **domain_name**             --  returns the primary domain associated with the organization

        **auth_code**               --  returns the Auth Code for the Organization, if enabled

        **is_auth_code_enabled**    --  returns boolean specifying whether Auth Code is enabled
        for the organization or not

        **machine_count**           --  returns the count of machines associated with the
        organization

        **user_count**              --  returns the count of users associated with the organization

        **contacts**                --  returns the list of primary contacts for the organization

        **sender_name**             -- returns email sender name

        **sender_email**            -- returns email adress of sender

        **default_plan**            --  returns the default plan associated with the organization

        **plans**                   --  returns the list of plans associated with the organization

        **operator_role**           -- returns the operator role assigned to an user

        **tenant_operator**         -- returns the operators associated with the organization

        **is_auto_discover_enabled**-- returns the autodiscover option for the Organization

        **is_backup_disabled**      -- returns the backup activity status for the Organization

        **is_restore_disabled**     -- returns the restore activity status for the Organization

        **is_login_disabled**       -- returns the Login activity status for the Organization

        **password_age_days**       -- returns the password age days for the Organization
        
        **is_download_software_from_internet_enabled**  --  returns the status of download software option for the Organization

        **is_tfa_enabled**          -- returns the status of tfa for the organization.

        **tfa_enabled_user_groups** --  returns list of user groups names for which tfa is enabled.

         **is_using_upn**           -- returns if organization is using upn or not

         **reseller_enabled**       -- returns if reseller is enabled or not

         **is_data_encryption_enabled**-- returns if owners are allowed to enable data encryption

         **infrastructure_type**    -- returns infrastructure associated with a organization

         **auto_laptop_owners_enabled**-- returns if laptop owners are assigned automatically for an organization

         **supported_solutions**    -- returns the supported solutions for an organization

         **job_start_time**         -- returns the job start time associated with the organization

        **client_groups**           -- returns clientgroups associated with the organization

        **file_exceptions**         -- returns dictionary consisting Global File exceptions for the Organisation

        **sites**                   -- Returns Sites configured for Organisation

        **tags**                    -- Returns Tags associated with Organisation

        **isPasskeyEnabled**        -- Returns True - If Passkey is enabled at Organisation level

        **isAuthrestoreEnabled**    -- Returns True - If Authrestore is enabled at Organisation level

        **isAllowUserstoEnablePasskeyEnabled** -- Returns True - If users have rights to enable passkey

        **is_company_privacy_enabled**         -- Returns True if the privacy is enabled for organization

        **is_owner_data_privacy_enabled**      -- Returns True if the privacy is enabled for owner of client in
        organization

        **company_theme**           --  Returns the company level theme if it exists

        **user_session_timeout**    --  Returns the time after which user session expires for company users

        **geo_info**                --  returns the regions this org is extended to

        **provder_guid**            --  returns the GUID for this organization

RemoteOrganization
============

    __init__()                  --  initializes instance of the RemoteOrganization class for doing
    remote operations on the selected Organization

    __repr__()                  --  returns the string representation of an instance of this class

    _get_organization_id()      --  gets the local ID of the RemoteOrganization

    _get_properties()           --  get the properties of the organization by fanout

    refresh()                   --  refresh the properties of the organization

    activate()                  --  To activate the organization

    deactivate()                --  To deactivate the organization
    
    get_entity_counts()         --  To get the counts of associated entities for company


RemoteOrganization Attributes
-----------------------

    Following attributes are available for an instance of the RemoteOrganization class:

        **organization_id**         --  returns the local id of the organization

        **organization_name**       --  returns the name of the organization

        **homecell**                --  returns the commserve name of the service commcell of this org

        **workloads**               --  returns the commcells this org is present in

        **geo_info**                --  returns the regions this org is extended to

        **provder_guid**            --  returns the GUID for this organization

        **organization_name**       --  returns the name of the organization

        **domain_name**             --  returns the primary domain associated with the organization (alias)

         **reseller_enabled**       -- returns if reseller is enabled or not

        **is_backup_disabled**       -- returns the backup activity status for the Organization

        **is_restore_disabled**      -- returns the restore activity status for the Organization

        **is_login_disabled**        -- returns the Login activity status for the Organization

        **tags**                    -- Returns Tags associated with Organisation

        **operators**               -- Returns Operators associated with this Organization

"""

import re
import json

from datetime import datetime

from .exception import SDKException
from .constants import ENTITY_TYPE_MAP
from .security.user import User
from .security.usergroup import UserGroup
from .security.two_factor_authentication import TwoFactorAuthentication

from base64 import b64encode


class Organizations:
    """Class for doing operations on Organizations like add / delete an organization, etc."""

    def __init__(self, commcell_object):
        """Initializes an instance of the Organizations class to perform operations on a company.

            Args:
                commcell_object     (object)    --  instance of the Commcell class

            Returns:
                object  -   instance of the Organizations class

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._organizations_api = self._services['ORGANIZATIONS']
        self._organizations = None
        self._organizations_cache = None
        self._fanout = False
        self.filter_query_count = 0

        self.refresh()

    def __str__(self):
        """Representation string consisting of all organizations present in the Commcell.

            Returns:
                str     -   string of all the organizations associated with the commcell

        """
        representation_string = '{:^5}\t{:^40}\n\n'.format('S. No.', 'Organization')

        for index, organization in enumerate(self._organizations):
            sub_str = '{:^5}\t{:40}\n'.format(index + 1, organization)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Returns the string representation of an instance of this class."""
        return "Organizations class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def __len__(self):
        """Returns the number of the organizations configured on the Commcell."""
        return len(self.all_organizations)

    def __getitem__(self, value):
        """Returns the name of the organization for the given organization ID or
            the details of the organization for given organization Name.

            Args:
                value   (str / int)     --  Name or ID of the organization

            Returns:
                str     -   name of the organization, if the organization id was given

                dict    -   dict of details of the organization, if organization name was given

            Raises:
                IndexError:
                    no organization exists with the given Name / Id

        """
        value = str(value)

        if value in self.all_organizations:
            return self.all_organizations[value]
        try:
            return list(
                filter(lambda x: x[1]['id'] == value, self.all_organizations.items())
            )[0][0]
        except IndexError:
            raise IndexError('No organization exists with the given Name / Id')

    def _get_organizations(self, full_response: bool = False):
        """Gets all the organizations associated with the Commcell environment.
            Args:
                full_response(bool) --  flag to return complete response
            Returns:
                dict    -   consists of all organizations added to the commcell

                    {
                        "organization1_name": organization1_id,

                        "organization2_name": organization2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._organizations_api, headers=self._get_headers())
        if flag:
            organizations = {}
            self._adv_config = {}
            if response.json() and 'providers' in response.json():
                if full_response:
                    return response.json()
                for provider in response.json()['providers']:
                    name = provider['connectName'].lower()
                    if self._fanout and "idpCompanyDetails" in provider:
                        marked_workloads = self._adv_config.get(name, {}).get('workloads', [])
                        this_workload = provider.get('commcell', {}).get('commCellName')
                        self._adv_config[name] = self._adv_config.get(name, {}) | {
                            'workloads': marked_workloads + [this_workload]
                        }
                        continue
                        # using dummy company to store workload commcells only
                    organization_id = provider['shortName']['id']
                    organization_guid = provider['providerGUID']
                    cloud_service_organizations = provider.get("organizationCloudServiceDetails", [{}])[0].\
                        get("cloudService", {}).get('redirectUrl')
                    organizations[name] = organization_id
                    self._adv_config[name] = self._adv_config.get(name, {}) | {
                        'id': organization_id,
                        'GUID': organization_guid,
                        'redirect_url': cloud_service_organizations,
                        'home_commcell': provider.get('commcell', {}).get('commCellName'),
                        'parent_company': provider.get('ownerCompanyName'),
                        'full_name': [contact.get('fullName','') for contact in provider.get('primaryContacts',[])],
                        'flags': provider.get('flags')
                    }
                    if 'workloads' not in self._adv_config[name]:
                        self._adv_config[name]['workloads'] = []

            self._get_associated_entities_count()

            return organizations
        response_string = self._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def _get_associated_entities_count(self):
        """Gets all the organizations associated with the Commcell environment.

            Returns:
                dict    -   consists of all organizations added to the commcell

                    {
                        "organization1_name": organization1_id,

                        "organization2_name": organization2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET',
            f"{self._organizations_api}?Fl=providers.associatedEntitiesCount,providers.shortName,providers.connectName",
            headers = self._get_headers()
        )

        if flag:
            if response.json() and 'providers' in response.json():
                for provider in response.json().get('providers'):
                    name = provider.get('connectName').lower()
                    organization_entites_count = provider.get('associatedEntitiesCount')
                    if name:
                        if name in self._adv_config.keys():
                            self._adv_config[name].update({'count': organization_entites_count})

                return
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_headers(self, target:str=None):
        """
        Returns fanout headers if fanout is set

        Args:
            target (str) -- target service commserve name (if applicable)
        """
        if not self._fanout:
            return None
        headers = self._commcell_object._headers.copy()
        headers['CVContext']='Comet'
        if target:
            headers['_cn'] = target
            headers['Comet-Commcells'] = target
        return headers

    def _get_fl_parameters(self, fl: list = None) -> str:
        """
        Returns the fl parameters to be passed in the mongodb caching api call

        Args:
            fl    (list)  --   list of columns to be passed in API request

        Returns:
            fl_parameters(str) -- fl parameter string
        """
        self.valid_columns = {
            'name': 'providers.connectName',
            'id': 'providers.shortname.id',
            'fullName': 'providers.primaryContacts.fullName',
            'associatedEntitiesCount': 'providers.associatedEntitiesCount',
            'status': 'providers.status',
            'providerGUID': 'providers.providerGUID',
            'tags': 'providers.provider.tags',
            'reseller': 'providers.canCreateCompanies',
            'parentCompany': 'providers.ownerCompanyName',
            'commcell': 'providers.commcell'
        }
        default_columns = 'providers.connectName,providers.shortName'

        if fl:
            if all(col in self.valid_columns for col in fl):
                fl_parameters = f"&fl={default_columns},{','.join(self.valid_columns[column] for column in fl)}"
            else:
                raise SDKException('Organization', '102', 'Invalid column name passed')
        else:
            fl_parameters = f"&fl={default_columns},{','.join(column for column in self.valid_columns.values())}"
        return fl_parameters

    def _get_sort_parameters(self, sort: list = None) -> str:
        """
        Returns the sort parameters to be passed in the mongodb caching api call

        Args:
            sort  (list)  --   contains the name of the column on which sorting will be performed and type of sort
                                valid sor type -- 1 for ascending and -1 for descending
                                e.g. sort = ['columnName','1']

        Returns:
            sort_parameters(str) -- sort parameter string
        """
        sort_type = str(sort[1])
        col = sort[0]
        if col in self.valid_columns.keys() and sort_type in ['1', '-1']:
            sort_parameter = '&sort=' + self.valid_columns[col] + ':' + sort_type
        else:
            raise SDKException('Organization', '102', 'Invalid column_name/ sort_type passed')
        return sort_parameter

    def _get_fq_parameters(self, fq: list = None) -> str:
        """
        Returns the fq parameters based on the fq list passed
        Args:
             fq     (list) --   contains the columnName, condition and value
                    e.g. fq = [['name','contains','test'],['status','eq','ACTIVE']]

        Returns:
            fq_parameters(str) -- fq parameter string
        """
        conditions = {"contains", "notContain", "eq", "neq", "gt", "lt", "nin"}
        params = []

        for column, condition, *value in fq or []:
            if column not in self.valid_columns:
                raise SDKException("Organization", "102", "Invalid column name passed")

            if column == "tags":
                params.append(f"&fq=providers.provider.tags.name:contains:{value[0]}")
            elif condition in conditions:
                params.append(f"&fq={self.valid_columns[column]}:{condition.lower()}:{value[0]}")
            elif condition == "isEmpty" and not value:
                params.append(f"&fq={self.valid_columns[column]}:in:null,")
            elif condition == "between" and "-" in value[0]:
                start, end = value[0].split("-")
                params.append(f"&fq={self.valid_columns[column]}:gteq:{start}")
                params.append(f"&fq={self.valid_columns[column]}:lteq:{end}")
            else:
                raise SDKException("Organization", "102", "Invalid condition passed")

        return "".join(params)

    def get_organizations_cache(self, hard: bool = False, **kwargs) -> dict:
        """
        Gets all the organizations present in CommcellEntityCache DB.

        Args:
            hard  (bool)      --   Flag to perform hard refresh on organization cache.
            **kwargs (dict):
                fl    (list)  --   list of columns to return in response (default: None).
                sort  (list)  --   contains the name of the column on which sorting will be performed and type of sort
                                        valid sor type: 1 for ascending and -1 for descending
                                        e.g. sort = ['name','1'] (default: None).
                limit (list)  --   contains the start and limit parameter value
                                        limit = [<startValue>,<limitValue>]
                                        default ['0','25']
                search (str)  --   contains the string to search in the commcell entity cache (default: None).
                fq     (list) --   contains the columnName, condition and value as a sublist of a list (default: None).
                                        e.g. fq = [['name','contains','test'],['status','equals','active']]

        Returns:
            dict: Dictionary of all the properties present in response.
        """
        # computing params
        fl_parameters = self._get_fl_parameters(kwargs.get('fl', None))
        fq_parameters = self._get_fq_parameters(kwargs.get('fq', None))
        limit = kwargs.get('limit', None)
        limit_parameters = f'start={limit[0]}&limit={limit[1]}' if limit else ''
        hard_refresh = '&hardRefresh=true' if hard else ''
        sort_parameters = self._get_sort_parameters(kwargs.get('sort', None)) if kwargs.get('sort', None) else ''

        # Search operation can only be performed on limited columns, so filtering out the columns on which search works
        searchable_columns = ["name", "fullName", "providerGUID", "status"]
        search_parameter = (f'&search={",".join(self.valid_columns[col] for col in searchable_columns)}:contains:'
                            f'{kwargs.get("search", None)}') if kwargs.get('search', None) else ''
        params = [
            limit_parameters,
            sort_parameters,
            fl_parameters,
            hard_refresh,
            search_parameter,
            fq_parameters
        ]

        # adding required additional param for comet layer
        if self._commcell_object.is_global_scope():
            params.append("&fq=providers.idpCompanyDetails:eq:null")

        request_url = f"{self._organizations_api}?" + "".join(params)
        flag, response = self._cvpysdk_object.make_request("GET", request_url)

        if not flag:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        organizations_cache = {}
        if response.json() and 'providers' in response.json():
            self.filter_query_count = response.json().get('filterQueryCount',0)
            for provider in response.json()['providers']:
                name = provider['connectName'].lower()
                organization_config = {
                    'name': provider['connectName'].lower(),
                    'id': provider.get('shortName', {}).get('id'),
                    'providerGUID': provider.get('providerGUID'),
                    'status': provider.get('status'),
                    'associatedEntitiesCount': provider.get('associatedEntitiesCount'),
                    'fullName':[contact.get('fullName','') for contact in provider.get('primaryContacts',[])],
                    'reseller': provider.get('canCreateCompanies', False),
                    'parentCompany': provider.get('ownerCompanyName', '')
                }
                if provider.get('provider') is not None and 'tags' in provider['provider']:
                    organization_config['tags'] = provider.get('provider', {}).get('tags')
                if self._commcell_object.is_global_scope():
                    organization_config.update(
                        {"commcell": provider.get('commcell', {}).get('entityInfo', {}).get('multiCommcellName','')}
                    )

                    # Handle duplicate names for different commcells
                    unique_name = name
                    i = 1
                    while unique_name in organizations_cache:
                        existing_user = organizations_cache[unique_name]
                        if existing_user.get('commcell') != organization_config.get('commcell'):
                            unique_name = f"{name}__{i}"
                            i += 1
                        else:
                            break
                    organizations_cache[unique_name] = organization_config
                else:
                    organizations_cache[name] = organization_config
            return organizations_cache
        else:
            raise SDKException('Response', '102')

    @property
    def all_organizations_cache(self):
        """Returns the dictionary consisting of all the organizations cache present in mongoDB

                    dict - consists of all the organizations configured on the commcell

                        {
                        "organization1_name":
                         {
                         id : <organization's id>,
                         domainName : <domain name of the organization>,
                         GUID : <GUID of the company>,
                         status: <status of the organization>,
                         associatedEntityCount: <associated Entities Count>
                         },

                        "organization2_name":
                        {
                         id : <organization's id>,
                         domainName : <domain name of the organization>,
                         GUID : <GUID of the company>,
                         status: <status of the organization>,
                         associatedEntityCount: <associated Entities Count>
                         },
                    }

                """
        if not self._organizations_cache:
            self._organizations_cache = self.get_organizations_cache()
        return self._organizations_cache

    @property
    def all_organizations(self):
        """Returns the dictionary consisting of all the organizations and their info.

            dict - consists of all the organizations configured on the commcell

                {
                    "organization1_name": organization1_id,

                    "organization2_name": organization2_id
                }

        """
        return self._organizations

    @property
    def all_organizations_props(self):
        """Returns the dictionary consisting of all the organizations guid info and redirect URL if present.

            dict - consists of all the organizations configured on the commcell and/or service commcells

                {
                    "organization1_name":
                     {
                     GUID : "49DADF71-247E-4D59-8BD8-CF7BFDF7DB28",
                     redirect_url: "<Webconsole url>",
                     home_commcell: "<commserve name>",
                     parent_company: "<company name>",
                     workloads: ['cs1', 'cs2']
                     count: 11
                     },

                    "organization2_name":
                    {
                    GUID : "49DADF71-247E-4D59-8BD8-CF7BFDF7DB27",
                    redirect_url: None,
                    home_commcell: "<commserve name>",
                    parent_company: "<company name>",
                    workloads: ['cs4']
                    count: 8
                    }
                }

        """
        return self._adv_config

    @property
    def fanout(self)->bool:
        """Returns status of fanout headers are enabled or not
        Returns:
            bool    -   True/False
        """
        return self._fanout

    @fanout.setter
    def fanout(self, value:bool=True):
        """
        Sets if fanout is required or not
        
        Args:
            value (bool) -- False if fanout not required
        """
        self._fanout = value
        self.refresh()

    def has_organization(self, name):
        """Checks if an organization exists in the Commcell with the input organization name.

            Args:
                name    (str)   --  name of the organization

            Returns:
                bool    -   boolean output whether the organization exists in the commcell or not

            Raises:
                SDKException:
                    if type of the organization name argument is not string

        """
        if not isinstance(name, str):
            raise SDKException('Organization', '101')

        return self._organizations and name.lower() in self._organizations

    def add_remote_org(self,
            name,
            email,
            contact_name,
            company_alias,
            **options):
        """Adds a new organization with the given name to the Commcell.

            Args:
                name            (str)   --  name of the organization to create

                email           (str)   --  email of the primary contact

                contact_name    (str)   --  name of the primary contact

                company_alias   (str)   --  alias of the company

                email_domain    (list)  --  list of email domains supported for the organization

                    if no value is given, domain of the user creating the organization will be used

                    default: None

                primary_domain  (str)   --  custom primary domain for organization

                    default: None

                default_plans   (list)  --  list of default plans to be associated with the
                organization

                    default: None

                send_email      (bool) --  If set to true, a welcome email is sent to the
                primary contact user.

                    default: False

                target          (str)   --  service commcell name where to add organization
                    
                    default: current commcell

            Returns:
                object  -   instance of the RemoteOrganization class

            Raises:
                SDKException:
                    if organization with the given name already exists

                    if inputs are not valid

                    if failed to create the organization remotely

                    if response is empty

                    if response is not success

        """
        if not self._fanout:
            raise Exception('Enable fanout property to perform remote operations')
        if self.has_organization(name):
            raise SDKException('RemoteOrganization', '108')

        if not (isinstance(name, str) and
                isinstance(email, str) and
                isinstance(contact_name, str) and
                isinstance(company_alias, str)):
            raise SDKException('RemoteOrganization', '105')

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            raise SDKException('RemoteOrganization', '107')

        email_domain=options.get('email_domain')
        primary_domain=options.get('primary_domain')
        default_plans=options.get('default_plans')
        enable_auto_discover=options.get('enable_auto_discover',False)
        send_email=options.get('send_email',False)
        target=options.get('target')

        if email_domain is None:
            email_domain = [email.split('@')[1]]

        if primary_domain is None:
            primary_domain = ''

        plans_list = []

        if default_plans:
            if not isinstance(default_plans, list):
                raise SDKException('RemoteOrganization', '105')
            else:
                for plan in default_plans:
                    if not self._commcell_object.plans.has_plan(plan):
                        raise SDKException(
                            'RemoteOrganization',
                            '106',
                            'Plan: "{0}" does not exist on Commcell'.format(plan)
                        )
                    else:
                        temp_plan = self._commcell_object.plans.get(plan)
                        temp = {
                            'plan': {
                                'planId': int(temp_plan.plan_id)
                            }
                        }
                        plans_list.append(temp)

                        del temp
                        del temp_plan

        request_json = {
            'organizationInfo': {
                'organization': {
                    'connectName': name,
                    'emailDomainNames': email_domain,
                    'shortName': {
                        'domainName': company_alias
                    }
                },
                'organizationProperties': {
                    'enableAutoDiscovery': enable_auto_discover,
                    'primaryDomain': primary_domain,
                    'primaryContacts': [
                        {
                            'fullName': contact_name,
                            'email': email
                        }
                    ],
                },
                'planDetails': plans_list
            }
        }

        send_email and request_json.update({'sendEmail': send_email})

        if target is None:
            target = self._commcell_object.commserv_name
        __, response = self._cvpysdk_object.make_request(
            'POST', self._organizations_api, request_json, headers=self._get_headers(target)
        )

        self.refresh()

        if response.json():
            if 'response' in response.json():
                error_code = response.json()['response']['errorCode']

                if error_code == 0:
                    return self.get_remote_org(name)

                raise SDKException(
                    'RemoteOrganization', '109', 'Response: {0}'.format(response.json())
                )

            elif 'errorMessage' in response.json():
                raise SDKException(
                    'RemoteOrganization', '109', 'Error: "{0}"'.format(response.json()['errorMessage'])
                )

            else:
                raise SDKException('RemoteOrganization', '109', 'Response: {0}'.format(response.json()))
        else:
            raise SDKException('Response', '102')

    def add(self,
            name,
            email,
            contact_name,
            company_alias,
            email_domain=None,
            primary_domain=None,
            default_plans=None,
            enable_auto_discover=False,
            service_commcells=None,
            send_email=False):
        """Adds a new organization with the given name to the Commcell.

            Args:
                name            (str)   --  name of the organization to create

                email           (str)   --  email of the primary contact

                contact_name    (str)   --  name of the primary contact

                company_alias   (str)   --  alias of the company

                email_domain    (list)  --  list of email domains supported for the organization

                    if no value is given, domain of the user creating the organization will be used

                    default: None

                primary_domain  (str)   --  custom primary domain for organization

                    default: None

                default_plans   (list)  --  list of default plans to be associated with the
                organization

                    default: None

                service_commcells (list) -- list of service commmcells to be associated with the
                organization

                    default: None

                send_email      (bool) --  If set to true, a welcome email is sent to the
                primary contact user.

                    default: False

            Returns:
                object  -   instance of the Organization class, for the newly created organization

            Raises:
                SDKException:
                    if organization with the given name already exists

                    if inputs are not valid

                    if failed to create the organization

                    if response is empty

                    if response is not success

        """
        if self.has_organization(name):
            raise SDKException('Organization', '106')

        if not (isinstance(name, str) and
                isinstance(email, str) and
                isinstance(contact_name, str) and
                isinstance(company_alias, str)):
            raise SDKException('Organization', '101')

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            raise SDKException('Organization', '105')

        if email_domain is None:
            email_domain = [email.split('@')[1]]

        if primary_domain is None:
            primary_domain = ''

        plans_list = []

        if service_commcells:
            if not isinstance(service_commcells, list):
                raise SDKException('Organization', '101')
        if default_plans:
            if not isinstance(default_plans, list):
                raise SDKException('Organization', '101')
            else:
                for plan in default_plans:
                    if not self._commcell_object.plans.has_plan(plan):
                        raise SDKException(
                            'Organization',
                            '102',
                            'Plan: "{0}" does not exist on Commcell'.format(plan)
                        )
                    else:
                        temp_plan = self._commcell_object.plans.get(plan)
                        temp = {
                            'plan': {
                                'planId': int(temp_plan.plan_id)
                            }
                        }
                        plans_list.append(temp)

                        del temp
                        del temp_plan

        request_json = {
            'organizationInfo': {
                'organization': {
                    'connectName': name,
                    'emailDomainNames': email_domain,
                    'shortName': {
                        'domainName': company_alias
                    }
                },
                'organizationProperties': {
                    'enableAutoDiscovery': enable_auto_discover,
                    'primaryDomain': primary_domain,
                    'primaryContacts': [
                        {
                            'fullName': contact_name,
                            'email': email
                        }
                    ],
                },
                'planDetails': plans_list
            }
        }

        send_email and request_json.update({'sendEmail': send_email})

        __, response = self._cvpysdk_object.make_request(
            'POST', self._organizations_api, request_json
        )

        self.refresh()

        if response.json():
            if 'response' in response.json():
                error_code = response.json()['response']['errorCode']

                if error_code == 0:
                    org_object = self.get(name)
                    if service_commcells:
                        for servicecommcell in service_commcells:
                            org_object.add_service_commcell_associations(name=name, service_commcell=servicecommcell)

                    return self.get(name)

                raise SDKException(
                    'Organization', '107', 'Response: {0}'.format(response.json())
                )

            elif 'errorMessage' in response.json():
                raise SDKException(
                    'Organization', '107', 'Error: "{0}"'.format(response.json()['errorMessage'])
                )

            else:
                raise SDKException('Organization', '107', 'Response: {0}'.format(response.json()))
        else:
            raise SDKException('Response', '102')

    def get(self, name):
        """Returns an instance of the Organization class for the given organization name.

            Args:
                name    (str)   --  name of the organization to get the instance of

            Returns:
                object  -   instance of the Organization class for the given organization name

            Raises:
                SDKException:
                    if type of the organization name argument is not string

                    if no organization exists with the given name

        """
        if not isinstance(name, str):
            raise SDKException('Organization', '101')

        name = name.lower()

        if self.has_organization(name):
            return Organization(self._commcell_object, name, self._organizations[name])
        raise SDKException('Organization', '103')

    def get_remote_org(self, name):
        """Returns an instance of the RemoteOrganization class for the given organization name.

            Args:
                name    (str)   --  name of the remote organization to get the instance of

            Returns:
                object  -   instance of the RemoteOrganization class for the given organization name

            Raises:
                SDKException:
                    if type of the organization name argument is not string

                    if no organization exists with the given name

        """
        if not self._fanout:
            raise Exception('Enable fanout property to perform remote operations')
        if not isinstance(name, str):
            raise SDKException('RemoteOrganization', '105')

        name = name.lower()

        if self.has_organization(name):
            return RemoteOrganization(
                self._commcell_object,
                name,
                self._organizations[name],
                homecell=self._adv_config[name]['home_commcell'],
                workloads=self._adv_config[name]['workloads']
            )
        raise SDKException('RemoteOrganization', '110')

    def delete(self, name, deactivate=True):
        """Deletes the organization with the given name from the Commcell.

            Args:
                name            (str)   --  name of the organization to delete
                deactivate      (bool)   -- Whether to deactivate organization before deleting, By default organization will be deactivated

            Returns:
                None    -   if the organization was removed successfully

            Raises:
                SDKException:
                    if organization with the given name does not exists

                    if failed to delete the organization

                    if response is empty

                    if response is not success

        """
        if not self.has_organization(name):
            raise SDKException('Organization', '103')

        if self._fanout:
            org = self.get_remote_org(name)
            target = org.homecell
        else:
            org = self.get(name)
            target = None

        if deactivate: org.deactivate()

        organization_id = self._organizations[name.lower()]

        flag, response = self._cvpysdk_object.make_request(
            'DELETE', self._services['ORGANIZATION'] % organization_id, headers=self._get_headers(target)
        )

        self.refresh()

        if flag:
            if response.json():
                error_message = response.json()['errorMessage']
                error_code = response.json()['errorCode']

                if error_code != 0:
                    raise SDKException('Organization', '104', 'Error: "{0}"'.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self, **kwargs):
        """
        Refresh the list of organization on this commcell.

            Args:
                **kwargs (dict):
                    mongodb (bool)  -- Flag to fetch organization cache from MongoDB (default: False).
                    hard (bool)     -- Flag to hard refresh MongoDB cache for this entity (default: False).
        """
        mongodb = kwargs.get('mongodb', False)
        hard = kwargs.get('hard', False)

        self._adv_config = None
        self._organizations = self._get_organizations()
        if mongodb:
            self._organizations_cache = self.get_organizations_cache(hard=hard)


class Organization:
    """Class for performing operations on an Organization."""

    def __init__(self, commcell_object, organization_name, organization_id=None):
        """Initialise the Client class instance.

            Args:
                commcell_object     (object)    --  instance of the Commcell class

                organization_name   (str)       --  name of the organization

                organization_id     (str)       --  id of the organization
                    default: None

            Returns:
                object  -   instance of the Organization class

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._organization_name = organization_name

        if organization_id:
            self._organization_id = str(organization_id)
        else:
            self._organization_id = self._get_organization_id()

        self._properties = {}

        self._description = None
        self._email_domain_names = None
        self._domain_name = None
        self._auth_code = None
        self._is_auth_code_enabled = False
        self._machine_count = None
        self._user_count = None
        self._default_plan = []
        self._contacts = {}
        self._plans = {}
        self._organization_info = None
        self._operator_role = None
        self._operators = None
        self._plan_details = None
        self._server_count = None
        self._user_groups = None
        self._sender_email = None
        self._sender_name = None
        self._supported_solutions = None
        self._org_creation_time = None
        self._use_upn = None
        self._reseller_enabled = None
        self._is_data_encryption_enabled = None
        self._infrastructure_type = None
        self._auto_laptop_owners = None
        self._file_exceptions = {}
        self._global_file_exceptions_enabled = False
        self._job_start_time = None
        self._client_groups = None
        self._update_props = {}
        self._primary_domain = None
        self._additional_domain = None
        self._is_passkey_enabled = None
        self._is_authorise_for_restore_enabled = None
        self._is_allow_users_to_enable_passkey_enabled = None
        self._company_privacy = None
        self._owner_privacy = None
        self._backup_disabled = None
        self._restore_disabled = None
        self._login_disabled = None
        self._retire_laptops = None
        self._password_age = None
        self._download_software_from_internet = None
        self._session_timeout = None
        self._tfa_obj = TwoFactorAuthentication(self._commcell_object, organization_id=self._organization_id)
        self.refresh()

    @property
    def is_using_upn(self):
        """ Returns if company uses UPN instead of Email """
        return self._use_upn

    @is_using_upn.setter
    def is_using_upn(self, value):
        """ Sets company to use UPN instead of Email """
        self._update_properties_json({'useUPNForEmail': value})
        self._update_properties()

    @property
    def reseller_enabled(self):
        """ Returns if reseller is enabled """
        return self._reseller_enabled

    @reseller_enabled.setter
    def reseller_enabled(self, value):
        """ Sets the reseller mode for a company"""
        self._update_properties_json({'canCreateCompanies': value})
        self._update_properties()

    @property
    def is_data_encryption_enabled(self):
        """ Returns if owners are allowed to enable data encryption"""
        return self._is_data_encryption_enabled

    def set_data_encryption_enabled(self, value):
        """ Sets property to allow owners to enable data encryption """
        self._update_properties_json({'showDLP': value})
        self._update_properties()

    @property
    def infrastructure_type(self):
        """ Returns infrastructure type """
        return self._infrastructure_type

    @infrastructure_type.setter
    def infrastructure_type(self, value):
        """ Sets infrastruture type for a comapny

        Args:
            value (int) -- id for the infrastructure type

            Rented storage = 0,
            Own Storage = 1,
            Rented and Own Storage  = 2
        """
        self._update_properties_json({'infrastructureType': value})
        self._update_properties()

    @property
    def auto_laptop_owners_enabled(self):
        """ Returns if laptop owners are assigned automatically """
        return True if self._auto_laptop_owners else False

    def set_auto_laptop_owners(self, client_assign_type, client_assign_value=None):
        """ Sets the property in company to assign owners to laptop automatically

        Args:
            client_assign_type (int): client owner assignment type
            client_assign_value (str): client owner assignment value
        """
        if client_assign_type == 3:
            self._update_properties_json({'autoClientOwnerAssignmentType': client_assign_type,
                                          'autoClientOwnerAssignmentValue': client_assign_value})
        else:
            self._update_properties_json({'autoClientOwnerAssignmentType': client_assign_type})

        self._update_properties()

    @property
    def supported_solutions(self):
        """ Returns the supported solutions
        supported solution from API is a integer value and it needs to be changed to a list
        """
        return self._supported_solutions

    @supported_solutions.setter
    def supported_solutions(self, value):
        """Sets the supported solution property of a company

        Args:
            value (int) -- bits converted to int for the supported solutions
        """
        self._update_properties_json({'supportedSolutions': value})
        self._update_properties()

    @property
    def job_start_time(self):
        """ Returns the job start time for a company or 'System default' if not set """
        return self._job_start_time

    @job_start_time.setter
    def job_start_time(self, value):
        """Sets the job start time property for a company

        Args:
            value (int) -- time to be set for job start time for a company
        """
        self._update_properties_json({'jobStartTime': value})
        self._update_properties()

    def __repr__(self):
        """Returns the string representation of an instance of this class."""
        return 'Organization class instance for Organization: "{0}"'.format(self.organization_name)

    def _get_organization_id(self):
        """Gets the id associated with this organization.

            Returns:
                str     -   id associated with this organization

        """
        organizations = Organizations(self._commcell_object)
        return organizations.get(self.organization_name).organization_id

    def _get_properties(self, **params):
        """Gets the properties of this Organization.
        
            Args:
                params  (dict)  --  dictionary of query parameters

            Returns:
                dict    -   dictionary consisting of the properties of this organization

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        url = self._services['ORGANIZATION'] % self.organization_id

        if params:
            url += '?'
            for key, value in params.items():
                url += f'{key}={value}&'
            url = url[:-1]

        flag, response = self._cvpysdk_object.make_request(
            'GET', url
        )

        if flag:
            if response.json() and 'organizationInfo' in response.json():
                self._organization_info = response.json()['organizationInfo']

                organization = self._organization_info['organization']
                organization_properties = self._organization_info['organizationProperties']

                self._description = organization['description']
                self._email_domain_names = organization.get('emailDomainNames')
                self._organization_name = organization.get('connectName')
                self._domain_name = organization['shortName']['domainName']
                self._backup_disabled = organization['deactivateOptions']['disableBackup']
                self._restore_disabled = organization['deactivateOptions']['disableRestore']
                self._login_disabled = organization['deactivateOptions']['disableLogin']
                self._is_auth_code_enabled = organization_properties['enableAuthCodeGen']
                self._auth_code = organization_properties.get('authCode')
                self._use_upn = organization_properties.get('useUPNForEmail')
                self._reseller_enabled = organization_properties.get('canCreateCompanies')
                self._is_data_encryption_enabled = organization_properties.get('showDLP')
                self._infrastructure_type = organization_properties.get('infrastructureType')
                self._auto_laptop_owners = organization_properties.get('autoClientOwnerAssignmentType')
                self._supported_solutions = organization_properties.get('supportedSolutions')
                self._global_file_exceptions_enabled = organization_properties.get('useCompanyGlobalFilter')
                self._primary_domain = organization_properties.get('primaryDomain', '')
                self._additional_domain = organization_properties.get('additionalDomains', [])
                self._is_passkey_enabled = True if organization_properties['advancedPrivacySettings'][
                                                       'authType'] == 2 else False
                self._is_authorise_for_restore_enabled = \
                organization_properties['advancedPrivacySettings']['passkeySettings']['enableAuthorizeForRestore']
                self._is_allow_users_to_enable_passkey_enabled = organization_properties['allowUsersToEnablePasskey']
                self._owner_privacy = organization_properties.get("allowUsersToEnablePrivacy")
                self._session_timeout = organization_properties.get("loginSessionTimeoutInMinutes")

                privacy = organization_properties.get('privacy')
                if privacy:
                    self._company_privacy = privacy.get("enableDataSecurity")

                self._retire_laptops = organization_properties.get('autoRetireDevices', {})

                job_time_enabled = organization_properties.get('isJobStartTimeEnabled')
                if job_time_enabled:
                    job_time_epoch = organization_properties.get('jobStartTime', None)
                    self._job_start_time = job_time_epoch
                else:
                    self._job_start_time = 'System default'

                self._password_age = organization_properties.get('agePasswordDays', 0)
                self._download_software_from_internet = organization_properties['clientGroupForceClientSideDownload']
                time_epoch = organization_properties.get('orgCreationDateTime')
                time_string = (datetime.fromtimestamp(time_epoch).strftime("%b %#d") +
                               (datetime.fromtimestamp(time_epoch).strftime(
                                   " %Y") if datetime.now().year != datetime.fromtimestamp(time_epoch).year else '') +
                               datetime.fromtimestamp(time_epoch).strftime(", %#I:%M %p"))
                self._org_creation_time = time_string

                self._machine_count = organization_properties['totalMachineCount']
                self._user_count = organization_properties['userCount']

                self._sender_name = organization_properties.get('senderName', '')
                self._sender_email = organization_properties.get('senderSmtp', '')

                for contact in organization_properties.get('primaryContacts', []):
                    self._contacts[contact['user']['userName']] = {
                        'id': contact['user']['userId'],
                        'name': contact['fullName']
                    }

                self._default_plan.clear()
                for plan in organization_properties.get('defaultPlans', []):
                    self._default_plan.append(plan['plan']['planName'])

                for plan in self._organization_info.get('planDetails', []):
                    self._plans[plan['plan']['planName'].lower()] = plan['plan']['planId']

                self._operator_role = organization_properties['operatorRole']['roleName']
                self._operators = organization_properties.get("operators", [])

                if self._organization_info.get('planDetails', []):
                    self._plan_details = self._organization_info['planDetails']

                self._server_count = organization_properties['serverCount']

                for file_filter in organization_properties['globalFiltersInfo']['globalFiltersInfoList']:
                    os_type_map = {1: 'Windows', 2: 'Unix'}
                    self._file_exceptions[os_type_map[file_filter['operatingSystemType']]] = \
                        file_filter['globalFilters'].get('filters', [])

                return self._organization_info
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_company_usergroup(self):
        """ Get usergroups associated to a organization """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['COMPANY_USERGROUP'] % self.organization_id
        )

        if flag:
            if response.json() and 'userGroups' in response.json():
                user_group_info = response.json()['userGroups']
                details = []
                for user_group in user_group_info:
                    details.append(user_group.get('userGroupEntity', {}).get('userGroupName'))

                return details
            else:
                return []
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_security_associations(self):
        """ Get the security associations for a organization
                    Returns: (dict)
                            {
                            'master': [
                                        ['Array Management'],
                                        ['Create Role', 'Edit Role', 'Delete Role'],
                                        ['Master']
                                    ],
                            'User2': [
                                        ['View']
                                    ]
                            }
                 """
        security_associations = {}
        value_list = {}
        url = self._services['SECURITY_ASSOCIATION'] + f'/61/{self._organization_id}'
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                response = response.json()
                security_list = response.get('securityAssociations')[0].get('securityAssociations').get('associations', [])
                for list_item in security_list:
                    name = list_item.get('userOrGroup')[0].get('userGroupName') or \
                           list_item.get('userOrGroup')[0].get('userName') or \
                           list_item.get('userOrGroup')[0].get('providerDomainName') + '\\' + \
                           list_item.get('userOrGroup')[0].get('externalGroupName')
                    if list_item.get('properties').get('role'):
                        value = (list_item.get('properties').get('role').get('roleName'))
                    elif list_item.get('properties').get('categoryPermission'):
                        for sub_list_item in list_item.get('properties').get('categoryPermission').get(
                                'categoriesPermissionList'):
                            value = (sub_list_item.get('permissionName'))
                    if value:
                        if name in value_list:
                            value_list[name].append(value)
                            value_list[name].sort()
                        else:
                            value_list[name] = [value]
                        security_associations.update({name: value_list[name]})

                return security_associations
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def update_security_associations(self, userOrGroupName, roleName, request_type=None, isUserGroup=False):
        """
        Updates Security Associations Of an Organisation

        Args:
            userOrGroupName (str)  --    User or User Group name
            roleName (str)         --    eg : 'Alert Owner' or 'Tenant Admin' or 'Tenant Operator' e.t.c
            request_type (str)     --    eg : 'OVERWRITE' or 'UPDATE' or 'DELETE', Default will be OVERWRITE operation
            isUserGroup (bool)     --    True or False. set isUserGroup = True, If input is user group.

        Raises:
            SDKException:
                if Invalid User or User Group is passed as parameter

                if failed to update the properties of the organization

                if response is empty
        """

        update_operator_request_type = {
            "OVERWRITE": 1,
            "UPDATE": 2,
            "DELETE": 3
        }

        if request_type:
            request_type = request_type.upper()

        req_json = {
            "entityAssociated": {
                "entity": [
                    {
                        "providerId": int(self.organization_id)
                    }
                ]
            },
            "securityAssociations": {
                "associationsOperationType": update_operator_request_type.get(request_type, 1),
                "associations": [{
                    "userOrGroup": [
                        {
                            "userGroupName" if isUserGroup else "userName": userOrGroupName
                        }
                    ],
                    "properties": {
                        "role": {
                            "roleName": roleName
                        }
                    }
                }
                ]
            }
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._services['SECURITY_ASSOCIATION'], req_json)

        if flag:
            if response.json():
                if 'errorMessage' in response.json():
                    error_message = response.json()['errorMessage']
                    error_code = response.json()['errorCode']
                    if error_code != 0:
                        raise SDKException('Organization', '110', 'Error: {0}'.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()

    def _update_properties(self, update_plan_details=False):
        """Executes the request on the server to update the properties of the organization.

            Args:
                update_plan_details -- to update the plan details associated with company

            Returns:
                None

            Raises:
                SDKException:
                    if failed to update the properties of the organization

                    if response is empty

        """

        request_json = {
            'organizationInfo': {
                'organization': self._properties.get('organization'),
                'organizationProperties': self._update_props.get('organizationProperties', {})
            }
        }

        domain_name = self._update_props.get('newAliasName')
        if domain_name:
            request_json['newAliasName'] = domain_name

        company_name = self._update_props.get('newCompanyName')
        if company_name:
            request_json['newCompanyName'] = company_name

        if update_plan_details:
            request_json['organizationInfo']['planDetailsOperationType'] = self._properties.get(
                'planDetailsOperationType')
            request_json['organizationInfo']['planDetails'] = self._properties.get('planDetails')

        __, response = self._cvpysdk_object.make_request(
            'PUT', self._services['UPDATE_ORGANIZATION'] % self.organization_id, request_json
        )

        self.refresh()

        if response.json():
            if 'error' in response.json():
                error_code = response.json()['error']['errorCode']
                error_message = response.json()['error'].get('errorMessage', '')
            else:
                error_code = response.json()['errorCode']
                error_message = response.json().get('errorMessage', '')

            if error_code != 0:
                raise SDKException(
                    'Organization', '110', 'Error: {0}'.format(error_message)
                )
        else:
            raise SDKException('Response', '102')

    def _update_properties_json(self, properties_dict):
        """Update the values of the **organizationProperties** tag in the properties JSON.

            Args:
                properties_dict     (dict)  --  dict consisting of the key in properties JSON
                to be updated, and the data to be substituted as it's value

            Returns:
                None

        """
        for key in properties_dict:
            self._update_props['organizationProperties'][key] = properties_dict[key]

    @property
    def name(self):
        """Returns the Organization display name """
        return self._organization_info['organization']['connectName']

    @property
    def organization_id(self):
        """Returns the value of the id for this Organization."""
        return self._organization_id

    @property
    def organization_name(self):
        """Returns the value of the name for this Organization."""
        return self._organization_name.lower()

    @organization_name.setter
    def organization_name(self, value):
        """Method to set organization name

        Args:

            value (string): company name to be set
        """
        req_json = {
            "newCompanyName": value
        }

        self._update_props = req_json
        self._update_properties()

    @property
    def description(self):
        """Returns the description for this Organization."""
        return self._description

    @property
    def email_domain_names(self):
        """Returns the value of the email domain names for this Organization."""
        return self._email_domain_names

    @email_domain_names.setter
    def email_domain_names(self, value):
        """Method to set supported smtp for this organization

        Args:

            value (list): list of supported smtp to be set
        """
        self._properties['organization']['emailDomainNames'] = value
        self._update_properties()

    @property
    def domain_name(self):
        """Returns the value of the domain name for this Organization."""
        return self._domain_name

    @domain_name.setter
    def domain_name(self, value):
        """Method to set domain name for this organization

        Args:

            value (str): company alias to be set
        """
        req_json = {
            "newAliasName": value
        }

        self._update_props = req_json
        self._update_properties()

    @property
    def auth_code(self):
        """Returns the value of the Auth Code for this Organization."""
        return self._auth_code

    @property
    def is_auth_code_enabled(self):
        """Returns boolean whether Auth Code generation is enabled for this Organization or not."""
        return self._is_auth_code_enabled

    @property
    def is_auto_discover_enabled(self):
        """Returns boolen whether organization autodiscover attribute enabled for this organization."""
        return self._properties['organizationProperties'].get('enableAutoDiscovery', False)

    @property
    def is_backup_disabled(self):
        """Returns boolean whether backup is disabled for this organisation"""
        return self._backup_disabled

    @property
    def is_restore_disabled(self):
        """Returns boolean whether restore is disabled for this organisation"""
        return self._restore_disabled

    @property
    def is_login_disabled(self):
        """Returns boolean whether login is disabled for this organisation"""
        return self._login_disabled

    @property
    def password_age_days(self):
        """Returns the password age days for the organisation"""
        return self._password_age

    @property
    def is_download_software_from_internet_enabled(self):
        """Returns boolean indicating whether download software from the internet is enabled"""
        return True if self._download_software_from_internet else False

    @property
    def shared_laptop(self):
        """Returns boolean whether Shared Laptop Usage is enabled for this Organization or not."""
        return not self._organization_info['organizationProperties'].get('preferenceMachineCentricClient', True)

    @shared_laptop.setter
    def shared_laptop(self, value):
        """Sets Shared Laptop Usage for this Organization

        Args:

        value (bool): True/False
            False: Enable Shared Laptop usage
            True: Disable Shared Laptop usage

        """
        self._update_properties_json({'preferenceMachineCentricClient': not value})
        self._update_properties()

    @property
    def machine_count(self):
        """Returns the count of machines added to this Organization."""
        return self._machine_count

    @property
    def user_count(self):
        """Returns the count of Users added to this Organization."""
        return self._user_count

    @property
    def contacts(self):
        """Returns the Primary Contacts for this Organization."""
        return list(self._contacts.keys())

    @contacts.setter
    def contacts(self, user_names):
        """
        Sets Contact details for organization.
        User should be present in tenant admin group of the organization

        Args:
            user_names (list) -- List of usernames

        Raises:
            SDKException:
                If input parameter is not list

                If Input list is empty
        """
        if isinstance(user_names, list):
            if len(user_names) == 0:
                raise SDKException('Organization', 114, 'Contact Lists cannot be empty')
        else:
            raise SDKException('Organization', 101, 'user_names should be list')

        user_list = list()
        for user_name in user_names:
            user_list.append(
                {
                    'user': {
                        "userName": user_name
                    }
                }
            )

        req_json = {
            "primaryContactsOperationType": "OVERWRITE",
            "primaryContacts": user_list
        }

        self._update_properties_json(req_json)
        self._update_properties()

    @property
    def operators(self) -> list[tuple[str, str]]:
        """
        Returns the list of operators and roles associated to this organization

        Returns:
            list    -   list of (operator, role) tuple pairs

        Example:
            [
                ('<user name>', '<role name>'),
                ('<usergroup name>', '<role name>'),
                ...
            ]
        """
        return sorted([
            (
                op.get('user', {}).get('userName') or op.get('userGroup', {}).get('userGroupName'),
                op.get('role', {}).get('roleName')
            ) for op in self._operators
        ])

    @operators.setter
    def operators(self, operator_list: list[tuple[str, str]]) -> None:
        """
        Overwrites the operator:role associations of the organization

        Args:
            operator_list (list): list of (userOrGroup, role) tuple pairs

            [
                ('<user name>', '<role name>'),
                ('<usergroup name>', '<role name>'),
                ...
            ]

        Returns:
            None

        Raises:
            SDKException:
                if failed to update the properties of the organization

                if response is empty

        """
        operators_list = []
        for user_or_group_name, role_name in operator_list:
            operator_dict = {
                "role": {
                    "roleName": role_name,
                    "roleId": int(self._commcell_object.roles.get(role_name).role_id)
                }
            }

            if user_id := self._commcell_object.users.all_users.get(user_or_group_name.lower()):
                operator_dict['user'] = {
                    'userName': user_or_group_name,
                    'userId': int(user_id)
                }
            elif user_group_id := self._commcell_object.user_groups.all_user_groups.get(user_or_group_name.lower()):
                operator_dict['userGroup'] = {
                    'userGroupName': user_or_group_name,
                    'userGroupId': int(user_group_id)
                }
            else:
                raise SDKException('Organization', '110', f'Invalid User or User Group name: {user_or_group_name}')
            operators_list.append(operator_dict)

        request_json = {
            "organizationInfo": {
                "organization": {
                    "shortName": {"domainName": self.name, "id": int(self._organization_id)}
                },
                "organizationProperties": {
                    "operatorsOperationType": 1,
                    "operators": operators_list
                },
            }
        }
        __, response = self._cvpysdk_object.make_request(
            'PUT', self._services['UPDATE_ORGANIZATION'] % self.organization_id, request_json
        )
        self.refresh()
        if response.json():
            if 'error' in response.json():
                error_code = response.json()['error']['errorCode']
                error_message = response.json()['error'].get('errorMessage', '')
            else:
                error_code = response.json()['errorCode']
                error_message = response.json().get('errorMessage', '')

            if error_code != 0:
                raise SDKException(
                    'Organization', '110', 'Error: {0}'.format(error_message)
                )
        else:
            raise SDKException('Response', '102')

    @property
    def contacts_fullname(self):
        """ Returns Primary Contacts full name for the organization"""
        return [contact['name'] for contact in self._contacts.values()]

    @property
    def default_plan(self):
        """Returns the Default Plans associated to this Organization."""
        return self._default_plan

    @default_plan.setter
    def default_plan(self, value):
        """
        Updates default plan for Organization

        Args:
            value (dict) -- Dictionary consisting Server or Laptop Plan

            example:
            value = {
                'Server Plan' : 'Server Plan Name',
                'Laptop Plan' : 'Laptop Plan Name'
            }

        Raises:
            SDKException:
                If plan doesnot exist on Commcell

                If plan is not associated with company

        """
        if isinstance(value, dict):
            plan_list = []
            for plan_name in value.values():
                if plan_name.lower() not in self.plans:
                    raise SDKException('Organization', '111')
                plan_list.append({
                    "plan": {
                        "planId": int(self._commcell_object.plans.all_plans[plan_name.lower()])
                    }
                })

            self._update_properties_json({
                "defaultPlans": plan_list,
                "defaultPlansOperationType": "OVERWRITE",
            })
            self._update_properties()
            return

        if not value:
            self._update_properties_json({'defaultPlansOperationType': 'OVERWRITE'})
            self._update_properties()
        elif value.lower() not in self.plans:
            raise SDKException('Organization', '111')
        else:
            temp_plan = self._commcell_object.plans.get(value.lower())
            temp = [{
                'plan': {
                    'planId': int(temp_plan.plan_id),
                    'planName': temp_plan.plan_name
                },
                'subtype': temp_plan.subtype
            }]

            self._update_properties_json({'defaultPlans': temp})
            self._update_properties()

    @property
    def plans(self):
        """Returns the Plans associated to this Organization."""
        return list(self._plans.keys())

    @property
    def plan_details(self):
        """Returns the jobstarttime of a plan associated with a company"""
        return self._plan_details

    @property
    def server_count(self):
        """Returns the server count associated with a company"""
        return self._server_count

    @property
    def sender_name(self):
        """Returns sender name"""
        return self._sender_name

    @sender_name.setter
    def sender_name(self, sender_name):
        """Sets the email Sender Name"""
        self._update_properties_json({'senderName': sender_name})
        self._update_properties()

    @property
    def sender_email(self):
        """Returns sender email"""
        return self._sender_email

    @sender_email.setter
    def sender_email(self, sender_email):
        """Sets Sender Email adress"""
        self._update_properties_json({'senderSmtp': sender_email})
        self._update_properties()

    def update_email_settings(self, email_settings):
        """
        Updates Email Settings of an organisation

        Args:
            email_settings (dict) -- Dictionary consisting of sender name and email

            example:
            email_settings = {
                'sender_name' : 'name',
                'sender_email' : 'email'
            }

        Raises:
            SDKException:
                if sender_name or sender_email is missing in inputs
        """
        name = email_settings.get('sender_name', None)
        email = email_settings.get('sender_email', None)

        if name is None or email is None:
            raise SDKException('Organization', 114, 'No configurable settings were set in the input')
        req_json = {
            "senderSmtp": email,
            "senderName": name
        }
        self._update_properties_json(req_json)
        self._update_properties()

    @property
    def user_groups(self):
        """Returns the user group associated with a company"""
        return self._user_groups

    @property
    def organization_created_on(self):
        """ Returns the company creation time """
        return self._org_creation_time

    @property
    def file_exceptions(self):
        """ Returns the file exceptions for a company """
        return self._file_exceptions

    @file_exceptions.setter
    def file_exceptions(self, value):
        """
        This sets Global File Exceptions at Company Level, Individually File Exceptions for Windows or Unix can be set

        file_exceptions = filters, 'OVERWRITE'   It will overwrite with the keys which are present in filters dict.
        file_exceptions = filters, 'UPDATE'      It will update the keys which are present in filters dict.

        Args:
            value (tuple)  --  (filters, Operation_Type)

            eg :
            filters = {
                'Windows' : ['*.py'],  (optional)
                'Unix' : ['*.exe'],    (optional)
            }

            Operation_Type = 'OVERWRITE' or 'UPDATE'

        Raises:
            SDKException:
                if input is not tuple

                If input tuple is not in this format (dict, str)

        """

        filter_list = list()

        if isinstance(value, tuple):
            if isinstance(value[0], dict) and isinstance(value[1], str):
                exceptions = value[0]
                operation_type = value[1]

                for os, filters in exceptions.items():
                    temp = {
                        "globalFilters": {
                            "opType": "OVERWRITE",
                            "filters": filters if operation_type == 'OVERWRITE' else self.file_exceptions[os] + filters
                        },
                        "operatingSystemType": 'WINDOWS_GLOBAL_FILTER' if os == 'Windows' else 'UNIX_GLOBAL_FILTER'
                    }

                    filter_list.append(temp)

                req_json = {
                    "globalFiltersInfo": {
                        "globalFiltersInfoList": filter_list
                    }
                }

            else:
                raise SDKException('Organization', 114, 'No configurable settings were set in the input')
        else:
            raise SDKException('Organization', 101, 'Input should be Tuple')

        self._update_properties_json(req_json)
        self._update_properties()

    @property
    def is_global_file_exceptions_enabled(self):
        """ Returns if file exception is enabled """
        return self._global_file_exceptions_enabled

    @plans.setter
    def plans(self, value):
        """Update the list of plans associated with the Organization.

            Args:
                value            (list)   --  list of plans

            Returns:
                None

        """
        if not isinstance(value, list):
            raise SDKException('Organization', '101')

        plans_list = []
        temp = {}

        for plan in value:
            plan_dict = {}
            if isinstance(plan, dict):
                plan_dict = plan
                plan = plan['plan_name']
            if not self._commcell_object.plans.has_plan(plan):
                raise SDKException(
                    'Organization', '102', 'Plan: "{0}" does not exist on Commcell'.format(plan)
                )

            temp_plan = self._commcell_object.plans.get(plan)
            temp = {
                'plan': {
                    'planId': int(temp_plan.plan_id)
                }
            }

            if plan_dict.get('job_start_time'):
                temp['jobStartTime'] = plan_dict['job_start_time']
                temp['isStartTimeOverridden'] = True

            plans_list.append(temp)

            del temp
            del temp_plan

        self._properties['planDetails'] = plans_list
        self._properties['planDetailsOperationType'] = 1
        self._update_properties(update_plan_details=True)

    @property
    def is_company_privacy_enabled(self):
        """Returns true if company privacy is enabled"""
        return self._company_privacy

    @property
    def is_owner_data_privacy_enabled(self):
        """Returns true if owner data privacy is enabled"""
        return self._owner_privacy

    @property
    def user_session_timeout(self):
        """Returns company user session timeout value"""
        return self._session_timeout

    @user_session_timeout.setter
    def user_session_timeout(self, value: int) -> None:
        """Sets user session timeout

        Args:
            value (int): timeout time in minutes
        """
        self._update_properties_json({'loginSessionTimeoutInMinutes': value})
        self._update_properties()

    def dissociate_plans(self, value):
        """disassociates plans from the organization

            Args:
                value            (list)   --  list of plans

            Returns:
                None
        """

        if not isinstance(value, list):
            raise SDKException('Organization', '101')

        plans_list = []

        for plan in value:
            if not self._commcell_object.plans.has_plan(plan):
                raise SDKException(
                    'Organization', '102', 'Plan: "{0}" does not exist on Commcell'.format(plan)
                )
            else:
                temp_plan = self._commcell_object.plans.get(plan)
                temp = {
                    'plan': {
                        'planId': int(temp_plan.plan_id)
                    }
                }
                plans_list.append(temp)

                del temp
                del temp_plan

        self._properties['planDetails'] = plans_list
        self._properties['planDetailsOperationType'] = 3
        self._update_properties(update_plan_details=True)

    def refresh(self, **params):
        """Refresh the properties of the Organization.
        
            Args:
                params  (dict)  --  dictionary of query parameters
        """
        self._default_plan = []
        self._contacts = {}
        self._plans = {}
        self._update_props['organizationProperties'] = {}
        self._properties = self._get_properties(**params)
        self._user_groups = self._get_company_usergroup()
        self._tfa_obj.refresh()

    def enable_auth_code(self):
        """Executes the request on the server to enable Auth Code Generation for the Organization.

            Refresh the Auth Code if Auth Code generation is already enabled for the Organization.

            Args:
                None

            Returns:
                str     -   auth code generated from the server

            Raises:
                SDKException:
                    if failed to enable auth code generation

                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['GENERATE_AUTH_CODE'] % self.organization_id
        )

        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']

                if error_code != 0:
                    raise SDKException(
                        'Organization', '108', 'Error: "{0}"'.format(
                            response.json()['error']['errorMessage']
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        return response.json()['organizationProperties']['authCode']

    def disable_auth_code(self):
        """Executes the request on the server to disable Auth Code Generation for the Organization.

            Args:
                None

            Returns:
                None

            Raises:
                SDKException:
                    if failed to disable auth code generation

                    if response is empty


                    if response is not success

        """
        try:
            self._update_properties_json({'enableAuthCodeGen': False})
            self._update_properties()
        except KeyError:
            raise SDKException('Organization', '109')

    @property
    def tenant_operator(self):
        """Returns the operators associated to this organization"""
        tenant_operators = self._organization_info.get('organizationProperties', {}).get('operators', [])
        user_list = []
        usergroup_list = []
        for role in tenant_operators:
            if 'user' in role:
                user_list.append(role['user']['userName'])
            else:
                usergroup_list.append(role['userGroup']['userGroupName'])

        operators = {'Users': user_list, 'User Group': usergroup_list}
        return operators

    def add_user_groups_as_operator(self, user_group_list, request_type):
        """Update the local user_group as tenant operator of the company

        Args:
            user_group_list        (list)  -- user group list

            request_type        (str)   --  decides whether to UPDATE, DELETE or OVERWRITE user_group
            security association

        """
        update_operator_request_type = {
            "NONE": 0,
            "OVERWRITE": 1,
            "UPDATE": 2,
            "DELETE": 3
        }
        user_group_list_object = []
        for user_group in user_group_list:
            if not isinstance(user_group, UserGroup):
                user_group = self._commcell_object.user_groups.get(user_group)
            user_group_list_object.append(user_group)
        request_operator = {
            'operators': [{
                'userGroup': {
                    'userGroupName': user_group.name,
                }
            } for user_group in user_group_list_object],
            'operatorsOperationType': update_operator_request_type[request_type.upper()]
        }
        self._update_properties_json(request_operator)
        self._update_properties()

    def add_users_as_operator(self, user_list, request_type):
        """Update the local user as tenant operator of the company

        Args:
            user_list        (list) -- list of users

            request_type    (Str)  --  decides whether to UPDATE, DELETE or
                                       OVERWRITE user security association

        """
        update_operator_request_type = {
            "NONE": 0,
            "OVERWRITE": 1,
            "UPDATE": 2,
            "DELETE": 3
        }
        user_list_object = []
        for user in user_list:
            if not isinstance(user, User):
                user = self._commcell_object.users.get(user)
            user_list_object.append(user)

        request_operator = {
            'operators': [{
                'user': {
                    'userName': user.user_name,
                }
            } for user in user_list_object],
            'operatorsOperationType': update_operator_request_type[request_type.upper()]
        }

        self._update_properties_json(request_operator)
        self._update_properties()

    @property
    def operator_role(self):
        """Returns the operator role associated to this organization"""
        return self._operator_role

    @operator_role.setter
    def operator_role(self, role_name):
        """Updates the role associated with a tenant operator

        Args:
            role_name   (str)   -- Role name to be associated

        """
        role_object = self._commcell_object.roles.get(role_name.lower())
        request_role = {
            'operatorRole': {
                'roleId': role_object.role_id,
                'roleName': role_name
            }
        }
        self._update_properties_json(request_role)
        self._update_properties()

    def activate(self):
        """
        To activate the organization

        Args:
            None

        Returns:
            None

        Raises:
            SDKException:
                if failed to activate the organization

                if response is empty

                if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['ACTIVATE_ORGANIZATION'] % self.organization_id
        )

        if flag:
            if response.json():
                error_code = response.json()['response']['errorCode']

                if error_code != 0:
                    raise SDKException(
                        'Organization', '112', 'Error: "{0}"'.format(
                            response.json()['error']['errorMessage']
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def deactivate(self,
                   disable_backup=True,
                   disable_restore=True,
                   disable_login=True):
        """
        To deactivate the organization

        Args:
            disable_backup  (bool)      -- To disable backup
                                            default: True

            disable_restore (bool)      -- To disable restore
                                            default: True

            disable_login   (bool)      -- To disable login
                                            default: True

        Returns:
            None

        Raises:
            SDKException:
                if failed to deactivate the organization

                if response is empty

                if response is not success

        """
        request_json = {
            "deactivateOptions": {
                "disableBackup": disable_backup,
                "disableRestore": disable_restore,
                "disableLogin": disable_login
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['DEACTIVATE_ORGANIZATION'] % self.organization_id, request_json
        )

        if flag:
            if response.json():
                error_code = response.json()['response']['errorCode']

                if error_code != 0:
                    raise SDKException(
                        'Organization', '113', 'Error: "{0}"'.format(
                            response.json()['error']['errorMessage']
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    def verify_owner_assignment_config(self, want_ownership_type):
        """ Verifies that the ownership assignments settings are configured and set properly for company

        Args:
            want_ownership_type            (int)    -- Option number for ownership assignment type

        Raises:
            SDKException:
                if response is empty

                if response is not success

                if ownership assignment is not correct

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['ORGANIZATION'] % str(self.organization_id)
        )

        if flag:
            if response and response.json():
                if 'response' in response.json():
                    error_code = response.json()['response']['errorCode']

                    if error_code != 0:
                        raise SDKException(
                            'Organization', '102', 'Error: "{0}"'.format(
                                response.json()['error']['errorMessage']
                            )
                        )
                elif 'errorMessage' in response.json():
                    raise SDKException(
                        'Organization', '102', 'Error: "{0}"'.format(response.json()['errorMessage'])
                    )
                else:
                    resp = response.json()
                    got_ownership_type = resp.get('organizationInfo', {}).get('organizationProperties', {}).get(
                        "autoClientOwnerAssignmentType")

                    if got_ownership_type != want_ownership_type:
                        raise SDKException(
                            'Organization', '102', f"Error: autoClientOwnerAssignmentType value not set correctly. \
                              Found: {got_ownership_type}, Expected: {want_ownership_type}")
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_auto_discover(self):
        """Enables autodiscover at company level..

            Raises:
                SDKException:
                    if failed to update enableAutoDiscovery property
        """
        self._update_properties_json({'enableAutoDiscovery': True})
        self._update_properties()

    def disable_auto_discover(self):
        """Disables autodiscover at company level..

            Raises:
                SDKException:
                    if failed to update enableAutoDiscovery property
        """
        self._update_properties_json({'enableAutoDiscovery': False})
        self._update_properties()

    def add_service_commcell_associations(self, name, service_commcell):
        """To add organization on service commcell

            Args:

                name   (str) -- name of the organization that has to be created on service commcell

                service_commcell (str) -- name of the commcell where the company has to be created

            Raises:
                SDKException:

                    if organization association to service commcell fails

                    if response is empty

                    if response is not success

        """

        if not (isinstance(name, str) and
                isinstance(service_commcell, str)):
            raise SDKException('Organization', '101')

        request_json = {
            "organizationId": int(self.organization_id),
            "associationsOperationType": 1,
            "associations": [
                {
                    "userOrGroup": {
                        "_type_": 61,
                        "providerId": int(self.organization_id),
                        "providerDomainName": name
                    },
                    "entity": {
                        "entityType": 194,
                        "entityName":
                            self._commcell_object.registered_routing_commcells[service_commcell]['commCell'][
                                'commCellName'],
                        "_type_": 150,
                        "entityId":
                            self._commcell_object.registered_routing_commcells[service_commcell]['commCell'][
                                'commCellId']
                    },
                    "properties": {
                        "role": {
                            "roleId": 3,
                            "roleName": "View"
                        }
                    }
                }
            ]
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['SERVICE_COMMCELL_ASSOC'], request_json
        )

        if flag:
            if response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code != 0:
                    raise SDKException('Organization', '115')
                self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def remove_service_commcell_associations(self, name):
        """ To delete the organization association for service commcell

        Args:

            name    (str) -- name of the organization

        Raises:
                SDKException:

                    if delete organization association to service commcell fails

                    if response is empty

                    if response is not success

        """

        if not isinstance(name, str):
            raise SDKException('Organization', '101')

        request_json = {
            "organizationId": int(self.organization_id),
            "associationsOperationType": 1
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['SERVICE_COMMCELL_ASSOC'], request_json
        )

        if flag:
            if response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code != 0:
                    raise SDKException('Organization', '113')
                self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def add_client_association(self, client_name):
        """To associate a client to an organization

            Args:

                client_name   (str) -- name of the client which has to be associated to organization

            Raises:
                SDKException:

                    if client association to organization fails

                    if response is empty

                    if response is not success

        """

        if not self._commcell_object.clients.has_client(client_name):
            raise SDKException('Organization', '101')
        else:
            client_obj = self._commcell_object.clients.get(client_name)
        request_json = {
            "entities": [
                {
                    "clientId": int(client_obj.client_id),
                    "_type_": 3
                }
            ]
        }
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['ORGANIZATION_ASSOCIATION'] % self.organization_id, request_json
        )

        if flag:
            if response.json():
                error_code = response.json().get('errorCode', 0)

                if error_code != 0:
                    raise SDKException('Organization', '115')
                self.refresh()
                return
            raise SDKException('Response', '102')
        response_string = self._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def remove_client_association(self, client_name):
        """To de-associate a client to an organization

            Args:

                client_name   (str) -- name of the client which has to be associated to organization

            Raises:
                SDKException:

                    if client de-association to organization fails

                    if response is empty

                    if response is not success

        """

        if not self._commcell_object.clients.has_client(client_name):
            raise SDKException('Organization', '101')
        else:
            client_obj = self._commcell_object.clients.get(client_name)
        request_json = {
            "entities": [
                {
                    "clientId": int(client_obj.client_id),
                    "_type_": 3
                }
            ]
        }
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['ORGANIZATION_ASSOCIATION'] % 0, request_json
        )

        if flag:
            if response.json():
                error_code = response.json().get('errorCode', 0)

                if error_code != 0:
                    raise SDKException('Organization', '115')
                self.refresh()
                return
            raise SDKException('Response', '102')
        response_string = self._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    @property
    def is_tfa_enabled(self):
        """returns the status of two factor authentication (True/False)"""
        return self._tfa_obj.is_tfa_enabled

    @property
    def tfa_enabled_user_groups(self):
        """returns the list of user group names for which tfa is enabled. only for group inclusion tfa"""
        return self._tfa_obj.tfa_enabled_user_groups

    def enable_tfa(self, user_groups=None):
        """
        Enables two factor authentication for the oganization.

        Args:
             user_groups    (list)          --      list of user group names for which tfa needs to be enabled.

        Returns:
            None
        """
        self._tfa_obj.enable_tfa(user_groups=user_groups)

    def disable_tfa(self):
        """
        Disables two factor authentication for the organization

        Returns:
            None
        """
        self._tfa_obj.disable_tfa()

    @property
    def client_groups(self):
        """returns all the clientgroups associated with the organization

            Returns:
                dict - consists of all clientgroups associated to an organization
                        {
                             "clientgroup1_name": clientgroup1_id,
                             "clientgroup2_name": clientgroup2_id,
                        }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        if self._client_groups is None:
            query_params = f"?fq=companyId%3Aeq%3A{self._organization_id}&fl=groups.clientGroup%2Cgroups.Id%2Cgroups.name"

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'GET', self._services['SERVERGROUPS_V4'] + query_params
            ) # fetch all client groups associated with the organization

            if flag:
                if response.json() and 'serverGroups' in response.json():
                    client_groups = response.json()['serverGroups']
                    self._client_groups = {}

                    for client_group in client_groups:
                        temp_name = client_group['name'].lower()
                        temp_id = str(client_group['id']).lower()
                        self._client_groups[temp_name] = temp_id
                else:
                    self._client_groups = {}
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

        return self._client_groups

    def get_alerts(self):
        """
        Get all the alerts associated to organization

        Args:
            org_id (int) : organization id

        Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._services['GET_ALL_ALERTS']
        )
        alerts = []
        if flag:
            if response.json() and 'alertList' in response.json():
                alert_list = response.json()['alertList']
                for alert in alert_list:
                    if alert['organizationId'] == int(self.organization_id):
                        alerts.append(alert['alert']['name'])

                return alerts
            else:
                return []
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_company_data_privacy(self):
        """ To enable company privacy to prevent admin access to company data
        """
        if self._company_privacy:
            return

        self.set_company_data_privacy(True)

    def disable_company_data_privacy(self):
        """ To disable company privacy to prevent admin access to company data
        """
        if not self._company_privacy:
            return

        self.set_company_data_privacy(False)

    def set_company_data_privacy(self, value):
        """Method to set company data privacy

        Args:
            value (bool): True/False to enable/disable privacy
        Raises:
            SDKException:
                if disable company data privacy to service commcell fails
                if response is empty
                if response is not success
        """
        url = self._services['DISABLE_PRIVACY_COMPANY_DATA'] % self.organization_id
        if value:
            url = self._services['ENABLE_PRIVACY_COMPANY_DATA'] % self.organization_id

        flag, response = self._cvpysdk_object.make_request(
            'POST', url, {}
        )

        if flag:
            if response and response.json():
                error_message = response.json().get('errorMessage')
                if response.json().get('errorCode', -1) != 0:
                    raise SDKException('Organization', '102', error_message)

                self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def get_retire_laptop_properties(self):
        """
        Returns:
            dict -- Retire Laptop Properties of Organization

            example: {
                    "retireDevicesAfterDays": 183,
                    "forceDeleteDevicesAfterDays": -1
            }
        """
        return self._retire_laptops

    def retire_offline_laptops(self, retire_days, delete_days=None):
        """
        The number of days specified to retire laptops must be less than or equal to the number of days specified to delete laptops
        If delete_days is not specified, It will be set to 'Never'

        Args:
            retire_days (int) --  Number of days to retire laptops
            delete_days (int) --  Number of days to delete laptops

        Raises:
            SDKException
                If retire days is more than delete days
        """

        if delete_days is None:
            delete_days = -1

        if delete_days != -1 and retire_days > delete_days:
            raise SDKException(Organization, 101, 'The number of days specified to \
             retire laptops must be less than or equal to the number of days specified to delete laptops.')

        req_json = {
            'autoRetireDevices': {
                'retireDevicesAfterDays': retire_days,
                'forceDeleteDevicesAfterDays': delete_days
            }
        }

        self._update_properties_json(req_json)
        self._update_properties()

    @property
    def sites(self):
        """
        Gets the site information of organisation

        Returns:
            sites (dict)  -- sites information of organisation
        """
        return {'primary_site': self._primary_domain, 'additional_sites': self._additional_domain}

    @sites.setter
    def sites(self, sites):
        """
        Updates Sites information for an Organisation

        Args:
            sites (dict)   --  Consisting Of Primary and Additional sites information, Pass Empty dictionary to remove site information

            example:
            sites = {
                'primary_site' : 'comm.com',
                'additional_sites' : ["cv.comm.com", "skhk.comm.com"]
            }

        Raises:
            SDKException:
                If input is not dictionary

                If primary_site Key is missing in input

                If it fails to update sites information for an organisation
        """

        if isinstance(sites, dict):
            primary_site = sites.get('primary_site', "")

            additional_sites = sites.get('additional_sites', [])

            self._update_properties_json({
                "primaryDomain": primary_site,
                "additionalDomains": additional_sites,
                "additionalDomainsOperationType": "OVERWRITE"
            })
            self._update_properties()
        else:
            raise SDKException('Organization', 101, 'Input Parameter should be dictionary')

    @property
    def tags(self):
        """
        Returns:
            tags (list)  -- List of dictionaries containing TAG values

        Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        req_url = self._services['GET_ORGANIZATION_TAGS'] % (self.organization_id)
        flag, response = self._cvpysdk_object.make_request('GET', req_url)

        if flag:
            if response.json():
                if 'tags' in response.json():
                    return response.json()['tags'][0]['tag']
                else:
                    return []
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @tags.setter
    def tags(self, tag_list):
        """
        Updates Tags for an Organisation

        Args:
            tag_list (list) --  List of Tag details

            example:
                tag_list = [
                    {
                    "name": "key1",
                    "value": "value1"
                    },
                    {
                    "name": "key2",
                    "value": "value2"
                    }
                ]

        Raises:
            SDKException:
                If it fails to Update Tags for an Organisation
        """

        req_json = {
            "entityTag": [
                {
                    "entityId": int(self.organization_id),
                    "entityType": 61,
                    "tag": tag_list
                }
            ]
        }

        req_url = self._services['ORGANIZATION_TAGS']
        flag, response = self._cvpysdk_object.make_request('PUT', req_url, req_json)

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = response.json()['error']['errorCode']
                    if error_code != 0:
                        error_message = response.json()['error']['errorMessage']
                        raise SDKException('Organization', '110', 'Error: {0}'.format(error_message))
            else:
                raise SDKException('Organization', '110')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()

    @property
    def isPasskeyEnabled(self):
        """Returns True if Passkey is enabled on company"""
        return self._is_passkey_enabled

    @property
    def isAuthrestoreEnabled(self):
        """Returns True if Authrestore is enabled on company"""
        return self._is_authorise_for_restore_enabled

    @property
    def isAllowUsersToEnablePasskeyEnabled(self):
        """Returns True if it is enabled"""
        return self._is_allow_users_to_enable_passkey_enabled

    @property
    def company_theme(self)->dict:
        """
        Returns:
            theme   (dict)  -   the company level theme colors set, empty dict if no company level theme set

        Example:
            {
                loginAndBannerBg: '#0B2E44',
                headerColor: '#DDE5ED',
                headerTextColor: '#0B2E44',
                navBg: '#FFFFFF',
                navIconColor: '#0b2e44',
                pageHeaderText: '#0B2E44',
                actionBtnBg: '#0B2E44',
                actionBtnText: '#eeeeee',
                linkText: '#4B8DCC',
                iconColor: '#0B2E44'
            }
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['GET_ORGANIZATION_THEME'] % self.organization_id
        )
        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = response.json()['error']['errorCode']
                    if error_code != 0:
                        error_message = response.json()['error']['errorMessage']
                        raise SDKException('Organization', '102', 'Error: {0}'.format(error_message))
                theme = response.json().get('organizationInfo', {}).get('organizationProperties', {})
                theme = theme.get('customization', '{}')
                return json.loads(theme)
            else:
                raise SDKException('Organization', '102', 'Empty Response')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @company_theme.setter
    def company_theme(self, theme_colors:dict)->None:
        """
        Sets company level theme for an Organisation

        Args:
            theme_colors    (dict)  -   with color setting name as key and color hex as value

            example:
                theme_colors = {
                    loginAndBannerBg: '#0B2E44',
                    headerColor: '#DDE5ED',
                    headerTextColor: '#0B2E44',
                    navBg: '#FFFFFF',
                    navIconColor: '#0b2e44',
                    pageHeaderText: '#0B2E44',
                    actionBtnBg: '#0B2E44',
                    actionBtnText: '#eeeeee',
                    linkText: '#4B8DCC',
                    iconColor: '#0B2E44'
                }

        Raises:
            SDKException:
                If it fails to Set theme for an Organisation
        """
        request_json = {
            "organizationInfo": {
                "organizationProperties": {
                    "customization": json.dumps(theme_colors)
                },
            }
        }
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['ORGANIZATION_THEME'] % self.organization_id, request_json
        )

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = response.json()['error']['errorCode']
                    if error_code != 0:
                        error_message = response.json()['error']['errorMessage']
                        raise SDKException('Organization', '110', 'Error: {0}'.format(error_message))
            else:
                raise SDKException('Organization', '110')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()

    def passkey(self, current_password, action, new_password=None):
        """"
        Updates Passkey properties of an Organisation

        Args:
            current_password (str) --  User Current Passkey to perform actions
            action (str)           --  'enable' | 'disable' | 'change passkey' | 'authorise'
            new_password (str)     --  Resetting existing Passkey

        Raises:
            SDKException:
                if invalid action is passed as a parameter

                if request fails to update passkey properties of  an organisation

                if new password is missing while changing passkey
        """

        current_password = b64encode(current_password.encode()).decode()

        req_url = self._services['COMPANY_PASSKEY'] % (int(self.organization_id))

        if action.lower() == 'enable':
            req_json = {
            "newPasskey": current_password,
            "confirmPasskey": current_password,
            "passkeyOpType": "CREATE"
            }

        elif action.lower() == 'disable':
            req_json = {
                "currentPasskey": current_password,
                "confirmPasskey": current_password,
                "passkeyOpType": "DISABLE"
            }

        elif action.lower() == 'change passkey':
            if new_password:
                new_password = b64encode(new_password.encode()).decode()
                req_json = {
                    "currentPasskey": current_password,
                    "newPasskey": new_password,
                    "confirmPasskey": new_password,
                    "passkeyOpType": "EDIT"
                }
            else:
                raise SDKException('Organization', 102, 'New password is missing in input')

        elif action.lower() == 'authorise':
            req_json = {
                "passkey": current_password,
                "passkeySettings": {
                    "enableAuthorizeForRestore": True,
                    "passkeyExpirationInterval": {
                        "toTime": 1800
                    }
                }
            }
            req_url = self._services['COMPANY_AUTH_RESTORE'] % (int(self.organization_id))

        else:
            raise SDKException('Organization', 102, 'Action is undefined, Invalid action passed as a parameter')

        flag, response = self._cvpysdk_object.make_request('POST', req_url, req_json)

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = response.json()['error']['errorCode']
                    if error_code != 0:
                        error_message = response.json()['error']['errorMessage']
                        raise SDKException('Organization', '110', 'Error: {0}'.format(error_message))
            else:
                raise SDKException('Organization', '110')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()

    def enable_owner_data_privacy(self):
        """ To enable company privacy to allow owner to enable data privacy """
        if self.is_owner_data_privacy_enabled:
            return

        self._update_properties_json({'allowUsersToEnablePrivacy': True})
        self._update_properties()

    def disable_owner_data_privacy(self):
        """ To disable company privacy to allow owner to enable data privacy """
        if not self.is_owner_data_privacy_enabled:
            return

        self._update_properties_json({'allowUsersToEnablePrivacy': False})
        self._update_properties()

    def allow_owners_to_enable_passkey(self, flag):
        """
        Enable or Disable option to allow owners to enable privacy

        Args:
            flag (boolean)   --  True (Enable Passkey) or False (Disable Passkey)
        """
        self._update_properties_json({"allowUsersToEnablePasskey": flag})
        self._update_properties()

    def update_general_settings(self, general_settings_dict):
        """Method to update properties of general settings in an organization

        Args:
                general_settings_dict (dict): general settings properties to be modified
                Eg.
                    properties_dict = {
                        "newName": "string",
                        "general": {
                            "newAlias": "string",
                            "emailSuffix": "string",
                            "authcodeForInstallation": true,
                            "twoFactorAuth": {
                                "enable": true,
                                "all": true,
                                "userGroups": [
                                    {
                                        "id": 0,
                                        "name": "string"
                                    }
                                ]
                            },
                            "resellerMode": true,
                            "enableDataEncryption": true,
                            "autoDiscoverApp": true,
                            "infrastructureType": "RENTED_STORAGE",
                            "supportedSolutions": [
                                "FILE_SERVER"
                            ],
                            "assignLaptopOwners": "LOGGED_IN_ACTIVE_DIRECTORY_USERS",
                        }
                    }

         Raises:
                SDKException:

                    if unable to update general settings

                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['EDIT_COMPANY_DETAILS'] % self.organization_id, general_settings_dict
        )

        if flag:
            if response and response.json():
                error_message = response.json().get('errorMessage')
                if response.json().get('errorCode', -1) != 0:
                    raise SDKException('Organization', '102', error_message)

                self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def geo_info(self) -> tuple[str, list[str]]:
        """
        The regions this company is mapped to

        Returns:
            idp_region          (str)   -   region name of idp
            workload_regions    (list)  -   list of region names of workloads
        """
        geo_info = self._organization_info.get('organizationProperties', {}).get('companyGeoInfo', [])
        workloads = []
        idp = None
        for region in geo_info:
            region_name = region.get('companyRegion', {}).get('regionName')
            if region.get('isIdPRegion'):
                idp = region_name
            else:
                workloads.append(region_name)
        return idp, workloads

    @property
    def provider_guid(self) -> str:
        """
        provider GUID for this organization
        """
        return self._organization_info.get('organization', {}).get('providerGUID')

    def add_additional_settings(self, key_name, category, data_type, value, comment="Added using automation", enabled=1):
        """Adds additional settings on company level

        Args:
            key_name (str):

        """
        properties_dict = {
            "additionalSettings": [
                {
                    "entityInfo": {
                        "entityId": int(self.organization_id),
                        "entityType": 189,
                        "_type_": 189
                    },
                    "registryKeys": [
                        {
                            "relativepath": category,
                            "keyName": key_name,
                            "type": data_type,
                            "value": value,
                            "enabled": enabled,
                            "comment": comment
                        }
                    ]
                }
            ]
        }
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['ORGANIZATION_ADDITIONAL_SETTINGS'], properties_dict
        )

        if flag:
            if response and response.json():
                error_message = response.json().get('errorMessage')
                if response.json().get('error', {}).get('errorCode', -1) != 0:
                    raise SDKException('Organization', '102', error_message)

                self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)



class RemoteOrganization:
    """Class for performing remote operations on an Organization."""

    def __init__(self, commcell_object, organization_name: str, organization_id: str = None, **kwargs):
        """Initialise the RemoteOrganization instance.

            Args:
                commcell_object     (object)    --  instance of the Commcell class

                organization_name   (str)       --  name of the organization

                organization_id     (str)       --  id of the organization
                    default: None

                homecell            (str)       --  the belonging service commcell of this organization
                    default: None

                workloads           (list)      --  list of workloads this organization is extended to

            Returns:
                object  -   instance of the RemoteOrganization class

        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._organization_name = organization_name

        self._homecell = kwargs.get('homecell') or self._get_homecell()
        self._workloads = kwargs.get('workloads') or self._get_workloads()

        self._headers = self._commcell_object._headers.copy()
        self._headers['CVContext']='Comet'
        self._headers['_cn'] = self._homecell
        self._headers['Comet-Commcells'] = self._homecell

        if organization_id:
            self._organization_id = str(organization_id)
        else:
            self._organization_id = self._get_organization_id()

        self._properties = {}
        self._reseller_enabled = None
        self._backup_disabled = None
        self._login_disabled = None
        self._restore_disabled = None
        self._domain_name = None
        self._operators = []
        self._parent_company = None

        self.refresh()

    @property
    def reseller_enabled(self)->bool:
        """
        Returns if reseller is enabled

        Returns:
            bool - True if reseller mode is enabled for the company
        """
        return self._reseller_enabled

    def __repr__(self)->str:
        """Returns the string representation of an instance of this class."""
        return 'Remote Organization class instance for Organization: "{0}" of "{1}"'.format(
            self.organization_name, self._homecell
        )

    def _get_organization_id(self)->str:
        """Gets the remote id associated with this remote organization within given commcell.

            Returns:
                str     -   remote id associated with this remote organization

        """
        organizations = Organizations(self._commcell_object)
        organizations.fanout = True
        return organizations.get_remote_org(self.organization_name).organization_id

    def _get_homecell(self)->str:
        """Gets the service commcell this company belongs to.

            Returns:
                str     -   service commcell where company resides

        """
        organizations = Organizations(self._commcell_object)
        organizations.fanout = True
        return organizations.get_remote_org(self.organization_name).homecell

    def _get_workloads(self) -> list[str]:
        """
        Gets the list of workloads this company is extended/associated to

        Returns:
            list    -   list of commcell names
        """
        organizations = Organizations(self._commcell_object)
        organizations.fanout = True
        return organizations.all_organizations_props[self._organization_name]['workloads']

    def _get_properties(self)->dict:
        """Gets the properties of this Organization.

            Returns:
                dict    -   dictionary consisting of the properties of this organization

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['ORGANIZATION'] % self.organization_id, headers=self._headers.copy()
        )

        if flag:
            if response.json() and 'organizationInfo' in response.json():
                self._organization_info = response.json().get('organizationInfo', {})

                organization = self._organization_info.get('organization', {})
                organization_properties = self._organization_info.get('organizationProperties', {})

                self._description = organization.get('description')
                self._email_domain_names = organization.get('emailDomainNames')
                self._domain_name = organization.get('shortName', {}).get('domainName')
                self._backup_disabled = organization.get('deactivateOptions', {}).get('disableBackup')
                self._restore_disabled = organization.get('deactivateOptions', {}).get('disableRestore')
                self._login_disabled = organization.get('deactivateOptions', {}).get('disableLogin')
                self._reseller_enabled = organization_properties.get('canCreateCompanies')

                self._operators = organization_properties.get("operators", [])
                self._parent_company = organization_properties.get("resellerCompany")

                return self._organization_info
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def name(self)->str:
        """
        Returns the Organization display name

        Returns:
            str     -   name of this organization
        """
        return self._organization_info.get('organization', {}).get('connectName')

    @property
    def organization_id(self)->str:
        """
        Returns the value of the id for this Organization.

        Returns:
            str     -   id of this organization (in given commcell)

        """
        return self._organization_id

    @property
    def homecell(self)->str:
        """
        Returns the service commcell name of this Organization.

        Returns:
            str     -   commserve name where this organization exists
        """
        return self._homecell

    @property
    def workloads(self) -> list[str]:
        """
        Returns the list of commcells this company has extensions in

        Returns:
            workloads   (list)  -   list of commcell names
        """
        return self._workloads

    @property
    def geo_info(self) -> tuple[str, list[str]]:
        """
        The regions this company is mapped to

        Returns:
            idp_region          (str)   -   region name of idp
            workload_regions    (list)  -   list of region names of workloads
        """
        geo_info = self._organization_info.get('organizationProperties', {}).get('companyGeoInfo', [])
        workloads = []
        idp = None
        for region in geo_info:
            region_name = region.get('companyRegion', {}).get('regionName')
            if region.get('isIdPRegion'):
                idp = region_name
            else:
                workloads.append(region_name)
        return idp, workloads

    @property
    def provider_guid(self) -> str:
        """
        Returns:
            provider GUID for this organization
        """
        return self._organization_info.get('organization', {}).get('providerGUID')

    @property
    def organization_name(self)->str:
        """
        Returns the value of the name for this Organization.

        Returns:
            str     -   organization name
        """
        return self._organization_name.lower()

    @property
    def domain_name(self)->str:
        """
        Returns the value of the domain name for this Organization.

        Returns:
            str     -   alias name/domain name of this organization

        """
        return self._domain_name

    @property
    def parent_company(self)->dict:
        """
        Returns the parent company details dict of this organization (if it is child company).

        Returns:
            dict    -   parent company details

        Example: {
            '_type_': <entity type id>,
            'providerId': <company id>,
            'providerDomainName': '<company name>'
            }

        """
        return self._parent_company

    @property
    def is_backup_disabled(self)->bool:
        """
        Returns boolean whether backup is disabled for this organisation

        Returns:
            bool    -   True if backup is disabled

        """
        return self._backup_disabled

    @property
    def is_restore_disabled(self)->bool:
        """
        Returns boolean whether restore is disabled for this organisation

        Returns:
            bool    -   True if restore is disabled

        """
        return self._restore_disabled

    @property
    def is_login_disabled(self)->bool:
        """
        Returns boolean whether login is disabled for this organisation

        Returns:
            bool    -   True if login is disabled

        """
        return self._login_disabled

    def refresh(self)->None:
        """Refresh the properties of the Organization."""
        self._properties = self._get_properties()

    @property
    def operators(self) -> list[tuple[str, str]]:
        """
        Returns the list of operators and roles associated to this organization

        Returns:
            list    -   list of (operator, role) tuple pairs

        Example:
            [
                ('<user name>', '<role name>'),
                ('<usergroup name>', '<role name>'),
                ...
            ]
        """
        return sorted([
            (
                op.get('user', {}).get('userName') or op.get('userGroup', {}).get('userGroupName'),
                op.get('role', {}).get('roleName')
            ) for op in self._operators
        ])

    def lookup_operator(self, user_or_group: str, role: str) -> dict:
        """
        Gets the user id role id full dictionary for given user/group and role
        """
        for operator in self._operators:
            this_role = operator.get('role', {}).get('roleName')
            this_user_or_group = (operator.get('user', {}).get('userName') or
                                  operator.get('userGroup', {}).get('userGroupName'))
            if this_role == role and this_user_or_group == user_or_group:
                return operator
        return {}

    @operators.setter
    def operators(self, operator_list: list[tuple[str, str]]) -> None:
        """
        Overwrites the operator:role associations of the remote organization

        Args:
            operator_list (list): list of (userOrGroup, role) tuple pairs

            [
                ('<user name>', '<role name>'),
                ('<usergroup name>', '<role name>'),
                ...
            ]

        Returns:
            None

        Raises:
            SDKException:
                if failed to update the properties of the organization

                if response is empty

        """
        operators_list = []
        for user_or_group_name, role_name in operator_list:
            if operator_dict := self.lookup_operator(user_or_group_name, role_name):
                operators_list.append(operator_dict)
                continue

            operator_dict = {
                "role": {
                    "roleName": role_name,
                    "roleId": int(self._commcell_object.roles.get(role_name).role_id)
                }
            }

            if user_id := self._commcell_object.users.all_users.get(user_or_group_name.lower()):
                operator_dict['user'] = {
                    'userName': user_or_group_name,
                    'userId': int(user_id)
                }
            elif user_group_id := self._commcell_object.user_groups.all_user_groups.get(user_or_group_name.lower()):
                operator_dict['userGroup'] = {
                    'userGroupName': user_or_group_name,
                    'userGroupId': int(user_group_id)
                }
            else:
                raise SDKException('RemoteOrganization', '101', f'User/Group not found: {user_or_group_name}')
            operators_list.append(operator_dict)

        request_json = {
            "organizationInfo": {
                "organization": {
                    "shortName": {"domainName": self.name, "id": int(self._organization_id)}
                },
                "organizationProperties": {
                    "operatorsOperationType": "OVERWRITE",
                    "operators": operators_list
                },
            }
        }
        api_endpoint = self._services['COMPANY_OPERATORS']

        try:
            sp_version = self._commcell_object.version.split('.')
            if len(sp_version) > 2 and int(sp_version[1]) <= 38 and int(sp_version[2]) <= 20:
                api_endpoint = self._services['UPDATE_ORGANIZATION'] % self.organization_id
        except:
            pass

        __, response = self._cvpysdk_object.make_request(
            'PUT', api_endpoint, request_json, headers=self._headers.copy()
        )
        self.refresh()
        if response.json():
            if 'error' in response.json():
                error_code = response.json()['error'].get('errorCode')
                error_message = response.json()['error'].get('errorMessage', '')
            else:
                error_code = response.json().get('errorCode')
                error_message = response.json().get('errorMessage', '')

            if error_code != 0:
                raise SDKException(
                    'RemoteOrganization', '101', 'Error: {0}'.format(error_message)
                )
        else:
            raise SDKException('Response', '102')

    def activate(self)->None:
        """
        To activate the organization remotely

        Args:
            None

        Returns:
            None

        Raises:
            SDKException:
                if failed to activate the organization

                if response is empty

                if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['ACTIVATE_ORGANIZATION'] % self.organization_id, headers=self._headers.copy()
        )
        self.refresh()
        if flag:
            if response.json():
                error_code = response.json()['response']['errorCode']

                if error_code != 0:
                    raise SDKException(
                        'RemoteOrganization', '102', 'Error: "{0}"'.format(
                            response.json()['error']['errorMessage']
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def deactivate(self,
                   disable_backup=True,
                   disable_restore=True,
                   disable_login=True)->None:
        """
        To deactivate the organization remotely

        Args:
            disable_backup  (bool)      -- To disable backup
                                            default: True

            disable_restore (bool)      -- To disable restore
                                            default: True

            disable_login   (bool)      -- To disable login
                                            default: True

        Returns:
            None

        Raises:
            SDKException:
                if failed to deactivate the organization

                if response is empty

                if response is not success

        """
        request_json = {
            "deactivateOptions": {
                "disableBackup": disable_backup,
                "disableRestore": disable_restore,
                "disableLogin": disable_login
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['DEACTIVATE_ORGANIZATION'] % self.organization_id, request_json,
            headers=self._headers.copy()
        )

        if flag:
            if response.json():
                error_code = response.json()['response']['errorCode']

                if error_code != 0:
                    raise SDKException(
                        'RemoteOrganization', '103', 'Error: "{0}"'.format(
                            response.json()['error']['errorMessage']
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    @property
    def tags(self)->list:
        """
        Returns:
            tags (list)  -- List of dictionaries containing TAG values

        Example:
                [
                    {
                    "name": "key1",
                    "value": "value1"
                    },
                    {
                    "name": "key2",
                    "value": "value2"
                    }
                ]

        Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        req_url = self._services['GET_ORGANIZATION_TAGS'] % (self.organization_id)
        flag, response = self._cvpysdk_object.make_request('GET', req_url, headers=self._headers.copy())

        if flag:
            if response.json():
                if 'tags' in response.json():
                    return response.json()['tags'][0]['tag']
                else:
                    return []
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @tags.setter
    def tags(self, tag_list:list)->None:
        """
        Updates Tags for an Organisation

        Args:
            tag_list (list) --  List of Tag details

            example:
                tag_list = [
                    {
                    "name": "key1",
                    "value": "value1"
                    },
                    {
                    "name": "key2",
                    "value": "value2"
                    }
                ]

        Raises:
            SDKException:
                If it fails to Update Tags for an Organisation
        """

        req_json = {
            "entityTag": [
                {
                    "entityId": int(self.organization_id),
                    "entityType": 61,
                    "tag": tag_list
                }
            ]
        }

        req_url = self._services['ORGANIZATION_TAGS']
        flag, response = self._cvpysdk_object.make_request('PUT', req_url, req_json, headers=self._headers.copy())

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = response.json()['error']['errorCode']
                    if error_code != 0:
                        error_message = response.json()['error']['errorMessage']
                        raise SDKException('RemoteOrganization', '104', 'Error: {0}'.format(error_message))
            else:
                raise SDKException('RemoteOrganization', '104')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()

    def get_entity_counts(self)->dict:
        """Gets the entity type and counts for company's associated entities

            Returns:
                dict    -   entity as key and count as value

                    {'total': 8, 'Alert definitions': 4, 'User': 1, 'User group': 2, 'Server group': 1}

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET',
            self._services['COMPANY_ENTITIES'] % self._organization_id,
            headers=self._headers.copy()
        )
        entity_counts = {}
        entity_types = ENTITY_TYPE_MAP
        if flag:
            if response.json():
                entity_counts['total'] = response.json().get('totalCount', None)
                for entity in response.json().get('entities',[]):
                    entity_counts[entity_types.get(entity['name'], f'type_{entity["name"]}')] = entity['count']
                return entity_counts
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def extend(self, region: str, country: str, commcell_name: str) -> None:
        """
        Extends this company to specified region
        
        Args:
            region  (str)           -   the name of region to extend to
            country (str)           -   country associated with region name
            commcell_name   (str)   -   commcell name associated with region
        """
        req_json = {
            "sourceCommcell": {
                "commcell": {"commCellName": self.homecell}
            },
            "targetCommcell": {
                "commcell": {"commCellName": commcell_name},
                "companyGeoInfo": {
                    "country": country,
                    "companyRegion": {"regionName": region}
                }
            },
            "tenantCompany": {
                "providerGUID": self.provider_guid.lower()
            }
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._services['EXTEND_ORGANIZATION'], req_json)

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = response.json()['error']['errorCode']
                    if error_code != 0:
                        error_message = response.json()['error']['errorMessage']
                        raise SDKException('RemoteOrganization', '111', 'Error: {0}'.format(error_message))
            else:
                raise SDKException('RemoteOrganization', '111')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()
