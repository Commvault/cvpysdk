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

    set_sso                     --  Enables/Disables single sign on a domain

    set_properties              --  Sets/modifies the properties for domain

    set_domain_status           --  Enables/Disables the domain
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from base64 import b64encode

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

if TYPE_CHECKING:
    from .commcell import Commcell

from .exception import SDKException


class Domains(object):
    """
    Manages and interacts with all domains associated with a Commcell.

    The Domains class provides a comprehensive interface for retrieving, managing,
    and manipulating domain objects within a Commcell environment. It supports
    operations such as adding, deleting, refreshing, and querying domains, as well
    as accessing domain details and checking for domain existence.

    Key Features:
        - Retrieve all domains associated with a Commcell
        - Access domain details using indexing and property access
        - Add new domains with detailed configuration options
        - Delete existing domains
        - Refresh the domain list to reflect current state
        - Check for the existence of a domain by name
        - Get domain information by name
        - Support for string representation, length, and iteration
        - Internal method for fetching domain data

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize a Domains object with a Commcell connection.

        Args:
            commcell_object: Instance of the Commcell class used to interact with the Commcell environment.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> domains = Domains(commcell)
            >>> print("Domains object initialized successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._DOMAIN_CONTROLER = self._services['DOMAIN_CONTROLER']

        self._domains = None
        self.refresh()

    def __str__(self) -> str:
        """Return a formatted string representation of all domains in the Commcell.

        The output lists each domain with its serial number in a tabular format.

        Returns:
            A string containing all domains associated with the Commcell, formatted for display.

        Example:
            >>> domains = Domains(commcell_object)
            >>> print(domains)
            # Output:
            # S. No.    Domain
            #   1       domain1
            #   2       domain2
            #   ...

        #ai-gen-doc
        """
        representation_string = "{:^5}\t{:^50}\n\n".format('S. No.', 'Domain')

        for index, domain_name in enumerate(self._domains):
            sub_str = '{:^5}\t{:30}\n'.format(index + 1, domain_name)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return a string representation of the Domains class instance.

        This method provides a human-readable description of the Domains object,
        typically used for debugging and logging purposes.

        Returns:
            String describing the Domains class instance.

        Example:
            >>> domains = Domains(commcell_object)
            >>> print(repr(domains))
            Domains class instance for Commcell

        #ai-gen-doc
        """
        return "Domains class instance for Commcell"

    def __len__(self) -> int:
        """Get the number of domains associated with the Commcell.

        Returns:
            The total count of domains managed by this Domains object.

        Example:
            >>> domains = Domains(commcell_object)
            >>> num_domains = len(domains)
            >>> print(f"Total domains: {num_domains}")
        #ai-gen-doc
        """
        return len(self.all_domains)

    def __getitem__(self, value: Union[str, int]) -> Union[str, Dict[str, Any]]:
        """Retrieve domain information by name or ID.

        If a domain name is provided, returns the details dictionary for that domain.
        If a domain ID is provided, returns the name of the corresponding domain.

        Args:
            value: The name (str) or ID (int or str) of the domain to retrieve.

        Returns:
            If a domain name is provided, returns a dictionary containing domain details.
            If a domain ID is provided, returns the name of the domain as a string.

        Raises:
            IndexError: If no domain exists with the given name or ID.

        Example:
            >>> domains = Domains()
            >>> # Get domain details by name
            >>> details = domains['Finance']
            >>> print(details)
            >>> # Get domain name by ID
            >>> name = domains[101]
            >>> print(f"Domain name: {name}")

        #ai-gen-doc
        """
        value = str(value)

        if value in self.all_domains:
            return self.all_domains[value]
        else:
            try:
                return list(filter(lambda x: x[1]['id'] == value, self.all_domains.items()))[0][0]
            except IndexError:
                raise IndexError('No domain exists with the given Name / Id')

    def _get_domains(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve all domains associated with the Commcell.

        Returns:
            Dictionary mapping domain names (as lowercase strings) to their details.
            Each value is a dictionary containing domain-specific information.

        Raises:
            SDKException: If the response from the Commcell is empty or unsuccessful.

        Example:
            >>> domains = domains_obj._get_domains()
            >>> print(f"Found {len(domains)} domains")
            >>> # Access details for a specific domain
            >>> if 'exampledomain' in domains:
            >>>     details = domains['exampledomain']
            >>>     print(f"Domain details: {details}")

        #ai-gen-doc
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
    def all_domains(self) -> Dict[str, Dict[str, Any]]:
        """Get all domains configured on this Commcell.

        Returns:
            Dictionary mapping domain names to their respective details.
            Each key is a domain name (str), and each value is a dictionary containing domain-specific information.

        Example:
            >>> domains = Domains(commcell_object)
            >>> all_domains = domains.all_domains  # Use dot notation for property access
            >>> print(f"Total domains: {len(all_domains)}")
            >>> for domain_name, details in all_domains.items():
            ...     print(f"Domain: {domain_name}, Details: {details}")

        #ai-gen-doc
        """
        return self._domains

    def has_domain(self, domain_name: str) -> bool:
        """Check if a domain with the specified name exists in the Commcell.

        Args:
            domain_name: Name of the domain to check, as a string.

        Returns:
            True if the domain exists in the Commcell, False otherwise.

        Raises:
            SDKException: If the domain_name argument is not a string.

        Example:
            >>> domains = Domains(commcell_object)
            >>> exists = domains.has_domain("example.com")
            >>> print(f"Domain exists: {exists}")
            >>> # Output: Domain exists: True or False

        #ai-gen-doc
        """
        if not isinstance(domain_name, str):
            raise SDKException('Domain', '101')

        return self._domains and domain_name.lower() in self._domains

    def get(self, domain_name: str) -> 'Domain':
        """Retrieve a domain object by its name.

        Args:
            domain_name: Name of the domain to retrieve.

        Returns:
            Domain object corresponding to the specified domain name.

        Raises:
            SDKException: If the domain does not exist or if the domain_name is not a string.

        Example:
            >>> domains = Domains(commcell_object)
            >>> domain = domains.get("example.com")
            >>> print(f"Domain object: {domain}")
            >>> # The returned Domain object can be used for further domain operations

        #ai-gen-doc
        """
        if not isinstance(domain_name, str):
            raise SDKException('Domain', '101')
        if not self.has_domain(domain_name):
            raise SDKException(
                'Domain', '102', "Domain {0} doesn't exists on this commcell.".format(
                    domain_name)
            )

        return Domain(self._commcell_object, domain_name, self._domains[domain_name.lower()]['shortName']['id'])

    def delete(self, domain_name: str) -> None:
        """Delete a domain from the Commcell.

        Removes the specified domain by name from the Commcell. If the domain does not exist,
        or if the deletion fails, an SDKException is raised.

        Args:
            domain_name: Name of the domain to remove from the Commcell.

        Raises:
            SDKException: If the domain name is not a string, if the domain does not exist,
                if the deletion fails, or if the response from the Commcell is invalid.

        Example:
            >>> domains = Domains(commcell_object)
            >>> domains.delete("example_domain")
            >>> print("Domain deleted successfully")
            # If the domain does not exist or deletion fails, an SDKException will be raised.

        #ai-gen-doc
        """

        if not isinstance(domain_name, str):
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

    def refresh(self) -> None:
        """Reload the domain information associated with the Commcell.

        This method updates the internal domain cache to ensure that the latest domain data
        from the Commcell is available for subsequent operations.

        Example:
            >>> domains = Domains(commcell_object)
            >>> domains.refresh()  # Refreshes the domain cache
            >>> print("Domain information updated successfully")
            >>> # The next access to domain data will use the refreshed information

        #ai-gen-doc
        """
        self._domains = self._get_domains()

    def add(self,
            domain_name: str,
            netbios_name: str,
            user_name: Optional[str] = None,
            password: Optional[str] = None,
            credential_id: Optional[int] = None,
            use_local_system_account: Optional[bool] = None,
            company_id: str = "",
            ad_proxy_list: Optional[List[str]] = None,
            enable_sso: bool = True,
            type_of_server: str = "active directory",
            **kwargs: Any) -> Dict[str, Any]:
        """Add a new domain to the Commcell environment.

        This method registers a new domain (such as Active Directory, LDAP, etc.) with the Commcell,
        allowing for centralized authentication and management. You can specify domain credentials,
        proxy clients, SSO settings, and additional LDAP attributes as needed.

        Args:
            domain_name: Name of the domain to be added.
            netbios_name: NetBIOS name of the domain.
            user_name: Username for domain authentication. Required unless using local system account or credential ID.
            password: Password for domain authentication. Required unless using local system account or credential ID.
            credential_id: Credential ID for domain authentication. Used if not providing username/password.
            use_local_system_account: If True, uses the LocalSystemAccount for authentication.
            company_id: Company ID for which the domain is being added.
            ad_proxy_list: Optional list of client names to be used as proxy for domain operations.
            enable_sso: Whether to enable Single Sign-On (SSO) for the domain.
            type_of_server: Type of server to register. Supported values:
                "active directory", "apple directory", "oracle ldap", "open ldap", "ldap server"
            **kwargs: Additional LDAP or directory server settings, such as:
                group_filter: LDAP group filter string.
                user_filter: LDAP user filter string.
                unique_identifier: LDAP unique identifier string.
                base_dn: LDAP base distinguished name.
                email_attribute: LDAP email attribute name.
                guid_attribute: LDAP GUID attribute name.
                additional_settings: List of additional settings dictionaries for directory server.

        Returns:
            Dictionary containing the properties of the newly added domain.

        Raises:
            SDKException: If input parameters are invalid or domain addition fails.

        Example:
            >>> domains = Domains(commcell_object)
            >>> domain_props = domains.add(
            ...     domain_name="example.com",
            ...     netbios_name="EXAMPLE",
            ...     user_name="admin",
            ...     password="password123",
            ...     ad_proxy_list=["client1", "client2"],
            ...     enable_sso=True,
            ...     type_of_server="active directory",
            ...     group_filter="(objectClass=group)",
            ...     user_filter="(&(objectCategory=User)(sAMAccountName=*))",
            ...     base_dn="dc=example,dc=com"
            ... )
            >>> print(domain_props)
            {'domainName': 'example.com', 'netbiosName': 'EXAMPLE', ...}

        #ai-gen-doc
        """
        service_type_mapping = {"active directory": 2, "apple directory": 8, "oracle ldap": 9, "open ldap": 10,
                                "ldap server": 14}
        service_type = service_type_mapping.get(type_of_server.lower())
        if not service_type:
            raise SDKException('Domain', "102", "please pass valid server type")
        if not (isinstance(domain_name, str) and
                isinstance(netbios_name, str) and
                (
                        isinstance(use_local_system_account, bool) or
                        isinstance(credential_id, int) or
                        (isinstance(user_name, str) and isinstance(password, str))
                )
        ):
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
                "flags": 1 if enable_sso else 0,
                "enabled": 1,
                "useSecureLdap": 0,
                "connectName": domain_name,
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

        if user_name and password:
            domain_create_request["provider"]['login'] = user_name
            domain_create_request["provider"]['bLogin'] = user_name
            domain_create_request["provider"]['bPassword'] = b64encode(password.encode()).decode()
        elif use_local_system_account:
            domain_create_request["provider"]['login'] = 'LocalSystemAccount'
            domain_create_request["provider"]['bLogin'] = 'LocalSystemAccount'
        else:
            domain_create_request["provider"]['domainCredInfo'] = {"credentialId": credential_id}

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
                    },
                    {
                        "attrTypeFlags": 6,
                        "customAttributeString": kwargs.get('email_attribute', 'mail'),
                        "attrId": 3,
                        "attributeName": "Email",
                        "staticAttributeString": "mail"
                    },
                    {
                        "attrTypeFlags": 6,
                        "customAttributeString": kwargs.get('guid_attribute', 'objectGUID'),
                        "attrId": 4,
                        "attributeName": "GUID",
                        "staticAttributeString": "objectGUID"
                    }
                ]
            }
            domain_create_request["provider"]["customProvider"] = custom_provider

        if kwargs.get('additional_settings'):
            domain_create_request["provider"]['additionalSettings'] = kwargs.get('additional_settings')

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
                    error_message = response.json()["errorMessage"]
                    o_str = ('Failed to add domain with error code: "{0}"'
                             '\nWith error message: "{1}"')
                    raise SDKException(
                        'Domain', '102', o_str.format(error_code, error_message)
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)


class Domain(object):
    """
    Represents a specific domain configured on a CommCell.

    This class provides an interface for managing and interacting with domains within a CommCell environment.
    It allows retrieval and modification of domain properties, management of Single Sign-On (SSO) settings,
    and enables or disables domain status. The class also supports refreshing domain information and provides
    access to domain identifiers and names.

    Key Features:
        - Initialize domain objects with CommCell context, domain name, and domain ID
        - Retrieve domain properties and identifiers
        - Refresh domain information from the CommCell
        - Enable or disable Single Sign-On (SSO) for the domain
        - Update domain properties using request bodies
        - Set domain status (enable/disable)
        - Access domain name and domain ID via properties
        - String representation for domain objects

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', domain_name: str, domain_id: Optional[str] = None) -> None:
        """Initialize a Domain object for the specified domain.

        Args:
            commcell_object: Instance of the Commcell class representing the Commcell connection.
            domain_name: Name of the domain as a string.
            domain_id: Optional string representing the domain ID. If not provided, it will be determined automatically.

        Example:
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> domain = Domain(commcell, "example.com")
            >>> # To specify a domain ID explicitly
            >>> domain_with_id = Domain(commcell, "example.com", domain_id="12345")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._domain_name = domain_name.lower()

        if domain_id is None:
            self._domain_id = self._get_domain_id(self._domain_name)
        else:
            self._domain_id = domain_id

        self._domain = self._commcell_object._services['DOMAIN_PROPERTIES'] % (self._domain_id)
        self._DOMAIN_CONTROLER = self._commcell_object._services['DOMAIN_CONTROLER']
        self._properties = None
        self._get_domain_properties()

    def __repr__(self) -> str:
        """Return a string representation of the Domain instance.

        This method provides a readable description of the Domain object,
        including the domain name for easier identification during debugging
        or logging.

        Returns:
            String representation of the Domain instance.

        Example:
            >>> domain = Domain(...)
            >>> print(repr(domain))
            Domain class instance for Domain: "example.com"
        #ai-gen-doc
        """
        representation_string = 'Domain class instance for Domain: "{0}"'
        return representation_string.format(self.domain_name)

    def _get_domain_id(self, domain_name: str) -> int:
        """Retrieve the domain ID associated with the specified domain name.

        Args:
            domain_name: The name of the domain for which to fetch the ID.

        Returns:
            The integer ID associated with the specified domain.

        Example:
            >>> domain = Domain(commcell_object)
            >>> domain_id = domain._get_domain_id("example.com")
            >>> print(f"Domain ID: {domain_id}")

        #ai-gen-doc
        """
        domain = Domains(self._commcell_object)
        return domain.get(domain_name).domain_id

    def _get_domain_properties(self) -> Dict[str, Any]:
        """Retrieve the properties of the current domain.

        This method fetches domain details such as domain name and domain ID from the Commcell server.
        It returns a dictionary containing the domain properties.

        Returns:
            Dictionary with domain properties, including:
                - domain_name (str): Name of the domain.
                - domain_id (str): Unique identifier for the domain.

        Raises:
            SDKException: If the response from the server is invalid or does not contain expected data.

        Example:
            >>> domain = Domain(commcell_object, domain_id)
            >>> properties = domain._get_domain_properties()
            >>> print(f"Domain Name: {properties['domain_name']}")
            >>> print(f"Domain ID: {properties['domain_id']}")

        #ai-gen-doc
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

    def refresh(self) -> None:
        """Reload the properties of the domain to ensure up-to-date information.

        This method refreshes the domain's internal state by re-fetching its properties.
        Use this when you need to ensure the domain object reflects the latest configuration.

        Example:
            >>> domain = Domain(...)
            >>> domain.refresh()  # Updates domain properties from the source
            >>> print("Domain properties refreshed successfully")
        #ai-gen-doc
        """
        self._get_domain_properties()

    def set_sso(self, flag: bool = True, **kwargs: Any) -> None:
        """Enable or disable Single Sign-On (SSO) for the domain.

        This method allows you to enable or disable SSO for the domain. You can optionally provide
        a username and password for authentication via keyword arguments.

        Args:
            flag: Set to True to enable SSO, or False to disable SSO.
            **kwargs: Optional keyword arguments for supported parameters:
                - username (str): Username to be used for authentication.
                - password (str): Password to be used for authentication.

        Raises:
            SDKException: If arguments are of incorrect types, if enabling/disabling SSO fails,
                if the response is empty, or if the response indicates failure.

        Example:
            >>> domain = Domain(...)
            >>> # Enable SSO with credentials
            >>> domain.set_sso(True, username="admin", password="securepass")
            >>> # Disable SSO
            >>> domain.set_sso(False)
        #ai-gen-doc
        """

        if not isinstance(flag, bool):
            raise SDKException('Domain', '101')
        request_json = {"enableSSO": flag}
        username = kwargs.get("username", None)
        password = kwargs.get("password", None)
        if username and password:
            if not (isinstance(username, str) and isinstance(password, str)):
                raise SDKException('Domain', '101')
            request_json["username"] = username
            request_json["password"] = b64encode(password.encode()).decode()
        url = self._commcell_object._services['DOMAIN_SSO'] % self.domain_id
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', url, request_json
        )
        if flag:
            if response.json():
                error_code = response.json().get('errorCode', 0)
                if error_code != 0:
                    raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))
                return
            raise SDKException('Response', '102')
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def set_properties(self, req_body: Dict[str, Any]) -> None:
        """Modify the properties of the domain using the provided payload.

        Args:
            req_body: Dictionary containing domain properties to update, formatted as JSON payload for the API.

        Raises:
            SDKException: If the properties could not be set or if the API request fails.

        Example:
            >>> domain = Domain(commcell_object, domain_id)
            >>> payload = {
            ...     "domainName": "NewDomainName",
            ...     "description": "Updated domain description"
            ... }
            >>> domain.set_properties(payload)
            >>> print("Domain properties updated successfully")

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', self._commcell_object._services['DOMAIN_SSO'] % self.domain_id, req_body
        )
        if flag:
            if response.json():
                error_code = response.json().get('errorCode', 0)
                if error_code != 0:
                    raise SDKException(
                        'Response', '101',
                        self._commcell_object._update_response_(response.text)
                    )
                return
            raise SDKException('Response', '102')
        raise SDKException(
            'Response', '101', self._commcell_object._update_response_(response.text))

    def set_domain_status(self, enable: bool) -> None:
        """Enable or disable the domain.

        This method updates the domain status based on the provided flag. If `enable` is True, the domain is enabled;
        if False, the domain is disabled. The operation is performed via a POST request to the domain controller.

        Args:
            enable: Set to True to enable the domain, or False to disable it.

        Raises:
            SDKException: If the response from the server indicates a failure or an error occurs during the update.

        Example:
            >>> domain = Domain(commcell_object)
            >>> domain.set_domain_status(True)   # Enable the domain
            >>> domain.set_domain_status(False)  # Disable the domain

        #ai-gen-doc
        """

        self._properties['enabled'] = 1 if enable else 0
        req_json = {"operation": 3,
                    "provider": self._properties}
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', self._DOMAIN_CONTROLER, req_json)
        if flag:
            if response.json():
                error_code = response.json().get('errorCode', 0)
                if error_code != 0:
                    raise SDKException(
                        'Domain', '102',
                        response.json().get('errorMessage', 'Unable to update domain status')
                    )
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException(
                'Response', '101',
                response.json().get('errorMessage', 'Unable to update domain status'))

    @property
    def domain_name(self) -> str:
        """Get the domain name associated with this Domain object.

        Returns:
            The domain name as a string.

        Example:
            >>> domain = Domain(...)
            >>> name = domain.domain_name  # Use dot notation for property access
            >>> print(f"Domain name: {name}")
        #ai-gen-doc
        """
        return self._properties['shortName']['domainName']

    @property
    def domain_id(self) -> str:
        """Get the unique identifier for this domain.

        Returns:
            The domain ID as a string.

        Example:
            >>> domain = Domain(...)
            >>> domain_id = domain.domain_id  # Use dot notation for properties
            >>> print(f"Domain ID: {domain_id}")

        #ai-gen-doc
        """
        return self._properties['shortName']['id']
