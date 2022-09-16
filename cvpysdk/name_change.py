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


class OperationType(Enum):
    """ Operation Types supported to get schedules of particular optype"""
    COMMSERVER_HOSTNAME_REMOTE_CLIENTS = 147
    COMMSERVER_HOSTNAME_AFTER_DR = 139
    CLIENT_HOSTNAME = "CLIENT_HOSTNAME"
    COMMSERVER_HOSTNAME = "COMMSERVER_HOSTNAME"


class NameChange(object):
    """Class for doing Name Change operations on clients and commcell"""

    def __init__(self, class_object):
        """Initializes an instance of the NameChange class to perform Name Change operations.

            Args:
                class_object (object)  --  instance of the client/commcell class

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
    def hostname(self):
        """
        Gets the client hostname or commserver hostname

         Returns:
                str - client hostname or commserver hostname
        """
        if self._is_client:
            return self._client_hostname
        else:
            return self._commcell_name

    @hostname.setter
    def hostname(self, parameters_dict):
        """
        Sets the client hostname or commserver hostname with the parameters provided
        Args:
            parameters_dict (str)      -- dictionary of parameters for namechange
                                    {
                                    "operation": Operation type to be performed on the client or
                                                commserver (OperationType)
                                    "ClientHostname":   Client hostname to be updated (str)
                                    "CommserverHostname":   Commserver hostname to be updated (str)
                                    "oldName":  old commserver hostname
                                    "newName":  new commserver hostname
                                    }

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
    def domain_name(self):
        """
        Gets the commserver hostname

        Returns:
                str - commserver hostname
        """
        return self._commcell_name

    @domain_name.setter
    def domain_name(self, domains_dict):
        """
        Sets the new domain name for the clients with the parameter provided
        Args:
            domains_dict (dict) -- new client domain name
                                    {
                                    "oldDomain": old client domain name (str)
                                    "newDomain": new client domain name (str)
                                    }

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
    def display_name(self):
        """
        Gets the display name of the client or commserver

        Returns:
                str - client or commserver display name
        """
        if self._is_client:
            return self._display_name
        else:
            return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display name of the client or commserver with the parameter provided
        Args:
            display_name (str) -- new client or commserver display name

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
    def client_name(self):
        """
        Gets the client name

        Returns:
                str - client name
        """
        if self._is_client:
            return self._client_name
        else:
            False

    @client_name.setter
    def client_name(self, client_name):
        """
        Sets the name of the client with the parameter provided
        Args:
            client_name (str) -- new client name

        """
        self._new_name = client_name
        self._client_name_change_op()

    def _client_name_change_op(self):
        """
        Performs the client namechange operations

            Raises:
            SDKException::
                if the client namechange failed

                if the response is empty
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

    def _commcell_name_change_op(self, parameters_dict):
        """
        Performs the commcell namechange operations

        Args:
            parameters_dict (dict)          --  dictionary with common namechange parameters like
                                                old commserver hostname, new commserver hostname
                                                or old domain name, new domain name, client IDs.
                                                clientIds can be an empty list too.
                                                  {"newName",
                                                    "oldName",
                                                    "operation",
                                                    "clientIds"}

            Raises:
            SDKException::
                if the client namechange failed

                if the response is empty

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
                if 'errorCode' in response.json().get('error'):
                    error_code = int(
                        response.json().get('error').get('errorCode'))
                    if error_code != 1:
                        # for errorString: "Failed to set Client properties."
                        # errorCode: 0 or others
                        error_message = "Failed to do namechange on commserver " \
                                        "with errorCode [{0}], errorString [{1}]".format(
                                            response.json().get('error').get('errorCode'),
                                            response.json().get('error').get('errorString')
                                        )
                        raise SDKException('Client', '102', error_message)

                    elif error_code == 1:
                        return True

                elif 'errorMessage' in response.json():
                        # for errorMessage: "Operation Failed" errorCode: 7
                    error_message = "Failed to do namechange on commserver " \
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
                    response. text))

    def get_clients_for_name_change_post_ccm(self):
        """
            Gets clients available for name change after commcell migration.
            Raises:
            SDKException::
                if the client namechange failed
                if the response is empty
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

    def name_change_post_ccm(self, parameters_dict):
        """
        Performs the commcell namechange for clients post commcell migration
        Args:
            parameters_dict (dict)      --  contains old commcell hostname, new commcell hostname,
                                            Ids of clients on which name change is to be performed
                                            {
                                            "sourceCommcellHostname": "source-1"
                                            "destinationCommcellHostname": "dest-1"
                                            "clientIds": ["id1", "id2"]
                                            }
            Raises:
            SDKException::
                if the client namechange failed
                if the response is empty
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