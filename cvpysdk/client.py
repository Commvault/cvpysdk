#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing client operations.

Clients and Client are 2 classes defined in this file.

Clients: Class for representing all the clients associated with the commcell

Client: Class for a single client of the commcell


Clients:
    __init__(commcell_object) -- initialise object of Clients class associated with the commcell
    __repr__()                -- return all the clients associated with the commcell
    _get_clients()            -- gets all the clients associated with the commcell
    has_client(client_name)   -- checks if a client exists with the given name or not
    get(client_name)          -- returns the Client class object of the input client name
    delete(client_name)       -- deletes the client specified by the client name from the commcell


Client:
    __init__(commcell_object,
             client_name,
             client_id=None)  -- initialise object of Class with the specified client name
                                     and id, and associated to the commcell
    __repr__()                -- return the client name and id, the instance is associated with
    _get_client_id()          -- method to get the client id, if not specified in __init__
    _get_client_properties()  -- get the properties of this client

"""


from agent import Agents
from schedules import Schedules
from exception import SDKException


class Clients(object):
    """Class for getting all the clients associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the Clients class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the Clients class
        """
        self._commcell_object = commcell_object
        self._CLIENTS = self._commcell_object._services.GET_ALL_CLIENTS
        self._clients = self._get_clients()

    def __repr__(self):
        """Representation string for the instance of the Clients class.

            Returns:
                str - string of all the clients associated with the commcell
        """
        representation_string = ''
        for client_name, client_id in self._clients.items():
            sub_str = 'Client "{0}" of Commcell: "{1}"\n'
            sub_str = sub_str.format(client_name, self._commcell_object._headers['Host'])
            representation_string += sub_str

        return representation_string.strip()

    def _get_clients(self):
        """Gets all the clients associated with the commcell

            Returns:
                dict - consists of all clients in the commcell
                    {
                         "client1_name": client1_id,
                         "client2_name": client2_id
                    }

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._CLIENTS)

        if flag:
            if response.json():
                clients_dict = {}

                for dictionary in response.json()['clientProperties']:
                    temp_name = str(dictionary['client']['clientEntity']['clientName']).lower()
                    temp_id = str(dictionary['client']['clientEntity']['clientId']).lower()
                    clients_dict[temp_name] = temp_id

                return clients_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def has_client(self, client_name):
        """Checks if a client exists in the commcell with the input client name.

            Args:
                client_name (str)  --  name of the client

            Returns:
                bool - boolean output whether the client exists in the commcell or not

            Raises:
                SDKException:
                    if type of the client name argument is not string
        """
        if not isinstance(client_name, str):
            raise SDKException('Client', '103')

        return self._clients and str(client_name).lower() in self._clients

    def get(self, client_name):
        """Returns a client object of the specified client name.

            Args:
                client_name (str)  --  name of the client

            Returns:
                object - instance of the Client class for the given client name

            Raises:
                SDKException:
                    if type of the client name argument is not string
                    if no client exists with the given name
        """
        if not isinstance(client_name, str):
            raise SDKException('Client', '103')
        else:
            client_name = str(client_name).lower()

            if self.has_client(client_name):
                return Client(self._commcell_object, client_name, self._clients[client_name])

            raise SDKException('Client',
                               '104',
                               'No client exists with name: {0}'.format(client_name))

    def delete(self, client_name):
        """Deletes the client from the commcell.

            Args:
                client_name (str)  --  name of the client to remove from the commcell

            Returns:
                None

            Raises:
                SDKException:
                    if type of the client name argument is not string
                    if response is empty
                    if response is not success
                    if no client exists with the given name
        """
        if not isinstance(client_name, str):
            raise SDKException('Client', '103')
        else:
            client_name = str(client_name).lower()

            if self.has_client(client_name):
                client_id = self._clients[client_name]
                CLIENT = self._commcell_object._services.CLIENT % (client_id)
                CLIENT += "?forceDelete=1"

                flag, response = self._commcell_object._cvpysdk_object.make_request('DELETE',
                                                                                    CLIENT)

                error_code = warning_code = 0

                if flag:
                    if response.json():
                        if 'response' in response.json():
                            if response.json()['response'][0]['errorCode'] == 0:
                                o_str = 'Client: "{0}" deleted successfully'
                                print o_str.format(client_name)
                            else:
                                print response.text
                            self._clients = self._get_clients()
                        else:
                            if 'errorCode' in response.json():
                                error_code = response.json()['errorCode']

                            if 'warningCode' in response.json():
                                warning_code = response.json()['warningCode']

                            if error_code != 0:
                                print response.json()['errorMessage']
                            elif warning_code != 0:
                                print response.json()['warningMessage']
                    else:
                        raise SDKException('Response', '102')
                else:
                    exception_message = 'Failed to delete the client: {0}'.format(client_name)
                    response_string = self._commcell_object._update_response_(response.text)
                    exception_message += "\n" + response_string

                    raise SDKException('Client',
                                       '104',
                                       exception_message)
            else:
                raise SDKException('Client',
                                   '104',
                                   'No client exists with name: {0}'.format(client_name))


class Client(object):
    """Class for performing client operations for a specific client."""

    def __init__(self, commcell_object, client_name, client_id=None):
        """Initialise the Client class instance.

            Args:
                commcell_object (object)  --  instance of the Commcell class
                client_name (str)         --  name of the client
                client_id (str)           --  id of the client
                    default: None

            Returns:
                object - instance of the Client class
        """
        self._commcell_object = commcell_object
        self._client_name = str(client_name).lower()

        if client_id:
            self._client_id = str(client_id)
        else:
            self._client_id = self._get_client_id()

        self._CLIENT = self._commcell_object._services.CLIENT % (self.client_id)
        self.properties = self._get_client_properties()

        self.agents = Agents(self)
        self.schedules = Schedules(self).schedules

    def __repr__(self):
        """String representation of the instance of this class.

            Returns:
                str - string containing the details of this client
        """
        representation_string = 'Client instance for Client: "{0}", of Commcell: "{1}"'

        return representation_string.format(self.client_name,
                                            self._commcell_object._headers['Host'])

    def _get_client_id(self):
        """Gets the client id associated with this client.

            Returns:
                str - id associated with this client
        """
        clients = Clients(self._commcell_object)
        return clients.get(self.client_name).client_id

    def _get_client_properties(self):
        """Gets the client properties of this client.

            Returns:
                dict - dictionary consisting of the properties of this client

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET',
                                                                            self._CLIENT)

        if flag:
            if response.json() and 'clientProperties' in response.json().keys():
                if isinstance(response.json()['clientProperties'][0], dict):
                    return response.json()['clientProperties'][0]
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def client_id(self):
        """Treats the client id as a read-only attribute."""
        return self._client_id

    @property
    def client_name(self):
        """Treats the client name as a read-only attribute."""
        return self._client_name
