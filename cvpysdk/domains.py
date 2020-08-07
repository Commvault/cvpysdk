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

"""File for performing domain related operations.


Domains: Class for representing all the associated domains with the commcell.


Domains:

    __init__(commcell_object)   --  initialize instance of the Domains associated with
    the specified commcell

    __str__()                   --  returns all the domains associated with the commcell

    __repr__()                  --  returns the string for the instance of the Domains class

    __len__()                   --  returns the number of domains associated with the Commcell

    __getitem__()               --  returns the name of the domain for the given domain Id
    or the details for the given domain name

    _get_domains()              --  gets all the domains associated with the commcell specified

    all_domains()               --  returns the dict of all the domanin configured

    has_domain()                --  checks if a domain exists with the given name or not

    get(domain_name)            --  returns the instance of the Domain class,
    for the the input domain name

    delete(domain_name)         --  deletes the domain from the commcell

    refresh()                   --  refresh the domains associated with the commcell


Domain:

    __init__()                  --  initializes instance of the Domain class for doing
    operations on the selected Domain

    __repr__()                  --  returns the string representation of an instance of this class

    _get_domain_id()            --  Gets the domain id associated with this domain

    _get_domain_properties      --  get the properties of the domain


"""

from __future__ import absolute_import
from __future__ import unicode_literals

from base64 import b64encode
from past.builtins import basestring

from .exception import SDKException


class Domains(object):
    """Class for getting all the domains associated with a commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the Domains class.

            Args:
                commcell_object     (object)    --  instance of the Commcell class

            Returns:
                object - instance of the Domains class

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._DOMAIN_CONTROLER = self._services['DOMAIN_CONTROLER']

        self._domains = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all domains of the Commcell.

            Returns:
                str - string of all the domains for a commcell

        """
        representation_string = "{:^5}\t{:^50}\n\n".format('S. No.', 'Domain')

        for index, domain_name in enumerate(self._domains):
            sub_str = '{:^5}\t{:30}\n'.format(index + 1, domain_name)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Domains class."""
        return "Domains class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def __len__(self):
        """Returns the number of the domains associated to the Commcell."""
        return len(self.all_domains)

    def __getitem__(self, value):
        """Returns the name of the domain for the given domain ID or
            the details of the domain for given domain Name.

            Args:
                value   (str / int)     --  Name or ID of the domain

            Returns:
                str     -   name of the domain, if the domain id was given

                dict    -   dict of details of the domain, if domain name was given

            Raises:
                IndexError:
                    no domain exists with the given Name / Id

        """
        value = str(value)

        if value in self.all_domains:
            return self.all_domains[value]
        else:
            try:
                return list(filter(lambda x: x[1]['id'] == value, self.all_domains.items()))[0][0]
            except IndexError:
                raise IndexError('No domain exists with the given Name / Id')

    def _get_domains(self):
        """Gets all the domains associated with the commcell

            Returns:
                dict - consists of all domain in the commcell

                    {
                         "domain1_name": domain_Details_dict1,

                         "domain2_name": domain_Details_dict2
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._DOMAIN_CONTROLER)

        if flag:
            domains_dict = {}

            if response.json() and 'providers' in response.json():
                response_value = response.json()['providers']

                for temp in response_value:
                    temp_name = temp['shortName']['domainName'].lower()
                    temp_details = temp
                    domains_dict[temp_name] = temp_details

            return domains_dict
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def all_domains(self):
        """Returns the domains configured on this commcell

            dict - consists of all domain in the commcell

                    {
                         "domain1_name": domain_Details_dict1,

                         "domain2_name": domain_Details_dict2
                    }
        """
        return self._domains

    def has_domain(self, domain_name):
        """Checks if a domain exists in the commcell with the input domain name.

            Args:
                domain_name     (str)   --  name of the domain

            Returns:
                bool    -   boolean output whether the domain exists in the commcell or not

            Raises:
                SDKException:
                    if type of the domain name argument is not string

        """
        if not isinstance(domain_name, basestring):
            raise SDKException('Domain', '101')

        return self._domains and domain_name.lower() in self._domains

    def get(self, domain_name):
        """Returns a domain object of the specified domain name.

            Args:
                domain_name (str)  --  name of the domain

            Returns:
                object of the domain

            Raises:
                SDKException:

					if domain doesn't exist with specified name

					if type of the domain name argument is not string

        """
        if not isinstance(domain_name, basestring):
            raise SDKException('Domain', '101')
        if not self.has_domain(domain_name):
            raise SDKException(
                'Domain', '102', "Domain {0} doesn't exists on this commcell.".format(
                    domain_name)
            )

        return Domain(self._commcell_object, domain_name, self._domains[domain_name.lower()]['shortName']['id'])

    def delete(self, domain_name):
        """Deletes the domain from the commcell.

            Args:
                domain_name     (str)   --  name of the domain to remove from the commcell

            Raises:
                SDKException:
                    if type of the domain name argument is not string

                    if failed to delete domain

                    if response is empty

                    if response is not success

                    if no domain exists with the given name

        """

        if not isinstance(domain_name, basestring):
            raise SDKException('Domain', '101')
        else:
            domain_name = domain_name.lower()

            if self.has_domain(domain_name):
                domain_id = str(self._domains[domain_name]["shortName"]["id"])
                delete_domain = self._services['DELETE_DOMAIN_CONTROLER'] % (domain_id)

                flag, response = self._cvpysdk_object.make_request('DELETE', delete_domain)

                if flag:
                    if response.json() and 'errorCode' in response.json():
                        error_code = response.json()["errorCode"]

                        if error_code == 0:
                            # initialize the domain again
                            # so the domains object has all the domains
                            self.refresh()
                        else:
                            o_str = ('Failed to delete domain with error code: "{0}"'
                                     '\nPlease check the documentation for '
                                     'more details on the error')
                            raise SDKException(
                                'Domain', '102', o_str.format(error_code)
                            )
                    else:
                        raise SDKException('Response', '102')
                else:
                    response_string = self._update_response_(response.text)
                    raise SDKException('Response', '101', response_string)
            else:
                raise SDKException(
                    'Domain', '102', 'No domain exists with name: {0}'.format(domain_name)
                )

    def refresh(self):
        """Refresh the domains associated with the Commcell."""
        self._domains = self._get_domains()

    def add(self,
            domain_name,
            netbios_name,
            user_name,
            password,
            company_id="",
            ad_proxy_list=None,
            enable_sso=True,
            type_of_server="active directory",
            **kwargs):
        """Adds a new domain to the commcell.

            Args:
                domain_name     (str)   --  name of the domain

                netbios_name    (str)   --  netbios name of the domain

                user_name       (str)   --  user name of the domain

                password        (str)   --  password of the domain

                company_id      (int)   --  company id for which the domain needs to be added for

                ad_proxy_list     (list)  --  list of client objects to be used as proxy.

                    default: None

                    if no proxy required

                enable_sso      (bool)  --  enable sso for domain

                type_of_server  (str)   --  Type of server to be registered
                    values:
                    "active directory"
                    "apple directory"
                    "oracle ldap"
                    "open ldap"
                    "ldap server"

                **kwargs            --      required parameters for LDAP Server registration

                    group_filter    (str)   --  group filter for ldap server
                    user_filter     (str)   --  user filter for ldap server
                    unique_identifier   (str)   --  unique identifier for ldap server
                    base_dn              (str)  --  base dn for ldap server

            Returns:
                dict    -   properties of domain

            Raises:
                SDKException:
                    if type of the domain name argument is not string

                    if no domain exists with the given name

        """
        service_type_mapping = {"active directory": 2, "apple directory": 8, "oracle ldap": 9, "open ldap": 10,
                                "ldap server": 14}
        service_type = service_type_mapping.get(type_of_server.lower())
        if not service_type:
            raise SDKException('Domain', "102", "please pass valid server type")
        if not (isinstance(domain_name, basestring) and
                isinstance(netbios_name, basestring) and
                isinstance(user_name, basestring) and
                isinstance(password, basestring)):
            raise SDKException('Domain', '101')
        else:
            domain_name = domain_name.lower()

            if self.has_domain(domain_name):
                return self._domains[domain_name]

        proxy_information = {}

        if ad_proxy_list:
            if isinstance(ad_proxy_list, list):
                proxy_information = {
                    'adProxyList': [{"clientName": client} for client in ad_proxy_list]
                }
            else:
                raise SDKException('Domain', '101')

        domain_create_request = {
            "operation": 1,
            "provider": {
                "serviceType": service_type,
                "flags": 1,
                "bPassword": b64encode(password.encode()).decode(),
                "login": user_name,
                "enabled": 1,
                "useSecureLdap": 0,
                "connectName": domain_name,
                "bLogin": user_name,
                "ownerCompanyId": company_id,
                "tppm": {
                    "enable": True if ad_proxy_list else False,
                    "tppmType": 4,
                    "proxyInformation": proxy_information
                },
                "shortName": {
                    "domainName": netbios_name
                }
            }
        }

        if kwargs:
            custom_provider = {
                    "providerTypeId": 0,
                    "attributes": [
                        {
                            "attrId": 6,
                            "attributeName": "User group filter",
                            "staticAttributeString": "(objectClass=group)",
                            "customAttributeString": kwargs.get('group_filter', ''),
                            "attrTypeFlags": 1
                        },
                        {
                            "attrId": 7,
                            "attributeName": "User filter",
                            "staticAttributeString": "(&(objectCategory=User)(sAMAccountName=*))",
                            "customAttributeString": kwargs.get('user_filter', ''),
                            "attrTypeFlags": 1
                        },
                        {
                          "attrId": 9,
                          "attributeName": "Unique identifier",
                          "staticAttributeString": "sAMAccountName",
                          "customAttributeString": kwargs.get('unique_identifier', ''),
                          "attrTypeFlags": 1
                        },
                        {
                          "attrId": 10,
                          "attributeName": "base DN",
                          "staticAttributeString": "baseDN",
                          "customAttributeString": kwargs.get('base_dn', ''),
                          "attrTypeFlags": 1
                        }
                    ]
                }
            domain_create_request["provider"]["customProvider"] = custom_provider

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._DOMAIN_CONTROLER, domain_create_request
        )

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json()["errorCode"]

                if error_code == 0:
                    # initialize the domain again
                    # so the domains object has all the domains
                    self.refresh()
                else:
                    o_str = ('Failed to add domain with error code: "{0}"'
                             '\nPlease check the documentation for '
                             'more details on the error')
                    raise SDKException(
                        'Domain', '102', o_str.format(error_code)
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

class Domain(object):
    """Class for representing a particular domain configured on a commcell"""

    def __init__(self, commcell_object, domain_name, domain_id=None):
        """Initialize the domain class object for specified domain

            Args:
                commcell_object (object)  --  instance of the Commcell class

                domain_name         (str)     --  name of the domain

                domain_id           (str)     --  id of the domain


        """
        self._commcell_object = commcell_object
        self._domain_name = domain_name.lower()

        if domain_id is None:
            self._domain_id = self._get_domain_id(self._domain_name)
        else:
            self._domain_id = domain_id

        self._domain = self._commcell_object._services['DOMAIN_PROPERTIES'] % (self._domain_id)
        self._properties = None
        self._get_domain_properties()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Domain class instance for Domain: "{0}"'
        return representation_string.format(self.domain_name)


    def _get_domain_id(self, domain_name):
        """Gets the domain id associated with this domain

            Args:
                domain_name         (str)     --     name of the domain

            Returns:
                int     -     id associated to the specified user
        """
        domain = Domains(self._commcell_object)
        return domain.get(domain_name).domain_id

    def _get_domain_properties(self):
        """Gets the properties of this domain

            Returns (dict):
                domain_name (str) - name of the domain
                domain_id   (str) - domain id

        """

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._domain
        )

        if flag:
            if response.json() and 'providers' in response.json():
                self._properties = response.json().get('providers', [{}])[0]
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the properties of the domain."""
        self._get_domain_properties()

    @property
    def domain_name(self):
        """Returns the User display name"""
        return self._properties['shortName']['domainName']

    @property
    def domain_id(self):
        """Returns the user name of this commcell user"""
        return self._properties['shortName']['id']

