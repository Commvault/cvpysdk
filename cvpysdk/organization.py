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

    **add_service_commcell_associations [deprecated] **
      Use commcell.service_commcells.add_associations() instead

    **remove_service_commcell_associations [deprecated] **
      Use commcell.service_commcells.remove_associations() instead

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
    
    configure_breakglass_account()   -- Configures the BreakGlass account for the organization

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
from base64 import b64encode
from typing import TYPE_CHECKING, Optional, List, Dict, Any, Union, Tuple

from .additional_settings import AdditionalSettings
from .exception import SDKException
from .constants import ENTITY_TYPE_MAP
from .security.user import User
from .security.usergroup import UserGroup
from .security.role import Role
from .security.two_factor_authentication import TwoFactorAuthentication

if TYPE_CHECKING:
    from .commcell import Commcell


class Organizations:
    """Class for doing operations on Organizations like add / delete an organization, etc.

    Attributes:
        _commcell_object (object): Instance of the Commcell class.
        _cvpysdk_object (object): Instance of the CVPySDK class.
        _services (dict): Dictionary of services.
        _update_response_ (callable): Function to update the response.
        _organizations_api (str): API endpoint for organizations.
        _organizations (dict): Dictionary of organizations.
        _organizations_cache (dict): Cache of organizations.
        _adv_config (dict): Advanced configuration for organizations.
        filter_query_count (int): Count of filter queries.

    Usage:
        # Initialize Organizations class
        orgs = Organizations(commcell_object)
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initializes an instance of the Organizations class to perform operations on a company.

            Args:
                commcell_object (object): Instance of the Commcell class

            Returns:
                object: Instance of the Organizations class

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._organizations_api = self._services['ORGANIZATIONS']
        self._organizations = None
        self._organizations_cache = None
        self._adv_config = None
        self.filter_query_count = 0

        self.refresh()

    def __str__(self) -> str:
        """Representation string consisting of all organizations present in the Commcell.

            Returns:
                str: String of all the organizations associated with the commcell

        """
        representation_string = '{:^5}\t{:^40}\n\n'.format('S. No.', 'Organization')

        for index, organization in enumerate(self._organizations):
            sub_str = '{:^5}\t{:40}\n'.format(index + 1, organization)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Returns the string representation of an instance of this class."""
        return "Organizations class instance for Commcell"

    def __len__(self) -> int:
        """Returns the number of the organizations configured on the Commcell."""
        return len(self.all_organizations)

    def __getitem__(self, value: str) -> str:
        """Returns the name of the organization for the given organization ID or
            the details of the organization for given organization Name.

            Args:
                value (str): Name or ID of the organization

            Returns:
                str: name of the organization, if the organization id was given

                dict: dict of details of the organization, if organization name was given

            Raises:
                IndexError: no organization exists with the given Name / Id

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

    def _get_organizations(self, full_response: bool = False) -> dict:
        """Gets all the organizations associated with the Commcell environment.
            Args:
                full_response (bool): flag to return complete response
            Returns:
                dict: consists of all organizations added to the commcell

                    {
                        "organization1_name": organization1_id,

                        "organization2_name": organization2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._organizations_api)
        if flag:
            organizations = {}
            self._adv_config = {}
            if response.json() and 'providers' in response.json():
                if full_response:
                    return response.json()
                for provider in response.json()['providers']:
                    name = provider['connectName'].lower()
                    home_commcell = provider.get('commcell', {}).get('commCellName')
                    organization_id = provider['shortName']['id']
                    organization_guid = provider['providerGUID']

                    if self._commcell_object.is_global_scope() and "idpCompanyDetails" in provider:
                        # these are dummy (duplicate) organizations meant to proxy idp company on other commcells
                        marked_workloads = self._adv_config.get(name, {}).get('workloads', [])
                        self._adv_config[name] = self._adv_config.get(name, {}) | {
                            'workloads': marked_workloads + [{
                                'id': organization_id,
                                'GUID': organization_guid,
                                'commcell': home_commcell
                            }]
                        }
                        self._adv_config[name]['home_commcell'] = self._adv_config[name].get('home_commcell')
                        # so home_commcell = None indicates this company is an orphaned proxy
                        continue

                    cloud_service_organizations = provider.get("organizationCloudServiceDetails", [{}])[0].\
                        get("cloudService", {}).get('redirectUrl')
                    organizations[name] = organization_id
                    ext_regions = list({
                        region.get('displayName') for region in provider.get('extendedRegions', [])
                    })

                    self._adv_config[name] = self._adv_config.get(name, {}) | {
                        'id': organization_id,
                        'GUID': organization_guid,
                        'redirect_url': cloud_service_organizations,
                        'home_commcell': home_commcell,
                        'extended_regions': ext_regions,
                        'parent_company': provider.get('ownerCompanyName'),
                        'full_name': [contact.get('fullName','') for contact in provider.get('primaryContacts',[])],
                        'flags': provider.get('flags'),
                        'alias': provider.get('shortName', {}).get('domainName'),
                    }
                    if 'workloads' not in self._adv_config[name]:
                        self._adv_config[name]['workloads'] = []

            self._get_associated_entities_count()

            return organizations
        response_string = self._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def _get_associated_entities_count(self) -> None:
        """Gets all the organizations associated with the Commcell environment.

            Returns:
                dict: consists of all organizations added to the commcell

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

    def _get_fl_parameters(self, fl: list = None) -> str:
        """
        Returns the fl parameters to be passed in the mongodb caching api call

        Args:
            fl (list): list of columns to be passed in API request

        Returns:
            str: fl parameter string
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
                fl_parameters = f"fl={default_columns},{','.join(self.valid_columns[column] for column in fl)}"
            else:
                raise SDKException('Organization', '102', 'Invalid column name passed')
        else:
            fl_parameters = f"fl={default_columns},{','.join(column for column in self.valid_columns.values())}"
        return fl_parameters

    def _get_sort_parameters(self, sort: list = None) -> str:
        """
        Returns the sort parameters to be passed in the mongodb caching api call

        Args:
            sort (list): contains the name of the column on which sorting will be performed and type of sort
                                valid sor type -- 1 for ascending and -1 for descending
                                e.g. sort = ['columnName','1']

        Returns:
            str: sort parameter string
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
             fq (list): contains the columnName, condition and value
                    e.g. fq = [['name','contains','test'],['status','eq','ACTIVE']]

        Returns:
            str: fq parameter string
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
            hard (bool): Flag to perform hard refresh on organization cache.
            **kwargs (dict):
                fl    (list): list of columns to return in response (default: None).
                sort  (list): contains the name of the column on which sorting will be performed and type of sort
                                        valid sor type: 1 for ascending and -1 for descending
                                        e.g. sort = ['name','1'] (default: None).
                limit (list): contains the start and limit parameter value
                                        limit = [<startValue>,<limitValue>]
                                        default ['0','25']
                search (str): contains the string to search in the commcell entity cache (default: None).
                fq     (list): contains the columnName, condition and value as a sublist of a list (default: None).
                                        e.g. fq = [['name','contains','test'],['status','equals','active']]
                include_deleted_companies (bool) --  Flag to include deleted companies in the response.

        Returns:
            dict: Dictionary of all the properties present in response.

        Usage:
            # Get organizations cache with default parameters
            orgs_cache = orgs.get_organizations_cache()

            # Get organizations cache with hard refresh
            orgs_cache = orgs.get_organizations_cache(hard=True)

            # Get organizations cache with specific columns, sorting, and limit
            orgs_cache = orgs.get_organizations_cache(fl=['name', 'status'], sort=['name', '1'], limit=['0', '10'])

            # Get organizations cache with search and filter
            orgs_cache = orgs.get_organizations_cache(search='test', fq=[['name', 'contains', 'test'], ['status', 'eq', 'active']])
        """
        # computing params
        fl_parameters = self._get_fl_parameters(kwargs.get('fl', None))
        fq_parameters = self._get_fq_parameters(kwargs.get('fq', None))
        limit = kwargs.get('limit', None)
        limit_parameters = f'&start={limit[0]}&limit={limit[1]}' if limit else ''
        hard_refresh = '&hardRefresh=true' if hard else ''
        sort_parameters = self._get_sort_parameters(kwargs.get('sort', None)) if kwargs.get('sort', None) else ''

        # Search operation can only be performed on limited columns, so filtering out the columns on which search works
        searchable_columns = ["name", "fullName", "providerGUID", "status"]
        search_parameter = (f'&search={",".join(self.valid_columns[col] for col in searchable_columns)}:contains:'
                            f'{kwargs.get("search", None)}') if kwargs.get('search', None) else ''
        params = [
            fl_parameters,
            fq_parameters,
            "&includeDeletedCompanies=true" if kwargs.get('include_deleted_companies', False) else '',
            limit_parameters,
            sort_parameters,
            hard_refresh,
            search_parameter,
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
    def all_organizations_cache(self) -> dict:
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
    def all_organizations(self) -> dict:
        """Returns the dictionary consisting of all the organizations and their info.

            dict - consists of all the organizations configured on the commcell

                {
                    "organization1_name": organization1_id,

                    "organization2_name": organization2_id
                }

        """
        if self._organizations is None:
            self._organizations = self._get_organizations()
        return self._organizations

    @property
    def all_organizations_props(self) -> dict:
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
        if self._adv_config is None:
            self._get_organizations()
        return self._adv_config

    def has_organization(self, name: str) -> bool:
        """Checks if an organization exists in the Commcell with the input organization name.

        Args:
            name (str): name of the organization

        Returns:
            bool: boolean output whether the organization exists in the commcell or not

        Raises:
            SDKException:
                if type of the organization name argument is not string

        Usage:
            organizations.has_organization('MyOrg')
        """
        if not isinstance(name, str):
            raise SDKException('Organization', '101')

        return self._organizations and name.lower() in self._organizations

    def add(self,
            name: str,
            email: str,
            contact_name: str,
            company_alias: str,
            email_domain: Optional[List[str]] = None,
            primary_domain: Optional[str] = None,
            default_plans: Optional[List[str]] = None,
            enable_auto_discover: bool = False,
            service_commcells: Optional[List[str]] = None,
            send_email: bool = False,
            address: Optional[str] = None,
            city: Optional[str] = None,
            country: Optional[str] = None,
            state_or_region: Optional[str] = None,
            postal_code: Optional[str] = None) -> 'Organization':
        """Adds a new organization with the given name to the Commcell.

        Args:
            name             (str): name of the organization to create
            email            (str): email of the primary contact
            contact_name     (str): name of the primary contact
            company_alias    (str): alias of the company
            email_domain     (list): list of email domains supported for the organization
            primary_domain   (str): custom primary domain for organization
            default_plans    (list): list of default plans to be associated with the organization
            enable_auto_discover (bool): enable auto discover for the organization
            service_commcells (list): list of service commmcells to be associated with the organization
            send_email       (bool): If set to true, a welcome email is sent to the primary contact user.
            address          (str): Address of the organization.
            city             (str): City where the organization is located.
            country          (str): Country where the organization is located.
            state_or_region  (str): State or region where the organization is located.
            postal_code      (str): Postal code of the organization's location.

        Returns:
            Organization: instance of the Organization class, for the newly created organization

        Raises:
            SDKException:
                if organization with the given name already exists

                if inputs are not valid

                if failed to create the organization

                if response is empty

                if response is not success

        Usage:
            organizations.add(name='MyOrg', email='test@example.com', contact_name='Test User', company_alias='My Company')
            organizations.add(name='MyOrg', email='test@example.com', contact_name='Test User', company_alias='My Company', email_domain=['example.com'])
            organizations.add(name='MyOrg', email='test@example.com', contact_name='Test User', company_alias='My Company', default_plans=['DefaultPlan'])
            organizations.add(name='MyOrg', email='test@example.com', contact_name='Test User', company_alias='My Company', service_commcells=['ServiceCommcell'])
            organizations.add(name='MyOrg', email='test@example.com', contact_name='Test User', company_alias='My Company', send_email=True)
            organizations.add(name='MyOrg', email='test@example.com', contact_name='Test User', company_alias='My Company', address='123 Main St', city='New York', country='USA', state_or_region='NY', postal_code='10001')
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

        if address is None:
            address = ''

        if city is None:
            city = ''

        if country is None:
            country = ''

        if state_or_region is None:
            state_or_region = ''

        if postal_code is None:
            postal_code = ''

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
                "tenantInfo": {
                    "address": {
                        "address": address,
                        "city": city,
                        "postalCode": postal_code,
                        "state": state_or_region,
                        "country": country
                    }
                },
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
                        self._commcell_object.service_commcells.associations.add(org_object, service_commcells)
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

    def get(self, name: str) -> 'Organization':
        """Returns an instance of the Organization class for the given organization name.

        Args:
            name (str): name of the organization to get the instance of

        Returns:
            Organization: instance of the Organization class for the given organization name

        Raises:
            SDKException:
                if type of the organization name argument is not string

                if no organization exists with the given name

        Usage:
            org = organizations.get('MyOrg')
        """
        if not isinstance(name, str):
            raise SDKException('Organization', '101')

        name = name.lower()

        if self.has_organization(name):
            return Organization(self._commcell_object, name, self._organizations[name])
        raise SDKException('Organization', '103')

    def delete(self, name: str, deactivate: bool = True) -> None:
        """Deletes the organization with the given name from the Commcell.

        Args:
            name       (str): name of the organization to delete
            deactivate (bool): Whether to deactivate organization before deleting, By default organization will be deactivated

        Returns:
            None: if the organization was removed successfully

        Raises:
            SDKException:
                if organization with the given name does not exists

                if failed to delete the organization

                if response is empty

                if response is not success

        Usage:
            organizations.delete('MyOrg')
            organizations.delete('MyOrg', deactivate=False)
        """
        if not self.has_organization(name):
            raise SDKException('Organization', '103')

        if deactivate:
            self.get(name).deactivate()

        organization_id = self._organizations[name.lower()]

        flag, response = self._cvpysdk_object.make_request(
            'DELETE', self._services['ORGANIZATION'] % organization_id
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

    def refresh(self, **kwargs: Dict[str, Any]) -> None:
        """Refresh the list of organization on this commcell.

        Args:
            **kwargs (dict):
                mongodb (bool): Flag to fetch organization cache from MongoDB (default: False).
                hard (bool): Flag to hard refresh MongoDB cache for this entity (default: False).

        Usage:
            organizations.refresh()
            organizations.refresh(mongodb=True)
            organizations.refresh(hard=True, mongodb=True)
        """
        mongodb = kwargs.get('mongodb', False)
        hard = kwargs.get('hard', False)

        self._adv_config = None
        self._organizations = self._get_organizations()
        if mongodb:
            self._organizations_cache = self.get_organizations_cache(hard=hard)

class Organization:
    """Class for performing operations on an Organization.

    Attributes:
        _commcell_object (Commcell): Instance of the Commcell class.
        _cvpysdk_object (CVPySDK): Instance of the CVPySDK class.
        _services (dict): Dictionary of service URLs.
        _update_response_ (method): Method to update the response.
        _organization_name (str): Name of the organization.
        _organization_id (str): ID of the organization.
        _properties (dict): Dictionary of organization properties.
        _organization_info (dict): Dictionary of organization information.
        _user_groups (list): List of user groups associated with the organization.
        _client_groups (list): List of client groups associated with the organization.
        _update_props (dict): Dictionary of properties to be updated.
        _additional_settings (dict): Dictionary of additional settings.
        _tags (list): List of tags associated with the organization.
        _tfa_obj (TwoFactorAuthentication): Instance of the TwoFactorAuthentication class.

    Usage:
        org = Organization(commcell_object, organization_name='MyOrg')
        org = Organization(commcell_object, organization_id=123)
    """

    def __init__(
            self,
            commcell_object: 'Commcell',
            organization_name: str = None,
            organization_id: int = None
        ) -> None:
        """
        Initialise the Client class instance.

        Args:
            commcell_object     (Commcell): Instance of the Commcell class.
            organization_name   (str):      Name of the organization.
                                            default: None, will be fetched using id
            organization_id     (int):      ID of the organization.
                                            default: None, will be fetched using name

        Raises:
            SDKException:
                if neither organization_name nor organization_id is provided.

        Usage:
            org = Organization(commcell_object, organization_name='MyOrg')
            org = Organization(commcell_object, organization_id=123)
        """
        if (organization_id is None) and (organization_name is None):
            raise SDKException('Organization', '101', 'Either organization_name or organization_id must be provided!')

        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._organization_name = organization_name

        if organization_id is not None: # allow org id = 0
            self._organization_id = str(organization_id)
        else:
            self._organization_id = self._get_organization_id()

        self._properties = {}
        self._organization_info = None
        self._user_groups = None
        self._client_groups = None
        self._update_props = {}
        self._additional_settings = None
        self._tags = None
        self._tfa_obj = None
        self.refresh()


    @property
    def tfa(self) -> 'TwoFactorAuthentication':
        """Returns the TwoFactorAuthentication object for this organization.

        Returns:
            TwoFactorAuthentication: The TwoFactorAuthentication object.

        Usage:
            tfa = org.tfa
        """
        if self._tfa_obj is None:
            self._tfa_obj = TwoFactorAuthentication(self._commcell_object, organization_id=self._organization_id)
        return self._tfa_obj


    @property
    def organization_info(self) -> dict:
        """Returns the organization info dictionary.

        Returns:
            dict: Dictionary containing organization information.

        Usage:
            info = org.organization_info
        """
        if self._organization_info is None:
            self._get_properties()
        return self._organization_info


    @property
    def core_info(self) -> dict:
        """Returns the core information of the organization.

        Returns:
            dict: Dictionary containing core information.

        Usage:
            core = org.core_info
        """
        return self.organization_info.get('organization', {})


    @property
    def organization_properties(self) -> dict:
        """Returns the organization properties.

        Returns:
            dict: Dictionary containing organization properties.

        Usage:
            props = org.organization_properties
        """
        return self.organization_info.get('organizationProperties', {})


    @property
    def is_using_upn(self) -> bool:
        """Returns if company uses UPN instead of Email.

        Returns:
            bool: True if company uses UPN, False otherwise.

        Usage:
            upn = org.is_using_upn
        """
        return self.organization_properties.get('useUPNForEmail')


    @is_using_upn.setter
    def is_using_upn(self, value: bool) -> None:
        """Sets company to use UPN instead of Email.

        Args:
            value (bool): True to use UPN, False otherwise.

        Usage:
            org.is_using_upn = True
        """
        self._update_properties_json({'useUPNForEmail': value})
        self._update_properties()


    @property
    def reseller_enabled(self) -> bool:
        """Returns if reseller is enabled.

        Returns:
            bool: True if reseller is enabled, False otherwise.

        Usage:
            enabled = org.reseller_enabled
        """
        return self.organization_properties.get('canCreateCompanies')


    @reseller_enabled.setter
    def reseller_enabled(self, value: bool) -> None:
        """Sets the reseller mode for a company.

        Args:
            value (bool): True to enable reseller mode, False otherwise.

        Usage:
            org.reseller_enabled = True
        """
        self._update_properties_json({'canCreateCompanies': value})
        self._update_properties()


    @property
    def is_data_encryption_enabled(self) -> bool:
        """Returns if owners are allowed to enable data encryption.

        Returns:
            bool: True if data encryption is enabled, False otherwise.

        Usage:
            enabled = org.is_data_encryption_enabled
        """
        return self.organization_properties.get('showDLP')


    def set_data_encryption_enabled(self, value: bool) -> None:
        """Sets property to allow owners to enable data encryption.

        Args:
            value (bool): True to allow data encryption, False otherwise.

        Usage:
            org.set_data_encryption_enabled(True)
        """
        self._update_properties_json({'showDLP': value})
        self._update_properties()


    @property
    def infrastructure_type(self) -> int:
        """Returns infrastructure type.

        Returns:
            int: Infrastructure type.

        Usage:
            infra_type = org.infrastructure_type
        """
        return self.organization_properties.get('infrastructureType')


    @infrastructure_type.setter
    def infrastructure_type(self, value: int) -> None:
        """Sets infrastruture type for a comapny

        Args:
            value (int): id for the infrastructure type

            Rented storage = 0,
            Own Storage = 1,
            Rented and Own Storage  = 2

        Usage:
            org.infrastructure_type = 0
        """
        self._update_properties_json({'infrastructureType': value})
        self._update_properties()


    @property
    def auto_laptop_owners_enabled(self) -> bool:
        """Returns if laptop owners are assigned automatically.

        Returns:
            bool: True if laptop owners are assigned automatically, False otherwise.

        Usage:
            enabled = org.auto_laptop_owners_enabled
        """
        return bool(self.organization_properties.get('autoClientOwnerAssignmentType'))


    def set_auto_laptop_owners(self, client_assign_type: int, client_assign_value: str = None) -> None:
        """Sets the property in company to assign owners to laptop automatically

        Args:
            client_assign_type  (int):  client owner assignment type
            client_assign_value (str):  client owner assignment value

        Usage:
            org.set_auto_laptop_owners(3, 'value')
            org.set_auto_laptop_owners(1)
        """
        if client_assign_type == 3:
            self._update_properties_json({'autoClientOwnerAssignmentType': client_assign_type,
                                          'autoClientOwnerAssignmentValue': client_assign_value})
        else:
            self._update_properties_json({'autoClientOwnerAssignmentType': client_assign_type})

        self._update_properties()


    @property
    def supported_solutions(self) -> int:
        """Returns the supported solutions
        supported solution from API is a integer value and it needs to be changed to a list

        Returns:
            int: Supported solutions.

        Usage:
            solutions = org.supported_solutions
        """
        return self.organization_properties.get('supportedSolutions')


    @supported_solutions.setter
    def supported_solutions(self, value: int) -> None:
        """Sets the supported solution property of a company

        Args:
            value (int): bits converted to int for the supported solutions

        Usage:
            org.supported_solutions = 123
        """
        self._update_properties_json({'supportedSolutions': value})
        self._update_properties()


    @property
    def job_start_time(self) -> str:
        """Returns the job start time for a company or 'System default' if not set.

        Returns:
            str: Job start time or 'System default'.

        Usage:
            start_time = org.job_start_time
        """
        if self.organization_properties.get('isJobStartTimeEnabled'):
            return self.organization_properties.get('jobStartTime')
        else:
            return 'System default'


    @job_start_time.setter
    def job_start_time(self, value: int) -> None:
        """Sets the job start time property for a company

        Args:
            value (int): time to be set for job start time for a company

        Usage:
            org.job_start_time = 123
        """
        self._update_properties_json({'jobStartTime': value})
        self._update_properties()


    def __repr__(self) -> str:
        """Returns the string representation of an instance of this class."""
        return 'Organization class instance for Organization: "{0}"'.format(self.organization_name)


    def _get_organization_id(self) -> str:
        """Gets the id associated with this organization.

        Returns:
            str: id associated with this organization

        Usage:
            org_id = org._get_organization_id()
        """
        organizations = Organizations(self._commcell_object)
        return organizations.get(self.organization_name).organization_id


    def _get_properties(self, **params: dict) -> dict:
        """Gets the properties of this Organization.
        
        Args:
            params (dict): dictionary of query parameters

        Returns:
            dict: dictionary consisting of the properties of this organization

        Raises:
            SDKException:
                if response is empty

                if response is not success

        Usage:
            props = org._get_properties()
            props = org._get_properties(param1='value1', param2='value2')
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
                self._organization_name = self._organization_info['organization'].get('connectName')
                return self._organization_info
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)


    def _get_company_usergroup(self) -> list:
        """Get usergroups associated to a organization

        Returns:
            list: List of user group names.

        Raises:
            SDKException:
                if response is not success.

        Usage:
            user_groups = org._get_company_usergroup()
        """
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


    def get_security_associations(self) -> dict:
        """Get the security associations for a organization

        Returns:
            dict: A dictionary of security associations.
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

        Raises:
            SDKException:
                if response is empty

                if response is not success

        Usage:
            security_associations = org.get_security_associations()
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


    def update_security_associations(self, userOrGroupName: str, roleName: str, request_type: str = None, isUserGroup: bool = False) -> None:
        """
        Updates Security Associations Of an Organisation

        Args:
            userOrGroupName (str):  User or User Group name
            roleName        (str):  eg : 'Alert Owner' or 'Tenant Admin' or 'Tenant Operator' e.t.c
            request_type    (str):  eg : 'OVERWRITE' or 'UPDATE' or 'DELETE', Default will be OVERWRITE operation
            isUserGroup     (bool): True or False. set isUserGroup = True, If input is user group.

        Raises:
            SDKException:
                if Invalid User or User Group is passed as parameter

                if failed to update the properties of the organization

                if response is empty

        Usage:
            org.update_security_associations('user1', 'Alert Owner')
            org.update_security_associations('group1', 'Tenant Admin', isUserGroup=True)
            org.update_security_associations('user2', 'Tenant Operator', request_type='UPDATE')
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


    def _update_properties(self, update_plan_details: bool = False) -> None:
        """Executes the request on the server to update the properties of the organization.

        Args:
            update_plan_details (bool): to update the plan details associated with company

        Raises:
            SDKException:
                if failed to update the properties of the organization

                if response is empty

        Usage:
            org._update_properties()
            org._update_properties(update_plan_details=True)
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


    def _update_properties_json(self, properties_dict: dict) -> None:
        """Update the values of the **organizationProperties** tag in the properties JSON.

        Args:
            properties_dict (dict): dict consisting of the key in properties JSON
                                    to be updated, and the data to be substituted as it's value

        Usage:
            org._update_properties_json({'key': 'value'})
        """
        for key in properties_dict:
            if 'organizationProperties' not in self._update_props:
                self._update_props['organizationProperties'] = {}
            self._update_props['organizationProperties'][key] = properties_dict[key]


    @property
    def name(self) -> str:
        """Returns the Organization display name

        Returns:
            str: Organization display name.

        Usage:
            name = org.name
        """
        return self.organization_info['organization']['connectName']


    @property
    def organization_id(self) -> str:
        """Returns the value of the id for this Organization.

        Returns:
            str: Organization ID.

        Usage:
            org_id = org.organization_id
        """
        return self._organization_id


    @property
    def organization_name(self) -> str:
        """Returns the value of the name for this Organization.

        Returns:
            str: Organization name.

        Usage:
            org_name = org.organization_name
        """
        return self._organization_name.lower()


    @organization_name.setter
    def organization_name(self, value: str) -> None:
        """Method to set organization name

        Args:
            value (str): company name to be set

        Usage:
            org.organization_name = 'New Org Name'
        """
        req_json = {
            "newCompanyName": value
        }

        self._update_props = req_json
        self._update_properties()


    @property
    def description(self) -> str:
        """Returns the description for this Organization.

        Returns:
            str: Organization description.

        Usage:
            desc = org.description
        """
        return self.core_info.get('description')


    @property
    def email_domain_names(self) -> list:
        """Returns the value of the email domain names for this Organization.

        Returns:
            list: List of email domain names.

        Usage:
            domains = org.email_domain_names
        """
        return self.core_info.get('emailDomainNames')


    @email_domain_names.setter
    def email_domain_names(self, value: list) -> None:
        """Method to set supported smtp for this organization

        Args:
            value (list): list of supported smtp to be set

        Usage:
            org.email_domain_names = ['domain1.com', 'domain2.net']
        """
        self._properties['organization']['emailDomainNames'] = value
        self._update_properties()


    @property
    def domain_name(self) -> str:
        """Returns the value of the domain name for this Organization.

        Returns:
            str: Domain name.

        Usage:
            domain = org.domain_name
        """
        return self.core_info.get('shortName', {}).get('domainName')


    @domain_name.setter
    def domain_name(self, value: str) -> None:
        """Method to set domain name for this organization

        Args:
            value (str): company alias to be set

        Usage:
            org.domain_name = 'newalias'
        """
        req_json = {
            "newAliasName": value
        }

        self._update_props = req_json
        self._update_properties()


    @property
    def auth_code(self) -> str:
        """Returns the value of the Auth Code for this Organization.

        Returns:
            str: Auth code.

        Usage:
            code = org.auth_code
        """
        return self.organization_properties.get('authCode')


    @property
    def is_auth_code_enabled(self) -> bool:
        """Returns boolean whether Auth Code generation is enabled for this Organization or not.

        Returns:
            bool: True if auth code generation is enabled, False otherwise.

        Usage:
            enabled = org.is_auth_code_enabled
        """
        return self.organization_properties.get('enableAuthCodeGen')


    @property
    def is_auto_discover_enabled(self) -> bool:
        """Returns boolen whether organization autodiscover attribute enabled for this organization.

        Returns:
            bool: True if autodiscover is enabled, False otherwise.

        Usage:
            enabled = org.is_auto_discover_enabled
        """
        return self._properties['organizationProperties'].get('enableAutoDiscovery', False)


    @property
    def is_backup_disabled(self) -> bool:
        """Returns boolean whether backup is disabled for this organisation

        Returns:
            bool: True if backup is disabled, False otherwise.

        Usage:
            disabled = org.is_backup_disabled
        """
        return self.core_info.get('deactivateOptions', {}).get('disableBackup')


    @property
    def is_restore_disabled(self) -> bool:
        """Returns boolean whether restore is disabled for this organisation

        Returns:
            bool: True if restore is disabled, False otherwise.

        Usage:
            disabled = org.is_restore_disabled
        """
        return self.core_info.get('deactivateOptions', {}).get('disableRestore')


    @property
    def is_login_disabled(self) -> bool:
        """Returns boolean whether login is disabled for this organisation

        Returns:
            bool: True if login is disabled, False otherwise.

        Usage:
            disabled = org.is_login_disabled
        """
        # organization['deactivateOptions']['disableLogin']
        return self.core_info.get('deactivateOptions', {}).get('disableLogin')

    def password_age_days(self) -> int:
        """Returns the password age days for the organisation

        Returns:
            int: The password age days.
        """
        return self.organization_properties.get('agePasswordDays', 0)


    @property
    def is_download_software_from_internet_enabled(self) -> bool:
        """Returns boolean indicating whether download software from the internet is enabled

        Returns:
            bool: True if downloading software from the internet is enabled, False otherwise.
        """
        return bool(
            self.organization_properties.get('clientGroupForceClientSideDownload')
        )


    @property
    def shared_laptop(self) -> bool:
        """Returns boolean whether Shared Laptop Usage is enabled for this Organization or not.

        Returns:
            bool: True if Shared Laptop Usage is disabled, False if enabled.
        """
        return not self.organization_info['organizationProperties'].get('preferenceMachineCentricClient', True)


    @shared_laptop.setter
    def shared_laptop(self, value: bool) -> None:
        """Sets Shared Laptop Usage for this Organization

        Args:
            value (bool): True/False
                False: Enable Shared Laptop usage
                True: Disable Shared Laptop usage

        Returns:
            None

        Usage:
            org.shared_laptop = False
        """
        self._update_properties_json({'preferenceMachineCentricClient': not value})
        self._update_properties()


    @property
    def machine_count(self) -> int:
        """Returns the count of machines added to this Organization.

        Returns:
            int: The count of machines.
        """
        return self.organization_properties.get('totalMachineCount')


    @property
    def user_count(self) -> int:
        """Returns the count of Users added to this Organization.

        Returns:
            int: The count of users.
        """
        return self.organization_properties.get('userCount')


    @property
    def contacts(self) -> list[str]:
        """Returns the Primary Contacts for this Organization.

        Returns:
            list[str]: List of usernames of the primary contacts.
        """
        return [
            contact.get('user', {}).get('userName')
            for contact in self.organization_properties.get('primaryContacts', [])
        ]


    @contacts.setter
    def contacts(self, user_names: list[str]) -> None:
        """
        Sets Contact details for organization.
        User should be present in tenant admin group of the organization

        Args:
            user_names (list[str]): List of usernames

        Raises:
            SDKException:
                If input parameter is not list

                If Input list is empty

        Usage:
            org.contacts = ['user1', 'user2']
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
            list[tuple[str, str]]: list of (operator, role) tuple pairs

        Usage:
            operators = org.operators
            # Returns:
            # [
            #     ('<user name>', '<role name>'),
            #     ('<usergroup name>', '<role name>'),
            #     ...
            # ]
        """
        return sorted([
            (
                op.get('user', {}).get('userName') or op.get('userGroup', {}).get('userGroupName'),
                op.get('role', {}).get('roleName')
            ) for op in self.organization_properties.get("operators", [])
        ])


    def _lookup_operator(self, user_or_group: Union[str, 'User', 'UserGroup'], role: Union[str, 'Role']) -> dict:
        """
        Gets the user id role id full dictionary for given user/group and role
        from existing operators in the organization

        Args:
            user_or_group (Union[str, User, UserGroup]): User or UserGroup name or SDK object
            role (Union[str, Role]): Role name or Role SDK object

        Returns:
            dict: Operator dictionary if found, empty dictionary otherwise.
        """
        if isinstance(user_or_group, User):
            user_or_group = user_or_group.user_name
        if isinstance(user_or_group, UserGroup):
            user_or_group = user_or_group.user_group_name
        if isinstance(role, Role):
            role = role.role_name

        for operator in self.organization_properties.get("operators", []):
            this_role = operator.get('role', {}).get('roleName')
            this_user_or_group = (operator.get('user', {}).get('userName') or
                                  operator.get('userGroup', {}).get('userGroupName'))
            if this_role == role and this_user_or_group == user_or_group:
                return operator
        return {}


    def _prepare_operator_dict(self, user_or_group: Union[str, 'User', 'UserGroup'], role: Union[str, 'Role']) -> dict:
        """
        Prepares the operator dictionary for given user/group and role

        Args:
            user_or_group (Union[str, User, UserGroup]): User or UserGroup name or SDK object
            role (Union[str, Role]): Role name or Role SDK object

        Returns:
            dict: Dictionary containing user/group and role information
            to pass as payload
        """
        # prefer using existing operator if present (to avoid errors during multi-commcell calls)
        if existing_operator := self._lookup_operator(user_or_group, role):
            return existing_operator

        # convert user, role to SDK objects
        if isinstance(user_or_group, str):
            self._commcell_object.users.refresh()
            self._commcell_object.user_groups.refresh()
            if self._commcell_object.users.has_user(user_or_group):
                user_or_group = self._commcell_object.users.get(user_or_group)
            elif self._commcell_object.user_groups.has_user_group(user_or_group):
                user_or_group = self._commcell_object.user_groups.get(user_or_group)
            else:
                raise SDKException('Organization', '110', f'Invalid User or User Group name: {user_or_group}')
        if isinstance(role, str):
            self._commcell_object.roles.refresh()
            role = self._commcell_object.roles.get(role)


        op_dict = {"role": {"roleName": role.role_name, "roleId": int(role.role_id)}}

        if isinstance(user_or_group, User):
            op_dict['user'] = {
                "userName": user_or_group.user_name,
                "userId": int(user_or_group.user_id)
            }
        elif isinstance(user_or_group, UserGroup):
            op_dict['userGroup'] = {
                "userGroupName": user_or_group.user_group_name,
                "userGroupId": int(user_or_group.user_group_id)
            }
        else:
            raise SDKException('Organization', '110', f'Invalid User or User Group object: {user_or_group}')
        return op_dict


    def _prepare_operators_payload(self, operator_list: list[tuple[Union[str, 'User', 'UserGroup'], Union[str, 'Role']]]) -> dict:
        """
        Prepares the operators payload for given operator list

        Args:
            operator_list (list[tuple[Union[str, User, UserGroup], Union[str, Role]]]): list of (userOrGroup, role) tuple pairs

        Returns:
            dict: List of dictionaries containing user/group and role information
        """
        return {
            "organizationInfo": {
                "organization": {
                    "shortName": {"domainName": self.name, "id": int(self.organization_id)}
                },
                "organizationProperties": {
                    "operatorsOperationType": 1,
                    "operators": [
                        self._prepare_operator_dict(ug, role)
                        for ug, role in operator_list
                    ]
                },
            }
        }


    @operators.setter
    def operators(self, operator_list: list[tuple[Union[str, 'User', 'UserGroup'], Union[str, 'Role']]]) -> None:
        """
        Overwrites the operator:role associations of the organization

        Args:
            operator_list (list[tuple[Union[str, User, UserGroup], Union[str, Role]]]): list of (userOrGroup, role) tuple pairs

            [
                ('<user name>', '<role name>'),
                ('<usergroup name>', '<role name>'),
                ...
            ]
            They can be User and Role SDK objects as well

        Returns:
            None

        Raises:
            SDKException:
                if failed to update the properties of the organization

                if response is empty

        Usage:
            org.operators = [('user1', 'Role1'), ('group1', 'Role2')]
        """
        self._commcell_object.wrap_request(
            'PUT', 'UPDATE_ORGANIZATION', (self.organization_id,),
            {'payload': self._prepare_operators_payload(operator_list)},
            sdk_exception=('Organization', '110')
        )
        self.refresh()


    def manage_operators(self, operator_list: list[tuple[Union[str, 'User', 'UserGroup'], Union[str, 'Role']]]) -> None:
        """
        Similar to operators setter, but uses manage operators API v4/Company/Operators,
        to set the operators for the organization

        Args:
            operator_list (list[tuple[Union[str, User, UserGroup], Union[str, 'Role']]]): list of (userOrGroup, role) tuple pairs

            [
                ('<user name>', '<role name>'),
                ('<usergroup name>', '<role name>'),
                ...
            ]
            They can be User and Role SDK objects as well

        Returns:
            None

        Raises:
            SDKException:
                if failed to update the properties of the organization

                if response is empty

        Usage:
            org.manage_operators = [('user1', 'Role1'), ('group1', 'Role2')]
        """
        payload = self._prepare_operators_payload(operator_list)
        payload["organizationInfo"]["organizationProperties"]["operatorsOperationType"] = "OVERWRITE"
        self._commcell_object.wrap_request(
            'PUT', 'COMPANY_OPERATORS',
            req_kwargs={'payload': payload},
            sdk_exception=('Organization', '110')
        )
        self.refresh()


    @property
    def contacts_fullname(self) -> list[str]:
        """ Returns Primary Contacts full name for the organization

        Returns:
            list[str]: List of full names of the primary contacts.
        """
        return [
            contact['fullName']
            for contact in self.organization_properties.get('primaryContacts', [])
        ]


    @property
    def default_plan(self) -> list[str]:
        """Returns the Default Plans associated to this Organization.

        Returns:
            list[str]: List of default plan names.
        """
        return [
            plan['plan']['planName']
            for plan in self.organization_properties.get('defaultPlans', [])
        ]


    @default_plan.setter
    def default_plan(self, value: Union[dict, str]) -> None:
        """
        Updates default plan for Organization

        Args:
            value (Union[dict, str]): Dictionary consisting Server or Laptop Plan or plan name

            example:
            value = {
                'Server Plan' : 'Server Plan Name',
                'Laptop Plan' : 'Laptop Plan Name'
            }

        Raises:
            SDKException:
                If plan doesnot exist on Commcell

                If plan is not associated with company

        Usage:
            org.default_plan = {'Server Plan': 'ServerPlan1', 'Laptop Plan': 'LaptopPlan1'}
            org.default_plan = 'ServerPlan1'
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
    def plans(self) -> list[str]:
        """Returns the Plans associated to this Organization.

        Returns:
            list[str]: List of plan names.
        """
        return [
            plan['plan']['planName'].lower()
            for plan in self.organization_info.get('planDetails', [])
        ]


    @property
    def plan_details(self) -> list[dict]:
        """Returns the jobstarttime of a plan associated with a company

        Returns:
            list[dict]: List of plan details.
        """
        return self.organization_info.get('planDetails')


    @property
    def server_count(self) -> int:
        """Returns the server count associated with a company

        Returns:
            int: The server count.
        """
        return self.organization_properties.get('serverCount')


    @property
    def sender_name(self) -> str:
        """Returns sender name

        Returns:
            str: The sender name.
        """
        return self.organization_properties.get('senderName', '')


    @sender_name.setter
    def sender_name(self, sender_name: str) -> None:
        """Sets the email Sender Name

        Args:
            sender_name (str): The sender name to set.

        Returns:
            None

        Usage:
            org.sender_name = 'New Sender Name'
        """
        self._update_properties_json({'senderName': sender_name})
        self._update_properties()


    @property
    def sender_email(self) -> str:
        """Returns sender email

        Returns:
            str: The sender email.
        """
        return self.organization_properties.get('senderSmtp', '')


    @sender_email.setter
    def sender_email(self, sender_email: str) -> None:
        """Sets Sender Email adress

        Args:
            sender_email (str): The sender email address to set.

        Returns:
            None

        Usage:
            org.sender_email = 'sender@example.com'
        """
        self._update_properties_json({'senderSmtp': sender_email})
        self._update_properties()


    def update_email_settings(self, email_settings: dict) -> None:
        """
        Updates Email Settings of an organisation

        Args:
            email_settings (dict): Dictionary consisting of sender name and email

            example:
            email_settings = {
                'sender_name' : 'name',
                'sender_email' : 'email'
            }

        Raises:
            SDKException:
                if sender_name or sender_email is missing in inputs

        Usage:
            org.update_email_settings({'sender_name': 'Sender Name', 'sender_email': 'sender@example.com'})
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
    def user_groups(self) -> List['UserGroup']:
        """Returns the user group associated with a company

        Returns:
            list[UserGroup]: List of user groups.
        """
        return self._user_groups


    @property
    def organization_created_on(self) -> str:
        """ Returns the company creation time

        Returns:
            str: Formatted string representing the company creation time.
        """
        time_epoch = self.organization_properties.get('orgCreationDateTime')
        return (
            datetime.fromtimestamp(time_epoch).strftime("%b %#d") +
            (
                datetime.fromtimestamp(time_epoch).strftime(" %Y")
                if datetime.now().year != datetime.fromtimestamp(time_epoch).year
                else ''
            ) + datetime.fromtimestamp(time_epoch).strftime(", %#I:%M %p")
        )


    @property
    def file_exceptions(self) -> Dict[str, list[str]]:
        """ Returns the file exceptions for a company

        Returns:
            dict[str, list[str]]: Dictionary of file exceptions, keyed by OS type.
        """
        os_type_map = {
            1: 'Windows',
            2: 'Unix'
        }
        file_exceptions = {}
        for file_filter in self.organization_properties['globalFiltersInfo']['globalFiltersInfoList']:
            file_exceptions[os_type_map[file_filter['operatingSystemType']]] = \
                file_filter['globalFilters'].get('filters', [])
        return file_exceptions


    @file_exceptions.setter
    def file_exceptions(self, value: tuple[dict[str, list[str]], str]) -> None:
        """
        This sets Global File Exceptions at Company Level, Individually File Exceptions for Windows or Unix can be set

        file_exceptions = filters, 'OVERWRITE'   It will overwrite with the keys which are present in filters dict.
        file_exceptions = filters, 'UPDATE'      It will update the keys which are present in filters dict.

        Args:
            value (tuple[dict[str, list[str]], str]): (filters, Operation_Type)

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

        Usage:
            org.file_exceptions = ({'Windows': ['*.py'], 'Unix': ['*.exe']}, 'OVERWRITE')
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
    def is_global_file_exceptions_enabled(self) -> bool:
        """ Returns if file exception is enabled

        Returns:
            bool: True if file exception is enabled, False otherwise.
        """
        return self.organization_properties.get('useCompanyGlobalFilter')


    @plans.setter
    def plans(self, value: list[Union[str, dict]]) -> None:
        """Update the list of plans associated with the Organization.

            Args:
                value (list[Union[str, dict]]): list of plans

            Returns:
                None

        Usage:
            org.plans = ['Plan1', 'Plan2']
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
    def is_company_privacy_enabled(self) -> bool:
        """Returns true if company privacy is enabled

        Returns:
            bool: True if company privacy is enabled, False otherwise.
        """
        return (
            self.organization_properties.get('privacy') or {}
        ).get("enableDataSecurity")


    @property
    def is_owner_data_privacy_enabled(self) -> bool:
        """Returns true if owner data privacy is enabled

        Returns:
            bool: True if owner data privacy is enabled, False otherwise.
        """
        return self.organization_properties.get("allowUsersToEnablePrivacy")


    @property
    def user_session_timeout(self) -> int:
        """Returns company user session timeout value

        Returns:
            int: The user session timeout in minutes.
        """
        return self.organization_properties.get("loginSessionTimeoutInMinutes")

    @user_session_timeout.setter
    def user_session_timeout(self, value: int) -> None:
        """Sets user session timeout

        Args:
            value (int): timeout time in minutes
        Usage:
            org.user_session_timeout = 30
        """
        self._update_properties_json({'loginSessionTimeoutInMinutes': value})
        self._update_properties()

    def dissociate_plans(self, value: list) -> None:
        """disassociates plans from the organization

        Args:
            value (list): list of plans

        Returns:
            None

        Raises:
            SDKException:
                -   if the 'value' is not a list.
                -   if the plan does not exist on the Commcell.

        Usage:
            org.dissociate_plans(['plan1', 'plan2'])
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

    def refresh(self, **params: dict) -> None:
        """Refresh the properties of the Organization.

        Args:
            params (dict): dictionary of query parameters
        Usage:
            org.refresh()
            org.refresh(param1='value1', param2='value2')
        """
        self._update_props['organizationProperties'] = {}
        self._properties = self._get_properties(**params)
        self._user_groups = self._get_company_usergroup()
        self._additional_settings = None
        self._tags = None
        self._commcell_object.organizations.refresh()
        if self._tfa_obj:
            self._tfa_obj.refresh()

    def enable_auth_code(self) -> str:
        """Executes the request on the server to enable Auth Code Generation for the Organization.

        Refresh the Auth Code if Auth Code generation is already enabled for the Organization.

        Args:
            None

        Returns:
            str: auth code generated from the server

        Raises:
            SDKException:
                -   if failed to enable auth code generation
                -   if response is empty
                -   if response is not success

        Usage:
            auth_code = org.enable_auth_code()
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

    def disable_auth_code(self) -> None:
        """Executes the request on the server to disable Auth Code Generation for the Organization.

        Args:
            None

        Returns:
            None

        Raises:
            SDKException:
                -   if failed to disable auth code generation
                -   if response is empty
                -   if response is not success

        Usage:
            org.disable_auth_code()
        """
        try:
            self._update_properties_json({'enableAuthCodeGen': False})
            self._update_properties()
        except KeyError:
            raise SDKException('Organization', '109')

    @property
    def tenant_operator(self) -> dict:
        """Returns the operators associated to this organization

        Returns:
            dict: A dictionary containing lists of users and user groups associated with the organization.
                  Example: {'Users': ['user1', 'user2'], 'User Group': ['group1', 'group2']}

        Usage:
            operators = org.tenant_operator
        """
        tenant_operators = self.organization_info.get('organizationProperties', {}).get('operators', [])
        user_list = []
        usergroup_list = []
        for role in tenant_operators:
            if 'user' in role:
                user_list.append(role['user']['userName'])
            else:
                usergroup_list.append(role['userGroup']['userGroupName'])

        operators = {'Users': user_list, 'User Group': usergroup_list}
        return operators

    def add_user_groups_as_operator(self, user_group_list: list, request_type: str) -> None:
        """Update the local user_group as tenant operator of the company

        Args:
            user_group_list (list): user group list
            request_type    (str): decides whether to UPDATE, DELETE or OVERWRITE user_group
                                     security association

        Raises:
            SDKException: If the user_group is not an instance of UserGroup and cannot be retrieved.

        Usage:
            org.add_user_groups_as_operator(['user_group1', 'user_group2'], 'UPDATE')
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

    def add_users_as_operator(self, user_list: list, request_type: str) -> None:
        """Update the local user as tenant operator of the company

        Args:
            user_list    (list): list of users
            request_type (str): decides whether to UPDATE, DELETE or
                                  OVERWRITE user security association

        Raises:
            SDKException: If the user is not an instance of User and cannot be retrieved.

        Usage:
            org.add_users_as_operator(['user1', 'user2'], 'UPDATE')
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
    def operator_role(self) -> str:
        """Returns the operator role associated to this organization

        Returns:
            str: The name of the operator role.

        Usage:
            role = org.operator_role
        """
        return self.organization_properties.get('operatorRole', {}).get('roleName')

    @operator_role.setter
    def operator_role(self, role_name: str) -> None:
        """Updates the role associated with a tenant operator

        Args:
            role_name (str): Role name to be associated

        Usage:
            org.operator_role = 'NewRole'
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

    def activate(self) -> None:
        """
        To activate the organization

        Args:
            None

        Returns:
            None

        Raises:
            SDKException:
                -   if failed to activate the organization
                -   if response is empty
                -   if response is not success

        Usage:
            org.activate()
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
        self.refresh()

    def deactivate(self,
                   disable_backup: bool = True,
                   disable_restore: bool = True,
                   disable_login: bool = True) -> None:
        """
        To deactivate the organization

        Args:
            disable_backup  (bool): To disable backup
                                     default: True
            disable_restore (bool): To disable restore
                                     default: True
            disable_login   (bool): To disable login
                                     default: True

        Returns:
            None

        Raises:
            SDKException:
                -   if failed to deactivate the organization
                -   if response is empty
                -   if response is not success

        Usage:
            org.deactivate()
            org.deactivate(disable_backup=False, disable_restore=False, disable_login=False)
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

    def lock(self) -> None:
        """
        Lock the organization to disable user logins and terminate existing sessions.

        This operation will:
        - Disable all user logins for the organization
        - Terminate all existing user sessions
        - Kill any running restore jobs
        - Prevent new restore operations (backups continue unaffected)

        Args:
            None

        Returns:
            None

        Raises:
            SDKException:
                - if failed to lock the organization
                - if response is empty
                - if response is not success

        Usage:
            org.lock()
        """
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['LOCK_ORGANIZATION'] % self.organization_id
        )

        if flag:
            if response.json():
                error_code = response.json().get('response', {}).get('errorCode', 0)
                if error_code != 0:
                    error_message = response.json().get('error', {}).get('errorMessage', 'Unknown error')
                    raise SDKException(
                        'Organization', '102', f'Failed to lock organization. Error: "{error_message}"'
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    def unlock(self) -> None:
        """
        Unlock the organization to restore normal operations.

        This operation will:
        - Re-enable user logins for the organization
        - Allow new user sessions
        - Re-enable restore operations

        Args:
            None

        Returns:
            None

        Raises:
            SDKException:
                - if failed to unlock the organization
                - if response is empty
                - if response is not success

        Usage:
            org.unlock()
        """
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['UNLOCK_ORGANIZATION'] % self.organization_id
        )

        if flag:
            if response.json():
                error_code = response.json().get('response', {}).get('errorCode', 0)
                if error_code != 0:
                    error_message = response.json().get('error', {}).get('errorMessage', 'Unknown error')
                    raise SDKException(
                        'Organization', '102', f'Failed to unlock organization. Error: "{error_message}"'
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    @property
    def is_locked(self) -> bool:
        """
        Returns whether the organization is currently locked.

        Returns:
            bool: True if the organization is locked, False otherwise.

        Usage:
            if org.is_locked:
                print("Organization is locked")
        """
        return 7 == self._organization_info.get('organization', {}).get('status', 0)

    def set_country(self, country_name: str) -> None:
        """Sets the country association for this organization.

        Args:
            country_name (str): Name of the country to associate with the organization
                               (e.g., 'United States', 'Canada', etc.)

        Raises:
            SDKException:
                if failed to set country for the organization
                if response is empty
                if response is not success

        Usage:
            org.set_country('United States')
            org.set_country('Canada')
        """
        request_json = {
            'companyId': int(self.organization_id),
            'countryName': country_name
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['SET_COMPANY_COUNTRY'], request_json
        )

        if flag:
            if response.json():
                response_data = response.json()
                error_code = response_data.get('errorCode', 0)

                if error_code != 0:
                    error_message = response_data.get('errorMessage', 'Unknown error')
                    raise SDKException(
                        'Organization', '102', f'Error: "{error_message}"'
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    def verify_owner_assignment_config(self, want_ownership_type: int) -> None:
        """ Verifies that the ownership assignments settings are configured and set properly for company

        Args:
            want_ownership_type (int): Option number for ownership assignment type

        Raises:
            SDKException:
                -   if response is empty
                -   if response is not success
                -   if ownership assignment is not correct

        Usage:
            org.verify_owner_assignment_config(1)
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

    def enable_auto_discover(self) -> None:
        """Enables autodiscover at company level.

        Raises:
            SDKException: if failed to update enableAutoDiscovery property

        Usage:
            org.enable_auto_discover()
        """
        self._update_properties_json({'enableAutoDiscovery': True})
        self._update_properties()

    def disable_auto_discover(self) -> None:
        """Disables autodiscover at company level.

        Raises:
            SDKException: if failed to update enableAutoDiscovery property

        Usage:
            org.disable_auto_discover()
        """
        self._update_properties_json({'enableAutoDiscovery': False})
        self._update_properties()

    def set_auto_discover(self, value: bool) -> None:
        """Sets autodiscover at company level.

        Args:
            value (bool): True to enable, False to disable

        Raises:
            SDKException: if failed to update enableAutoDiscovery property

        Usage:
            org.set_auto_discover(True)
            org.set_auto_discover(False)
        """
        self._update_properties_json({'enableAutoDiscovery': value})
        self._update_properties()

    def add_client_association(self, client_name: str) -> None:
        """To associate a client to an organization

        Args:
            client_name (str): name of the client which has to be associated to organization

        Raises:
            SDKException:
                -   if client association to organization fails
                -   if response is empty
                -   if response is not success

        Usage:
            org.add_client_association('client1')
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

    def remove_client_association(self, client_name: str) -> None:
        """To de-associate a client to an organization

        Args:
            client_name (str): name of the client which has to be associated to organization

        Raises:
            SDKException:
                -   if client de-association to organization fails
                -   if response is empty
                -   if response is not success

        Usage:
            org.remove_client_association('client1')
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
    def is_tfa_enabled(self) -> bool:
        """returns the status of two factor authentication (True/False)

        Returns:
            bool: True if two-factor authentication is enabled, False otherwise.

        Usage:
            is_enabled = org.is_tfa_enabled
        """
        return self.tfa.is_tfa_enabled

    @property
    def tfa_enabled_user_groups(self) -> list:
        """returns the list of user group names for which tfa is enabled. only for group inclusion tfa

        Returns:
            list: A list of user group names for which TFA is enabled.

        Usage:
            groups = org.tfa_enabled_user_groups
        """
        return self.tfa.tfa_enabled_user_groups

    def enable_tfa(self, user_groups: list = None, otp: str = None) -> None:
        """
        Enables two factor authentication for the oganization.

        Args:
             user_groups (list): list of user group names for which tfa needs to be enabled.
             otp (str): otp for two-factor authentication operation.
        Returns:
            None

        Usage:
            org.enable_tfa()
            org.enable_tfa(user_groups=['group1', 'group2'])
        """
        self.tfa.enable_tfa(user_groups=user_groups, otp=otp)

    def disable_tfa(self, otp: str = None) -> None:
        """
        Disables two factor authentication for the organization

        Args:
            otp (str): otp for two-factor authentication operation.

        Returns:
            None

        Usage:
            org.disable_tfa()
        """
        self.tfa.disable_tfa(otp=otp)

    @property
    def client_groups(self) -> dict:
        """returns all the clientgroups associated with the organization

        Returns:
            dict: consists of all clientgroups associated to an organization
                  {
                       "clientgroup1_name": clientgroup1_id,
                       "clientgroup2_name": clientgroup2_id,
                  }

        Raises:
            SDKException:
                -   if response is empty
                -   if response is not success

        Usage:
            client_groups = org.client_groups
        """
        if self._client_groups is None:
            query_params = f"?fq=companyId%3Aeq%3A{self._organization_id}&fl=groups.clientGroup%2Cgroups.Id%2Cgroups.name"

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'GET', self._services['SERVERGROUPS_V4'] + query_params
            )  # fetch all client groups associated with the organization

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

    def get_alerts(self) -> List[str]:
        """
        Get all the alerts associated to organization

        Returns:
            list[str]: List of alert names associated with the organization. Returns an empty list if no alerts are found.

        Raises:
            SDKException:
                if response is empty

                if response is not success

        Usage:
            alerts = org.get_alerts()
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

    def enable_company_data_privacy(self) -> None:
        """To enable company privacy to prevent admin access to company data

        Usage:
            org.enable_company_data_privacy()
        """
        if self.is_company_privacy_enabled:
            return

        self.set_company_data_privacy(True)

    def disable_company_data_privacy(self) -> None:
        """To disable company privacy to prevent admin access to company data

        Usage:
            org.disable_company_data_privacy()
        """
        if not self.is_company_privacy_enabled:
            return

        self.set_company_data_privacy(False)

    def set_company_data_privacy(self, value: bool) -> None:
        """Method to set company data privacy

        Args:
            value (bool): True/False to enable/disable privacy
        Raises:
            SDKException:
                if disable company data privacy to service commcell fails
                if response is empty
                if response is not success

        Usage:
            org.set_company_data_privacy(True)
            org.set_company_data_privacy(False)
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
    def get_retire_laptop_properties(self) -> dict:
        """
        Returns:
            dict: Retire Laptop Properties of Organization

            example: {
                    "retireDevicesAfterDays": 183,
                    "forceDeleteDevicesAfterDays": -1
            }

        Usage:
            properties = org.get_retire_laptop_properties
        """
        return self.organization_properties.get('autoRetireDevices', {})

    def retire_offline_laptops(self, retire_days: int, delete_days: Optional[int] = None) -> None:
        """
        The number of days specified to retire laptops must be less than or equal to the number of days specified to delete laptops
        If delete_days is not specified, It will be set to 'Never'

        Args:
            retire_days (int):  Number of days to retire laptops
            delete_days (int):  Number of days to delete laptops

        Raises:
            SDKException:
                If retire days is more than delete days

        Usage:
            org.retire_offline_laptops(retire_days=90, delete_days=180)
            org.retire_offline_laptops(retire_days=90)
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
    def sites(self) -> dict:
        """
        Gets the site information of organisation

        Returns:
            dict: sites information of organisation

        Usage:
            sites = org.sites
        """
        return {
            'primary_site': self.organization_properties.get('primaryDomain', ''),
            'additional_sites': self.organization_properties.get('additionalDomains', [])
        }

    @sites.setter
    def sites(self, sites: dict) -> None:
        """
        Updates Sites information for an Organisation

        Args:
            sites (dict):  Consisting Of Primary and Additional sites information, Pass Empty dictionary to remove site information

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

        Usage:
            sites = {'primary_site': 'comm.com', 'additional_sites': ["cv.comm.com", "skhk.comm.com"]}
            org.sites = sites
            org.sites = {}
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

    def _get_tags(self) -> list[dict]:
        """
        Fetches the tags associated with the organization.

        Returns:
            list[dict]: List of tag dicts as returned by API

        Raises:
            SDKException:
                if response is empty

                if response is not success

        Usage:
            tags = org._get_tags()
        """
        with self._commcell_object.wrapped_request(
            'GET', 'GET_ORGANIZATION_TAGS', (self.organization_id,)
        ) as response:
            return response.get('tags', [{}])[0].get('tag', [])

    @property
    def tags(self) -> dict[str, str]:
        """
        Returns:
            dict[str, str]: dict with tag name as key and tag value as value

        Raises:
                SDKException:
                    if response is empty

                    if response is not success

        Usage:
            tags = org.tags
        """
        if self._tags is None:
            self._tags = self._get_tags()
        return {
            tag['name']: tag.get('value', '')
            for tag in self._tags
        }

    def _prepare_tag_dict(self, tag_name: str, tag_value: str) -> dict[str, str]:
        """
        Prepares a tag dictionary with name and value.

        Args:
            tag_name (str): The name of the tag.
            tag_value (str): The value of the tag.

        Returns:
            dict[str, str]: A dictionary with 'name' and 'value' keys.

        Usage:
            tag_dict = org._prepare_tag_dict('tag1', 'value1')
        """
        _ = self.tags
        for tag in self._tags:
            if tag['name'] == tag_name:
                # keep existing tag ID, if present
                return tag | {'value': tag_value}
        return {
            'name': tag_name,
            'value': tag_value
        }

    @tags.setter
    def tags(self, tags_dict: dict[str, str]) -> None:
        """
        Updates Tags for an Organisation

        Args:
            tags_dict (dict):  Consisting of tag name as key and tag value as value
            Example: {
                'tag1': 'value1',
                'tag2': ''
            }

        Raises:
            SDKException:
                If it fails to Update Tags for an Organisation

        Usage:
            tags_dict = {'tag1': 'value1', 'tag2': ''}
            org.tags = tags_dict
        """
        tag_list = [
            self._prepare_tag_dict(tag_name, tag_value)
            for tag_name, tag_value in tags_dict.items()
        ]
        req_json = {
            "entityTag": [
                {
                    "entityId": int(self.organization_id),
                    "entityType": 61,
                    "tag": tag_list
                }
            ]
        }
        self._commcell_object.wrap_request(
            'PUT', 'ORGANIZATION_TAGS',
            req_kwargs={'payload': req_json},
            sdk_exception=('Organization', '110')
        )
        self._tags = None

    @property
    def isPasskeyEnabled(self) -> bool:
        """Returns True if Passkey is enabled on company

        Usage:
            is_enabled = org.isPasskeyEnabled
        """
        return self.organization_properties.get(
            'advancedPrivacySettings', {}
        ).get('authType') == 2

    @property
    def isAuthrestoreEnabled(self) -> Optional[bool]:
        """Returns True if Authrestore is enabled on company

        Usage:
            is_enabled = org.isAuthrestoreEnabled
        """
        return self.organization_properties.get(
            'advancedPrivacySettings', {}
        ).get('passkeySettings', {}).get('enableAuthorizeForRestore')

    @property
    def isAllowUsersToEnablePasskeyEnabled(self) -> Optional[bool]:
        """Returns True if it is enabled

        Usage:
            is_enabled = org.isAllowUsersToEnablePasskeyEnabled
        """
        return self.organization_properties['allowUsersToEnablePasskey']

    @property
    def company_theme(self) -> dict:
        """
        Returns:
            dict: the company level theme colors set, empty dict if no company level theme set

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

        Raises:
            SDKException:
                If the response contains an error.
                If the response is empty.

        Usage:
            theme = org.company_theme
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
    def company_theme(self, theme_colors: dict) -> None:
        """
        Sets company level theme for an Organisation

        Args:
            theme_colors (dict): with color setting name as key and color hex as value

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

        Usage:
            theme_colors = {
                'loginAndBannerBg': '#0B2E44',
                'headerColor': '#DDE5ED',
                'headerTextColor': '#0B2E44',
                'navBg': '#FFFFFF',
                'navIconColor': '#0b2e44',
                'pageHeaderText': '#0B2E44',
                'actionBtnBg': '#0B2E44',
                'actionBtnText': '#eeeeee',
                'linkText': '#4B8DCC',
                'iconColor': '#0B2E44'
            }
            org.company_theme = theme_colors
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

    def passkey(self, current_password: str, action: str, new_password: Optional[str] = None) -> None:
        """
        Updates Passkey properties of an Organisation

        Args:
            current_password (str):  User Current Passkey to perform actions
            action           (str):  'enable' | 'disable' | 'change passkey' | 'authorise'
            new_password     (str):  Resetting existing Passkey

        Raises:
            SDKException:
                if invalid action is passed as a parameter

                if request fails to update passkey properties of  an organisation

                if new password is missing while changing passkey

        Usage:
            org.passkey(current_password='old_pass', action='disable')
            org.passkey(current_password='old_pass', action='change passkey', new_password='new_pass')
            org.passkey(current_password='auth_pass', action='authorise')
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

    def configure_breakglass_account(
            self,
            password: str,
            user_name: Optional[str] = None,
            force_reset: bool = False,
            is_password_encoded: bool = False
    ) -> dict:
        """Configures Break Glass Account for an organization.

        Args:
            password (str): Break glass account password. Plain text by default.
            user_name (Optional[str]): Existing break glass username. Ignored when force_reset is True.
            force_reset (bool): If True, calls API with forceReset=true and sends userName as null.
            is_password_encoded (bool): Set to True if password is already base64 encoded.

        Returns:
            dict: API response payload.

        Example:
            org.configure_breakglass_account(password='6Cap_6Small_6Symbol_6Num', user_name='bga_testuser')
            org.configure_breakglass_account(password='6Cap_6Small_6Symbol_6Num', force_reset=True)
        """
        if not isinstance(password, str):
            raise SDKException('Organization', '101', 'password must be a string')

        if user_name is not None and not isinstance(user_name, str):
            raise SDKException('Organization', '101', 'user_name must be a string')

        encoded_password = password if is_password_encoded else b64encode(password.encode()).decode()
        api_url = self._services['BREAKGLASS_ACCOUNT']

        if force_reset:
            user_name = None
            api_url = f"{api_url}?forceReset=true"

        request_json = {
            "users": [
                {
                    "password": encoded_password,
                    "userEntity": {
                        "userName": user_name
                    }
                }
            ]
        }

        flag, response = self._cvpysdk_object.make_request('POST', api_url, request_json)

        if flag:
            if response.json():
                response_json = response.json()
                if 'error' in response_json:
                    error_code = response_json['error'].get('errorCode', 0)
                    error_message = response_json['error'].get('errorMessage', '')
                else:
                    error_code = response_json.get('errorCode', 0)
                    error_message = response_json.get('errorMessage', '')

                if error_code != 0:
                    raise SDKException('Organization', '110', 'Error: {0}'.format(error_message))

                return response_json

            raise SDKException('Response', '102')

        response_string = self._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def enable_owner_data_privacy(self) -> None:
        """To enable company privacy to allow owner to enable data privacy

        Usage:
            org.enable_owner_data_privacy()
        """
        if self.is_owner_data_privacy_enabled:
            return

        self._update_properties_json({'allowUsersToEnablePrivacy': True})
        self._update_properties()

    def disable_owner_data_privacy(self) -> None:
        """To disable company privacy to allow owner to enable data privacy

        Usage:
            org.disable_owner_data_privacy()
        """
        if not self.is_owner_data_privacy_enabled:
            return

        self._update_properties_json({'allowUsersToEnablePrivacy': False})
        self._update_properties()

    def allow_owners_to_enable_passkey(self, flag: bool) -> None:
        """
        Enable or Disable option to allow owners to enable privacy

        Args:
            flag (bool):  True (Enable Passkey) or False (Disable Passkey)

        Usage:
            org.allow_owners_to_enable_passkey(flag=True)
            org.allow_owners_to_enable_passkey(flag=False)
        """
        self._update_properties_json({"allowUsersToEnablePasskey": flag})
        self._update_properties()

    def update_general_settings(self, general_settings_dict: dict) -> None:
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

        Usage:
            general_settings = {
                "newName": "New Org Name",
                "general": {
                    "newAlias": "new_alias",
                    "emailSuffix": "example.com",
                }
            }
            org.update_general_settings(general_settings_dict=general_settings)
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
    def geo_info(self) -> Tuple[Optional[str], List[str]]:
        """
        The regions this company is mapped to

        Returns:
            Tuple[Optional[str], List[str]]:
                idp_region          (str)   -   region name of idp
                workload_regions    (list)  -   list of region names of workloads

        Usage:
            idp_region, workload_regions = org.geo_info
        """
        geo_info = self.organization_info.get('organizationProperties', {}).get('companyGeoInfo', [])
        workloads = []
        idp = None
        for region in geo_info:
            region_name = region.get('companyRegion', {}).get('regionName')
            if region.get('isIdPRegion'):
                idp = region_name
            else:
                workloads.append(region_name)
        return idp, workloads

    def home_commcell(self) -> str:
        """
        Returns the home cell name of this organization

        Returns:
            str: home cell name

        Usage:
            home_cell = org.home_commcell
        """
        return self._commcell_object.organizations.all_organizations_props.get(
            self.name.lower(), {}
        ).get('home_commcell')


    @property
    def workloads(self) -> list[dict]:
        """
        Returns the workloads associated with this organization

        Returns:
            list[dict]: list of workload property dicts
            example: [
                {'id': ..., 'GUID': ..., 'commcell': ...}
                {'id': ..., 'GUID': ..., 'commcell': ...},
                ...
            ]

        Usage:
            workloads = org.workloads
        """
        return self._commcell_object.organizations.all_organizations_props.get(
            self.name.lower(), {}
        ).get('workloads', [])


    @property
    def provider_guid(self) -> str:
        """
        provider GUID for this organization

        Returns:
            str: The provider GUID.

        Usage:
            guid = org.provider_guid
        """
        return self.organization_info.get('organization', {}).get('providerGUID')


    @property
    def parent_company(self) -> dict:
        """
        Returns the parent company details dict of this organization (if it is child company).

        Returns:
            dict: parent company details

        Example: {
            '_type_': <entity type id>,
            'providerId': <company id>,
            'providerDomainName': '<company name>'
        }

        Usage:
            parent_company = org.parent_company
        """
        return self.organization_properties.get("resellerCompany")


    def add_additional_settings(self, key_name: str, category: str, data_type: str, value: str, comment: str="Added using automation", enabled: int=1) -> None:
        """Adds additional settings on company level

        Args:
            key_name (str): The name of the setting.
            category (str): The category of the setting.
            data_type (str): The data type of the setting.
            value (str): The value of the setting.
            comment (str): Comment for the setting. Defaults to "Added using automation".
            enabled (int): Whether the setting is enabled. Defaults to 1.

        Usage:
            org.add_additional_settings(key_name='setting1', category='category1', data_type='string', value='value1')
            org.add_additional_settings(key_name='setting2', category='category2', data_type='int', value='123', comment='test', enabled=0)
        """
        self.additional_settings.add_additional_setting(
            key_name, category, data_type, value, comment, bool(enabled)
        )


    @property
    def additional_settings(self) -> 'AdditionalSettings':
        """
        Returns the AdditionalSettings object associated with this organization.

        Returns:
            AdditionalSettings: The AdditionalSettings object.

        Usage:
            settings = org.additional_settings
        """
        if self._additional_settings is None:
            self._additional_settings = AdditionalSettings(self)
        return self._additional_settings


    def get_entity_counts(self) -> dict[str, int]:
        """
        Gets the entity type and counts for company's associated entities

        Returns:
            dict[str, int]: entity as key and count as value

            {'total': 8, 'Alert definitions': 4, 'User': 1, 'User group': 2, 'Server group': 1}

        Raises:
            SDKException:
                if response is empty

                if response is not success

        Usage:
            entity_counts = org.get_entity_counts()
        """
        resp = self._commcell_object.wrap_request(
            'GET', 'COMPANY_ENTITIES', (self._organization_id,)
        )
        return {
            ENTITY_TYPE_MAP.get(entity['name'], f'type_{entity["name"]}'): entity['count']
            for entity in resp.get('entities', [])
        } | {'total': resp.get('totalCount', -1)}


    def extend(self, region: str, country: str, source_commcell: str, target_commcell: str) -> None:
        """
        Extends this company to specified region

        Args:
            region          (str): the name of region to extend to
            country         (str): country associated with region name
            source_commcell (str): name of the source commcell from which this company is extended
            target_commcell (str): name of the target commcell to which this company is extended

        Usage:
            org.extend(region='US', country='USA', source_commcell='source_cc', target_commcell='target_cc')
        """
        req_json = {
            "sourceCommcell": {
                "commcell": {
                    "commCellName": source_commcell
                }
            },
            "targetCommcell": {
                "commcell": {
                    "commCellName": target_commcell
                },
                "companyGeoInfo": {
                    "country": country,
                    "companyRegion": {
                        "regionName": region
                    }
                }
            },
            "tenantCompany": {
                "providerGUID": self.provider_guid.lower()
            }
        }

        self._commcell_object.wrap_request(
            'POST', 'EXTEND_ORGANIZATION',
            req_kwargs={'payload': req_json},
            sdk_exception=('Organization', '115')
        )
