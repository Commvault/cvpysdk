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

"""Main file for doing Name Change operations.

OperationType:  Class with the supported hostname change operations

NameChange: Class for doing operations for Name Change operations on clients and commcell.

NameChange:
    __init__(class_object)                          --  initialise object of the NameChange
                                                        class

    hostname()                                      --  gets the current hostname of the client or
                                                        commserver

    hostname(parameters_dict)                       --  sets the hostname from client or commserver
                                                        level

    display_name()                                  --  gets the display name of the client or
                                                        commserver

    display_name(display_name)                      --  sets the display name of the client or
                                                        commserver

    client_name()                                   --  gets the name of the client

    client_name(client_name)                        --  sets the name of the client

    domain_name()                                    --  gets the commserver hostname

    domain_name(domains_dict)                        --  sets the new domain name for the clients

    _client_name_change_op()                        --  performs client namechange based on the
                                                        setters

    _commcell_name_change_op(parameters_dict)       --  performs commserver namechange based on the
                                                        setters

    get_clients_for_name_change_post_ccm()          -- gets all the clients available for name change
                                                        post commcell migration

    name_change_post_ccm(parameters_dict)           -- perfoms name change for migrated clients post
                                                        commcell migration
"""

import re
from enum import Enum
from .exception import SDKException
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from .commcell import Commcell
    from .client import Client

class OperationType(Enum):
    """
    Enumeration of operation types supported for retrieving schedules.

    This Enum class defines the various operation types that can be used
    to obtain schedules for specific operation types within the system.
    It serves as a standardized way to reference and manage different
    operation types when interacting with scheduling functionalities.

    Key Features:
        - Enumerates supported operation types for schedule retrieval
        - Provides a clear and type-safe way to specify operation types
        - Facilitates consistent usage across scheduling components

    #ai-gen-doc
    """
    COMMSERVER_HOSTNAME_REMOTE_CLIENTS = 147
    COMMSERVER_HOSTNAME_AFTER_DR = 139
    CLIENT_HOSTNAME = "CLIENT_HOSTNAME"
    COMMSERVER_HOSTNAME = "COMMSERVER_HOSTNAME"


class NameChange(object):
    """
    Class for performing name change operations on clients and the commcell.

    This class provides a set of methods and properties to facilitate the management
    and execution of name change operations for clients and commcell entities. It
    allows retrieval and modification of various name-related attributes such as
    hostname, domain name, display name, and client name. The class also supports
    operations specific to client and commcell name changes, as well as post-CCM
    (CommCell Migration) name change processes.

    Key Features:
        - Retrieve and manage hostname, domain name, display name, and client name via properties
        - Perform client name change operations
        - Perform commcell name change operations with parameter dictionaries
        - Retrieve clients eligible for name change after CommCell Migration (CCM)
        - Execute name change operations post-CCM

    #ai-gen-doc
    """

    def __init__(self, class_object: Union['Commcell', 'Client']) -> None:
        """Initialize a NameChange instance for performing name change operations.

        Args:
            class_object: An instance of the client or commcell class to associate with this NameChange object.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> cc = Commcell('commcell_host', 'username', 'password')
            >>> name_change = NameChange(cc)
            >>> # The NameChange object can now be used to perform name change operations

        #ai-gen-doc
        """
        from .commcell import Commcell
        from .client import Client
        if isinstance(class_object, Commcell):
            self._commcell_object = class_object
            self._display_name = self._commcell_object.clients.get(self._commcell_object.
                                                                   commserv_hostname).display_name
            self._commcell_name = self._commcell_object.clients.get(self._commcell_object.
                                                                    commserv_hostname).commcell_name
            self._is_client = False

        elif isinstance(class_object, Client):
            self._client_object = class_object
            self._commcell_object = class_object._commcell_object
            self._client_hostname = self._client_object.client_hostname
            self._display_name = self._client_object.display_name
            self._client_name = self._client_object.client_name
            self._commcell_name = self._client_object.commcell_name
            self._new_name = None
            self._is_client = True

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

    @property
    def hostname(self) -> str:
        """Get the hostname of the client or CommServe.

        Returns:
            The hostname as a string, which may represent either a client or the CommServe.

        Example:
            >>> name_change = NameChange()
            >>> host = name_change.hostname
            >>> print(f"Hostname: {host}")

        #ai-gen-doc
        """
        if self._is_client:
            return self._client_hostname
        else:
            return self._commcell_name

    @hostname.setter
    def hostname(self, parameters_dict: dict) -> None:
        """Set the client or CommServe hostname using the provided parameters.

        This setter updates the hostname for a client or CommServe based on the specified parameters.
        The parameters_dict should include the operation type and relevant hostname details.

        Args:
            parameters_dict: Dictionary containing parameters for the name change operation. Expected keys:
                - "operation": The type of operation to perform (e.g., "COMMSERVER_HOSTNAME", "CLIENT_HOSTNAME").
                - "ClientHostname": The new client hostname to be set (str).
                - "CommserverHostname": The new CommServe hostname to be set (str).
                - "oldName": The old CommServe hostname (str).
                - "newName": The new CommServe hostname (str).

        Example:
            >>> name_change = NameChange()
            >>> params = {
            ...     "operation": "COMMSERVER_HOSTNAME/CLIENT_HOSTNAME",
            ...     "ClientHostname": "new-client.example.com",
            ...     "CommserverHostname": "new-commserve.example.com",
            ...     "oldName": "old-commserve.example.com",
            ...     "newName": "new-commserve.example.com"
            ... }
            >>> name_change.hostname = params  # Use assignment to trigger the setter

        #ai-gen-doc
        """
        if self._is_client:
            if parameters_dict["operation"] == OperationType.CLIENT_HOSTNAME.value:
                if parameters_dict["ClientHostname"] is None:
                    raise SDKException('NameChange', '101')
                self._client_hostname = parameters_dict["ClientHostname"]
                self._client_name_change_op()
            if parameters_dict["operation"] == OperationType.COMMSERVER_HOSTNAME.value:
                if parameters_dict["CommserverHostname"] is None:
                    raise SDKException('NameChange', '102')
                self._commcell_name = parameters_dict["CommserverHostname"]
                self._client_name_change_op()
        else:
            if parameters_dict["operation"] == OperationType.COMMSERVER_HOSTNAME_REMOTE_CLIENTS.value:
                parameters_dict["oldName"] = self._commcell_name
                self._commcell_name_change_op(parameters_dict)
            elif parameters_dict["operation"] == OperationType.COMMSERVER_HOSTNAME_AFTER_DR.value:
                if parameters_dict["clientIds"] is None:
                    raise SDKException('NameChange', '105')
                parameters_dict["newName"] = self._commcell_name
                self._commcell_name_change_op(parameters_dict)

    @property
    def domain_name(self) -> str:
        """Get the CommServe host name associated with this NameChange instance.

        Returns:
            The CommServe host name as a string.

        Example:
            >>> name_change = NameChange()
            >>> hostname = name_change.domain_name  # Use dot notation for property access
            >>> print(f"CommServe host name: {hostname}")
        #ai-gen-doc
        """
        return self._commcell_name

    @domain_name.setter
    def domain_name(self, domains_dict: dict) -> None:
        """Set the new domain name for clients using the provided domain mapping.

        Args:
            domains_dict: A dictionary specifying the old and new domain names for clients.
                Example format:
                    {
                        "oldDomain": "old_domain_name",
                        "newDomain": "new_domain_name"
                    }
                - "oldDomain": The current domain name of the clients (str).
                - "newDomain": The new domain name to assign to the clients (str).

        Example:
            >>> name_change = NameChange()
            >>> name_change.domain_name = {
            ...     "oldDomain": "CORP",
            ...     "newDomain": "ENTERPRISE"
            ... }
            >>> # The domain name for clients will be updated from 'CORP' to 'ENTERPRISE'
        #ai-gen-doc
        """
        if domains_dict["oldDomain"] is None:
            raise SDKException('NameChange', '103')
        elif domains_dict["newDomain"] is None:
            raise SDKException('NameChange', '104')
        dict_domains = {
            "oldName": domains_dict["oldDomain"],
            "newName": domains_dict["newDomain"],
            "operation": 136
        }
        self._commcell_name_change_op(dict_domains)

    @property
    def display_name(self) -> str:
        """Get the display name of the client or CommServe.

        Returns:
            The display name as a string, representing either the client or CommServe.

        Example:
            >>> name_change = NameChange()
            >>> print(name_change.display_name)  # Use dot notation for property access
            >>> # Output: 'Client123' or 'CommServe01'

        #ai-gen-doc
        """
        if self._is_client:
            return self._display_name
        else:
            return self._display_name

    @display_name.setter
    def display_name(self, display_name: str) -> None:
        """Set the display name for the client or CommServe.

        Args:
            display_name: The new display name to assign to the client or CommServe.

        Example:
            >>> name_changer = NameChange()
            >>> name_changer.display_name = "NewDisplayName"  # Use assignment for property setter
            >>> # The display name is now updated to "NewDisplayName"

        #ai-gen-doc
        """
        if self._is_client:
            self._display_name = display_name
            self._client_name_change_op()
        else:
            dict_cs = {
                "oldName": self._display_name,
                "newName": display_name,
                "operation": 9811,
            }
            self._commcell_name_change_op(dict_cs)

    @property
    def client_name(self) -> str:
        """Get the name of the client associated with this NameChange instance.

        Returns:
            The client name as a string.

        Example:
            >>> name_change = NameChange()
            >>> client = name_change.client_name  # Use dot notation for property access
            >>> print(f"Client name: {client}")

        #ai-gen-doc
        """
        if self._is_client:
            return self._client_name
        else:
            False

    @client_name.setter
    def client_name(self, client_name: str) -> None:
        """Set the name of the client to the specified value.

        Args:
            client_name: The new name to assign to the client.

        Example:
            >>> name_change = NameChange()
            >>> name_change.client_name = "NewClientName"  # Use assignment to set the client name
            >>> # The client's name is now updated to "NewClientName"
        #ai-gen-doc
        """
        self._new_name = client_name
        self._client_name_change_op()

    def _client_name_change_op(self) -> None:
        """Perform the client name change operation.

        This method executes the necessary steps to change the name of a client.
        It raises an SDKException if the name change fails or if the response is empty.

        Raises:
            SDKException: If the client name change operation fails or if the response is empty.

        Example:
            >>> name_change = NameChange()
            >>> name_change._client_name_change_op()
            >>> print("Client name change operation completed successfully.")

        #ai-gen-doc
        """
        request_json = {
            "App_SetClientPropertiesRequest":
            {
                "clientProperties": {
                    "client": {
                        "displayName": self._display_name,
                        "clientEntity": {
                            "hostName": self._client_hostname,
                            "clientName": self._client_name,
                            "commCellName": self._commcell_name
                        }
                    }
                },
                "association": {
                    "entity": [
                        {
                            "clientName": self._client_name,
                            "newName": self._new_name
                        }
                    ]
                }
            }
        }
        flag, response = self._client_object._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], request_json
        )

        if flag:
            if response.json():
                if 'errorMessage' in response.json():
                    # for errorMessage: "Operation Failed" errorCode: 7
                    # for errorMessage: "Error 0x911: Failed to process request due to invalid /
                    # entity information.Invalid clientId for clientName.\n"
                    # errorCode: 2 and others

                    error_message = "Failed to do namechange on client, " \
                                    "with errorCode [{0}], errorMessage [{1}]".format(
                                        response.json().get('errorCode'),
                                        response.json().get('errorMessage')
                                    )
                    raise SDKException('Client', '102', error_message)

                elif 'errorCode' in response.json().get('response')[0]:
                    error_code = str(
                        response.json().get('response')[0].get('errorCode'))
                    if error_code != '0':
                        error_message = "Failed to do namechange on client"
                        raise SDKException('Client', '102', error_message)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException(
                    'Response', '101', self._update_response_(
                        response.text))
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))

    def _commcell_name_change_op(self, parameters_dict: dict) -> None:
        """Perform Commcell name change operations using the provided parameters.

        This method executes name change operations for the Commcell, such as updating the CommServe hostname,
        domain name, or associated client IDs. The `parameters_dict` should contain the necessary keys:
        - "newName": The new Commcell or domain name.
        - "oldName": The current Commcell or domain name.
        - "operation": The type of name change operation to perform.
        - "clientIds": List of client IDs to update (can be an empty list).

        Args:
            parameters_dict: Dictionary containing the name change parameters. Example:
                {
                    "newName": "new_commcell_name",
                    "oldName": "old_commcell_name",
                    "operation": 0,
                    "clientIds": [101, 102, 103]
                }

        Raises:
            SDKException: If the client name change operation fails or if the response is empty.

        Example:
            >>> name_change = NameChange()
            >>> params = {
            ...     "newName": "new_commcell",
            ...     "oldName": "old_commcell",
            ...     "operation": 0,
            ...     "clientIds": [1001, 1002]
            ... }
            >>> name_change._commcell_name_change_op(params)

        #ai-gen-doc
        """

        request_json = {
            "EVGui_ClientNameControlReq":
            {
                "isPostMigration": "",
                "newName": parameters_dict.get("newName", ""),
                "destinationConfiguration": 0,
                "sourceConfiguration": 0,
                "setWithoutConditionFlag": 0,
                "oldName": parameters_dict.get("oldName", ""),
                "commCellId": 0,
                "operation": parameters_dict.get("operation", 0),
                "forceChangeName": 0,
                "clientList": parameters_dict.get("clientIds", [])

            }
        }
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], request_json
        )
        if flag:
            if response.json():
                if 'errorMessage' in response.json():
                    # for errorMessage: "Operation Failed" errorCode: 7
                    error_message = "Failed to do namechange on commserver " \
                                    "with errorCode [{0}], errorMessage [{1}]".format(
                        response.json().get('errorCode'),
                        response.json().get('errorMessage')
                    )
                    raise SDKException('Client', '102', error_message)
                
                elif not 'errorMessage' in response.json():
                    return True

                elif 'errorCode' in response.json().get('error'):
                    error_code = int(
                        response.json().get('error').get('errorCode'))

                    error_message = "Failed to do namechange on commserver " \
                                    "with errorCode [{0}], errorString [{1}]".format(
                        response.json().get('error').get('errorCode'),
                        response.json().get('error').get('errorString')
                    )
                    raise SDKException('Client', '102', error_message)

                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException(
                    'Response', '101', self._update_response_(
                        response.text))
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response. text))

    def get_clients_for_name_change_post_ccm(self) -> list:
        """Retrieve the list of clients available for name change after Commcell migration.

        This method fetches clients that are eligible for a name change operation following a Commcell migration.
        It is typically used in post-migration scenarios to identify clients that require renaming.

        Returns:
            list: A list of client names or client objects available for name change.

        Raises:
            SDKException: If the client name change operation fails or if the response is empty.

        Example:
            >>> name_change = NameChange()
            >>> clients = name_change.get_clients_for_name_change_post_ccm()
            >>> print(f"Clients available for name change: {clients}")

        #ai-gen-doc
        """
        xml = """
            <EVGui_GetClientForNameControlReq>
            </EVGui_GetClientForNameControlReq>
        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], xml
        )
        def get_clients(response):
            clients_list = []
            all_clients = response.json()["clientList"]
            for client in all_clients:
                temp_dict = {}
                name = client.get("name", "")
                domain = client.get("domain", "")
                cs_host_name = client.get("csHostName", "")
                if name + "." + domain != cs_host_name and name != cs_host_name:
                    clients_list.append({"csHostname": cs_host_name, "name": name})
            return clients_list
        if flag:
            if response.json():
                if 'errorCode' in response.json().get('error'):
                    error_code = int(
                        response.json().get('error').get('errorCode'))
                    if error_code != 1:
                        # for errorString: "Failed to get clients for name change operation"
                        # errorCode: 0 or others
                        error_message = "Failed to get clients for name change operation" \
                                        "with errorCode [{0}], errorString [{1}]".format(
                            response.json().get('error').get('errorCode'),
                            response.json().get('error').get('errorString')
                        )
                        raise SDKException('Client', '102', error_message)
                    elif error_code == 1:
                        return get_clients(response)
                elif 'errorMessage' in response.json():
                    error_message = "Failed to get clients for name change operation" \
                                    "with errorCode [{0}], errorMessage [{1}]".format(
                        response.json().get('errorCode'),
                        response.json().get('errorMessage')
                    )
                    raise SDKException('Client', '102', error_message)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException(
                    'Response', '101', self._update_response_(
                        response.text))
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))

    def name_change_post_ccm(self, parameters_dict: dict) -> None:
        """Perform a Commcell name change for clients after Commcell migration.

        This method updates the Commcell association for specified clients, changing their
        reference from the source Commcell hostname to the destination Commcell hostname.

        Args:
            parameters_dict: Dictionary containing the following keys:
                - "sourceCommcellHostname" (str): The hostname of the source Commcell.
                - "destinationCommcellHostname" (str): The hostname of the destination Commcell.
                - "clientIds" (list of str): List of client IDs to update.

                Example:
                    {
                        "sourceCommcellHostname": "source-1",
                        "destinationCommcellHostname": "dest-1",
                        "clientIds": ["id1", "id2"]
                    }

        Raises:
            SDKException: If the client name change fails or if the response is empty.

        Example:
            >>> params = {
            ...     "sourceCommcellHostname": "old-ccm",
            ...     "destinationCommcellHostname": "new-ccm",
            ...     "clientIds": ["234", "123"]
            ... }
            >>> name_change = NameChange()
            >>> name_change.name_change_post_ccm(params)
            >>> print("Name change completed successfully.")

        #ai-gen-doc
        """
        name_change_xml = """
            <EVGui_ClientNameControlReq 
                commCellId="0" 
                destinationConfiguration="2" 
                isPostMigration="1" 
                newName="{0}"
                oldName="{1}"
                operation="139" 
                setWithoutConditionFlag="0" 
                sourceConfiguration="2"> 
                {2}
            </EVGui_ClientNameControlReq>
        """
        client_tag = """
            <clientList val= "{0}"/>
        """
        clients_string = ""
        for clients_id in parameters_dict.get("clientIds", []):
            clients_string += client_tag.format(clients_id)
        name_change_xml = name_change_xml.format(parameters_dict["destinationCommcellHostname"],
                                                 parameters_dict["sourceCommcellHostname"],
                                                 clients_string)
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], name_change_xml
        )
        if flag:
            if response.json():
                if 'errorCode' in response.json().get('error'):
                    error_code = int(
                        response.json().get('error').get('errorCode'))
                    if error_code != 1:
                        error_message = "Failed to perform name change operation" \
                                        "with errorCode [{0}], errorString [{1}]".format(
                                        response.json().get('error').get('errorCode'),
                                        response.json().get('error').get('errorString')
                                        )
                        raise SDKException('Client', '102', error_message)
                    elif error_code == 1:
                        return True
                elif 'errorMessage' in response.json():
                    error_message = "Failed to get clients for name change operation" \
                                    "with errorCode [{0}], errorMessage [{1}]".format(response.json().get('errorCode'),
                                                                                      response.json().get(
                                                                                          'errorMessage')
                                                                                      )
                    raise SDKException('Client', '102', error_message)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException(
                    'Response', '101', self._update_response_(
                        response.text))
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))