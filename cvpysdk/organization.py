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

    has_organization()          --  checks whether the organization with given name exists or not

    add()                       --  adds a new organization to the commcell

    get()                       --  returns Organization class object for the specified input name

    delete()                    --  deletes an organization from the commcell

    dissociate_plans()          -- disassociates plans from the organization

    refresh()                   --  refresh the list of organizations associated with the commcell

Organizations Attributes
------------------------

    **all_organizations**   --  returns the dict consisting of organizations and their details

    **all_organizations_props** -- returns the dict consisting of organizations and their guid's


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

    enable_auto_discover()      --  Enable autodiscover option for the oraganization

    disable_auto_discover()      --  Diable autodiscover option for the oraganization

    add_service_commcell_associations() -- Adds the organization association on service commcell

    remove_service_commcell_associations()-- Removes the orgainization association on service commcell

    enable_tfa()                --      Enable tfa option for the organization

    disable_tfa()               --      Disable tfa option for the organization

    get_alerts()                --  get all the alerts associated to organization
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

        **default_plan**            --  returns the default plan associated with the organization

        **default_plan = 'plan'**   --  update the default plan of the organization

        **plans**                   --  returns the list of plans associated with the organization

        **plans = ['plan1',
        'plan2']**                  --  update the list of plans associated with the organization

        **operator_role**             -- returns the operator role assigned to an user

        **tenant_operator**             -- returns the operators associated with the organization

         **is_auto_discover_enabled**-- returns the autodiscover option for the Organization

         **is_tfa_enabled**          -- returns the status of tfa for the organization.

         **tfa_enabled_user_groups**    --  returns list of user groups names for which tfa is enabled.

         **is_using_upn**           -- returns if organization is using upn or not

         **reseller_enabled**       -- returns if reseller is enabled or not

         **is_data_encryption_enabled**-- returns if owners are allowed to enable data encryption

         **infrastructure_type**    -- returns infrastructure associated with a organization

         **auto_laptop_owners_enabled**-- returns if laptop owners are assigned automatically for an organization

         **supported_solutions**    -- returns the supported solutions for an organization

         **job_start_time**         -- returns the job start time associated with the organization

        **client_groups**          -- returns clientgroups associated with the organization
"""

import re

from datetime import datetime
from past.builtins import basestring

from .exception import SDKException

from .security.user import User
from .security.usergroup import UserGroup
from .security.two_factor_authentication import TwoFactorAuthentication


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

    def _get_organizations(self):
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
        flag, response = self._cvpysdk_object.make_request('GET', self._organizations_api)

        if flag:
            organizations = {}
            self._adv_config = {}
            if response.json() and 'providers' in response.json():
                for provider in response.json()['providers']:
                    name = provider['connectName'].lower()
                    organization_id = provider['shortName']['id']
                    organization_guid = provider['providerGUID']
                    organizations[name] = organization_id
                    self._adv_config[name] = {
                        'GUID': organization_guid
                    }

            return organizations
        response_string = self._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

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
        """Returns the dictionary consisting of all the organizations guid info.

            dict - consists of all the organizations configured on the commcell

                {
                    "organization1_name":
                     {
                     GUID : "49DADF71-247E-4D59-8BD8-CF7BFDF7DB28"
                     },

                    "organization2_name":
                    {
                    GUID : "49DADF71-247E-4D59-8BD8-CF7BFDF7DB27"
                    }
                }

        """
        return self._adv_config

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
        if not isinstance(name, basestring):
            raise SDKException('Organization', '101')

        return self._organizations and name.lower() in self._organizations

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

        if not (isinstance(name, basestring) and
                isinstance(email, basestring) and
                isinstance(contact_name, basestring) and
                isinstance(company_alias, basestring)):
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
                    'defaultPlans': plans_list
                }
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
        if not isinstance(name, basestring):
            raise SDKException('Organization', '101')

        name = name.lower()

        if self.has_organization(name):
            return Organization(self._commcell_object, name, self._organizations[name])
        raise SDKException('Organization', '103')

    def delete(self, name):
        """Deletes the organization with the given name from the Commcell.

            Args:
                name            (str)   --  name of the organization to delete

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

    def refresh(self):
        """Refresh the list of organizations associated to the Commcell."""
        self._adv_config = None
        self._organizations = self._get_organizations()


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
        self._default_plan = None
        self._contacts = {}
        self._plans = {}
        self._organization_info = None
        self._operator_role = None
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

        self._tfa_obj = TwoFactorAuthentication(self._commcell_object,organization_id=self._organization_id)
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
            value (int) : id for the infrastructure type
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
            value (int): bits converted to int for the supported solutions
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
            value (int): time to be set for job start time for a company
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

    def _get_properties(self):
        """Gets the properties of this Organization.

            Returns:
                dict    -   dictionary consisting of the properties of this organization

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['ORGANIZATION'] % self.organization_id
        )

        if flag:
            if response.json() and 'organizationInfo' in response.json():
                self._organization_info = response.json()['organizationInfo']

                organization = self._organization_info['organization']
                organization_properties = self._organization_info['organizationProperties']

                self._description = organization['description']
                self._email_domain_names = organization.get('emailDomainNames')
                self._domain_name = organization['shortName']['domainName']

                self._is_auth_code_enabled = organization_properties['enableAuthCodeGen']
                self._auth_code = organization_properties.get('authCode')
                self._use_upn = organization_properties.get('useUPNForEmail')
                self._reseller_enabled = organization_properties.get('canCreateCompanies')
                self._is_data_encryption_enabled = organization_properties.get('showDLP')
                self._infrastructure_type = organization_properties.get('infrastructureType')
                self._auto_laptop_owners = organization_properties.get('autoClientOwnerAssignmentType')
                self._supported_solutions = organization_properties.get('supportedSolutions')
                self._global_file_exceptions_enabled = organization_properties.get('useCompanyGlobalFilter')

                job_time_enabled = organization_properties.get('isJobStartTimeEnabled')
                if job_time_enabled:
                    job_time_epoch = organization_properties.get('jobStartTime', None)
                    self._job_start_time = job_time_epoch
                else:
                    self._job_start_time = 'System default'

                time_epoch = organization_properties.get('orgCreationDateTime')
                time_string = (datetime.fromtimestamp(time_epoch).strftime("%b %#d") +
                               (datetime.fromtimestamp(time_epoch).strftime(" %Y") if datetime.now().year != datetime.fromtimestamp(time_epoch).year else '') +
                               datetime.fromtimestamp(time_epoch).strftime(", %#I:%M:%S %p"))
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

                for plan in organization_properties.get('defaultPlans', []):
                    self._default_plan = plan['plan']['planName']

                for plan in self._organization_info.get('planDetails', []):
                    self._plans[plan['plan']['planName'].lower()] = plan['plan']['planId']

                self._operator_role = organization_properties['operatorRole']['roleName']

                if self._organization_info.get('planDetails', []):
                    self._plan_details = self._organization_info['planDetails']

                self._server_count = organization_properties['serverCount']

                for file_filter in organization_properties['globalFiltersInfo']['globalFiltersInfoList']:
                    os_type_map = {1: 'Windows', 2: 'Unix'}
                    self._file_exceptions[os_type_map[file_filter['operatingSystemType']]] =\
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
                security_list = response.get('securityAssociations')[0].get('securityAssociations').get('associations')
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
                'organizationProperties': self._properties.get('organizationProperties')
            }
        }

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
                error_message = response.json()['error']['errorMessage']
            else:
                error_code = response.json()['errorCode']
                error_message = response.json()['errorMessage']

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
            self._properties['organizationProperties'][key] = properties_dict[key]

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

    @property
    def description(self):
        """Returns the description for this Organization."""
        return self._description

    @property
    def email_domain_names(self):
        """Returns the value of the email domain names for this Organization."""
        return self._email_domain_names

    @property
    def domain_name(self):
        """Returns the value of the domain name for this Organization."""
        return self._domain_name

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
        """Update the default plan associated with the Organization."""

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

    @property
    def sender_email(self):
        """Returns sender email"""
        return self._sender_email

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

    def refresh(self):
        """Refresh the properties of the Organization."""
        self._default_plan = None
        self._contacts = {}
        self._plans = {}
        self._properties = self._get_properties()
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

        self.refresh()

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

        return self.auth_code

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

        if not (isinstance(name, basestring) and
                isinstance(service_commcell, basestring)):
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
                            self._commcell_object.registered_routing_commcells[service_commcell]['commCell']['commCellName'],
                        "_type_": 150,
                        "entityId":
                            self._commcell_object.registered_routing_commcells[service_commcell]['commCell']['commCellId']
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

        if not isinstance(name, basestring):
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
        organization_name = self._organization_name
        if self._client_groups is None:
            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'GET', self._services['CLIENTGROUPS']
            )

            if flag:
                if response.json() and 'groups' in response.json():
                    client_groups = response.json()['groups']
                    clientgroups_dict = {}

                    for client_group in client_groups:
                        temp_name = client_group['name'].lower()
                        temp_id = str(client_group['Id']).lower()
                        company_name = client_group['clientGroup']['entityInfo']['companyName']
                        if company_name in clientgroups_dict.keys():
                            clientgroups_dict[company_name][temp_name] = temp_id
                        else:
                            clientgroups_dict[company_name] = {temp_name: temp_id}
                    self._client_groups = clientgroups_dict[organization_name]
                else:
                    self._client_groups = []
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
