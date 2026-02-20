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
Main file for performing service commcell related operations

ServiceCommcells: Class for managing Service Commcells registered to this router commcell
    Methods:
        add()                       --  registers a service commcell
        has_service_commcell()      --  checks if a service commcell with the given name exists
        delete()                    --  deletes a service commcell with the given name
        get()                       --  gets the service commcell object for the given service commcell
        refresh()                   --  refreshes the cached service commcells information
        get_service_rules()         --  gets the service rules for this commcell to be shared with router commcell

    Properties:
        associations                --  returns an Associations object for managing associations of service commcells
        all_service_commcells       --  returns all service commcell details
        global_mongo_status         --  returns the global mongoDB status/health for each registered service commcell
        commcells_for_user          --  returns the list of accessible commcells to currently logged user
        commcells_for_switching     --  returns the commcell details for all switchable commcells


ServiceCommcell: Class for performing operations on a single service commcell
    Methods:
        update()                    --  updates the properties of the service commcell
        reregister()                --  reregisters this commcell with the provided username and password
        refresh_sync()              --  refreshes the service commcell's properties synced with the router commcell
        refresh()                   --  refreshes the cached properties of the service commcell obj

    Properties:
        props                       --  returns the properties of the service commcell
        commcell_id                 --  returns the commcell ID of the service commcell
        cs_guid                     --  returns the csGUID of the service commcell
        client_id                   --  returns the client ID of the service commcell
        client_name                 --  returns the client name of the service commcell
        interface_name              --  returns the interface name of the service commcell
        display_name                --  returns the display name of the service commcell
        webconsole_url              --  returns the webconsole URL of the service commcell
        service_pack_info           --  returns the service pack information of the service commcell
        sync_status                 --  returns the sync status of the service commcell
        role_string                 --  returns the role string of the service commcell
        details                     --  returns detailed properties of the service commcell
        associations                --  Associations object for managing associations of this service commcell


Associations:  Class for managing associations of service commcell(s)
    Methods:
        get()                       --  gets an entity's association details
        add()                       --  adds entity association to the specified service commcell
        delete()                    --  deletes entity associations from the specified service commcell(s)

    Properties:
        all_associations            --  returns all associations of service commcells
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from base64 import b64encode
from typing import Any, TYPE_CHECKING

from .exception import SDKException
if TYPE_CHECKING:
    from .commcell import Commcell


class ServiceCommcells:
    """
    Class for performing service commcell operations.

    Attributes:
        _commcell (Commcell): Instance of the Commcell class.
        associations (Associations): Instance of the Associations class.
        _service_commcells (dict[str, dict[str, Any]] | None): Cached service commcells information.
        _global_mongo_status (dict | None): Cached global MongoDB status.
        _commcells_for_user (list[dict[str, Any]] | None): Cached list of accessible commcells for the user.
        _commcells_for_switching (dict[str, Any] | None): Cached commcell details for switching.
    Usage:
        >>> service_commcells = ServiceCommcells(commcell_object)
    """
    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialise the Activity control class instance.

            Args:
                commcell_object (Commcell): instance of the Commcell class

            Returns:
                object: instance of the ServiceCommcells class
        """
        self._commcell = commcell_object
        self.associations = Associations(self._commcell)
        self._service_commcells: dict[str, dict[str, Any]] | None = None
        self._global_mongo_status: dict | None = None
        self._commcells_for_user: list[dict[str, Any]] | None = None
        self._commcells_for_switching: dict[str, Any] | None = None

    def __repr__(self) -> str:
        """String representation of the instance of this class."""
        return f'ServiceCommcells class instance for commcell: {self._commcell.webconsole_hostname}'

    def __getitem__(self, item: str) -> 'ServiceCommcell':
        """
        Gets the service commcell object for the given service commcell.
        Performs advanced lookup allowing match from any identifying commcell property.

        Args:
            item (str): commserv name of the service commcell

        Returns:
            ServiceCommcell: The service commcell object.

        Usage:
            >>> service_commcell = service_commcells['commcell_name']
        """
        return self.get(item, True)

    def refresh(self) -> None:
        """
        Refreshes the cached service commcells information.

        Usage:
            >>> service_commcells.refresh()
        """
        self._service_commcells = None
        self._global_mongo_status = None
        self._commcells_for_user = None
        self._commcells_for_switching = None
        self.associations.refresh()

    def _get_commcells_for_switching(self) -> dict[str, Any]:
        """
        returns the commcell details for all switchable commcells

        Returns:
            dict: dict with details on accessible commcells

        Raises:
            SDKException:
                if response is empty

                if response is not success

        Usage:
            >>> commcells_for_switching = service_commcells._get_commcells_for_switching()
            Example:
            {
                'serviceCommcell': [
                    {'webUrl': '...', 'commcellRole': ..., 'commcellHostname': '...'},
                    {...}, {...},
                ]
                'IDPCommcell': {...},
                'routerCommcell': [{...}]
            }
        """
        return self._commcell.wrap_request('GET', 'MULTI_COMMCELL_SWITCHER')

    def _get_commcells_for_user(self) -> list[dict[str, Any]]:
        """
        Returns the list of accessible commcells to currently logged user

        Returns:
            list: consists list of dicts with info about accessible commcells

        Raises:
            SDKException:
                if response is empty

                if response is not success

        Usage:
            >>> commcells_for_user = service_commcells._get_commcells_for_user()
            Example:
                [
                    {'redirectUrl': '', 'commcellName': '', 'commcellType': ''},
                    {...},
                    ...
                ]
        """
        return self._commcell.wrap_request('GET', 'MCC_FOR_USER').get('AvailableRedirects', [])

    def _get_global_mongodb_status(self) -> dict:
        """
        returns the Global mongoDB status/health for each registered service commcell

        Returns:
            dict: dict with global mongo status details

        Raises:
            SDKException:
                if response is empty

                if response is not success

        Usage:
            >>> global_mongo_status = service_commcells._get_global_mongodb_status()
        """
        with self._commcell.global_scope():
            response = self._commcell.wrap_request('GET', 'GLOBAL_MONGODB_STATUS')
        return {
            cs_prop['commcellName']: cs_prop for cs_prop in response
        }

    def _get_service_commcells(self) -> dict[str, dict[str, Any]]:
        """
        Gets the registered routing commcells

        Returns:
            dict: consists of all registered routing commcells

        Raises:
            SDKException:
                if response is empty

                if response is not success

        Usage:
            >>> service_commcells_data = service_commcells._get_service_commcells()
            Example:
                {
                    "commcell_name1": {
                        'displayName': ...,
                        'multiCommcellType': ...,
                        'statusDetail': ...,
                        'disableAggregation': ...,
                        'lastSyncWithIDP': ...,
                        'activeManagementStatus': ...
                        ....
                    },
                    "commcell_name2:: {...}
                }
        """
        resp = self._commcell.wrap_request(
            'GET', 'SERVICE_COMMCELLS', empty_check=False
        )
        return {
            commcell['commCell']['commCellName']: commcell
            for commcell in resp.get('commcellsList', [])
        }

    def add(self, cc_url: str, username: str, password: str, **kwargs: Any) -> None:
        """
        Registers a service commcell

        Args:
            cc_url   (str): command center URL of the service commcell to register
            username (str): username of the user who has administrative rights on a commcell
            password (str): password of the user specified
            **kwargs: any other payload parameters to pass

        Raises:
            SDKException:
                if the registration fails
                if response is empty
                if there is no response

        Usage:
            >>> service_commcells.add(cc_url='https://example.com/commandcenter', username='admin', password='password')
            >>> service_commcells.add(cc_url='https://example.com/commandcenter', username='admin', password='password', isIDPCommcell=True)
        """
        cc_url = cc_url.lower()
        if not cc_url.endswith("/commandcenter"):
            cc_url = cc_url.rstrip('/')
            cc_url += '/commandcenter'
        if not cc_url.startswith("https://") or cc_url.startswith("http://"):
            cc_url = "http://" + cc_url

        payload = {
            "serviceCommcelWebconsoleUrl": cc_url,
            "username": username,
            "password": b64encode(password.encode()).decode(),
            "isIDPCommcell": False,
            "userOrGroup": [],
        } | kwargs

        self._commcell.wrap_request(
            'POST', 'SERVICE_REGISTER', req_kwargs={'payload': payload},
            sdk_exception=('ServiceCommcells', '102'),
        )
        self.refresh()

    def has_service_commcell(self, commcell_name: str) -> bool:
        """
        Checks if the service commcell with the given name exists

        Args:
            commcell_name (str): commserv name of the service commcell

        Returns:
            bool: True if service commcell exists, False otherwise

        Usage:
            >>> has_commcell = service_commcells.has_service_commcell(commcell_name='commcell_name')
        """
        return commcell_name in self.all_service_commcells

    def delete(self, commcell_name: str, force: bool = False) -> None:
        """
        Deletes the service commcell with the given name

        Args:
            commcell_name (str): commserv name of the service commcell
            force       (bool): if True, forces the deletion without confirmation

        Usage:
            >>> service_commcells.delete(commcell_name='commcell_name')
            >>> service_commcells.delete(commcell_name='commcell_name', force=True)
        """
        payload = {
          "commcell": {
            "commCell": {
              "commCellId": self[commcell_name].commcell_id,
              "csGUID": self[commcell_name].cs_guid,
            },
            "ccClientId": self[commcell_name].client_id,
            "ccClientName": self[commcell_name].client_name,
            "interfaceName": self[commcell_name].interface_name
          },
          "forceUnregister": force
        }

        self._commcell.wrap_request(
            'POST', 'UNREGISTRATION',
            req_kwargs={'payload': payload},
            sdk_exception=('ServiceCommcells', '103')
        )
        self.refresh()

    def get(self, commcell_name: str, adv_lookup: bool = False) -> 'ServiceCommcell':
        """
        Gets the service commcell object for the given service commcell

        Args:
            commcell_name (str): commserv name of the service commcell
            adv_lookup    (bool): if True, performs an advanced lookup allowing match from any partial property

        Raises:
            SDKException:
                if no service commcell is found with the given name

        Returns:
            ServiceCommcell: The service commcell object.

        Usage:
            >>> service_commcell = service_commcells.get(commcell_name='commcell_name')
        """
        if commcell_name in self.all_service_commcells:
            return ServiceCommcell(self._commcell, commcell_name)
        else:
            if adv_lookup:
                if found_name := self.lookup_name(commcell_name):
                    return ServiceCommcell(self._commcell, found_name)
            raise SDKException(
                'ServiceCommcells',
                '102',
                f'No service commcell found with name: {commcell_name}. '
                f'Choose from {list(self.all_service_commcells.keys())}'
            )

    def lookup_name(self, lookup_prop: Any) -> str | None:
        """
        Looks up the commcell name from any identifying property of the service commcell

        Args:
            lookup_prop (Any): any identifying property of the service commcell

        Returns:
            str: commcell name of the service commcell
        """
        # risky fuzzy matching from any commcell property
        # responsibility on caller to provide unique enough input
        for cs_name, cs_props in self.all_service_commcells.items():
            # prioritize perfect matches
            if str(lookup_prop).lower() == cs_name.lower():
                return cs_name
            for prop_value in cs_props.values():
                if prop_value == lookup_prop:
                    return cs_name
                if isinstance(prop_value, dict):
                    ...  # todo: recurse

            # substr case-insensitive matches
            if str(lookup_prop).lower() in cs_name.lower():
                return cs_name
            for prop_value in cs_props.values():
                if str(lookup_prop).lower() in str(prop_value).lower():
                    return cs_name
                if isinstance(prop_value, dict):
                    ...  # todo: recurse
        return None

    @property
    def all_service_commcells(self) -> dict[str, Any]:
        """
        Returns all service commcell details

        Usage:
            >>> all_commcells = service_commcells.all_service_commcells
            Example:
            {
                "commcell_name1": {
                    'displayName': ...,
                    'multiCommcellType': ...,
                    'statusDetail': ...,
                    'disableAggregation': ...,
                    'lastSyncWithIDP': ...,
                    'activeManagementStatus': ...
                    ....
                },
                "commcell_name2:: {...}
            }
        """
        if self._service_commcells is None:
            self._service_commcells = self._get_service_commcells()
        return self._service_commcells

    @property
    def global_mongo_status(self) -> dict:
        """
        Returns the global mongoDB status/health for each registered service commcell

        Usage:
            >>> mongo_status = service_commcells.global_mongo_status
        """
        if self._global_mongo_status is None:
            self._global_mongo_status = self._get_global_mongodb_status()
        return self._global_mongo_status

    @property
    def commcells_for_user(self) -> list[dict[str, Any]]:
        """
        Returns the list of accessible commcells to currently logged user

        Returns:
            list: consisting of all accessible commcells to the user

        Usage:
            >>> commcells = service_commcells.commcells_for_user
            Example:
                [
                    {'redirectUrl': '', 'commcellName': '', 'commcellType': ''},
                    {...},
                    ...
                ]
        """
        if self._commcells_for_user is None:
            self._commcells_for_user = self._get_commcells_for_user()
        return self._commcells_for_user

    @property
    def commcells_for_switching(self) -> dict[str, Any]:
        """
        Returns the commcell details for all switchable commcells

        Returns:
            dict: dict with details on service, IDP and router commcells

        Usage:
            >>> switchable_commcells = service_commcells.commcells_for_switching
            Example:
            {
                'serviceCommcell': [
                    {'webUrl': '...', 'commcellRole': ..., 'commcellHostname': '...'},
                    {...}, {...},
                ]
                'IDPCommcell': {...},
                'routerCommcell': [{...}]
            }
        """
        if self._commcells_for_switching is None:
            self._commcells_for_switching = self._get_commcells_for_switching()
        return self._commcells_for_switching

class ServiceCommcell:
    """
    Class for performing operations on a service commcell.

    Attributes:
        _commcell (Commcell): Instance of the Commcell class.
        commcell_name (str): Commserve name of the service commcell.
        associations (Associations): Associations object for the service commcell.
        _props (dict): Properties of the service commcell.
        _details (dict): Detailed properties of the service commcell.
        _mongo_status (dict): MongoDB status of the service commcell.

    Usage:
        >>> service_commcell = ServiceCommcell(commcell_object, "service_commcell_name")
    """
    def __init__(self, commcell_object: 'Commcell', commcell_name: str) -> None:
        """
        Initialise the ServiceCommcell class instance.

        Args:
            commcell_object (Commcell): instance of the Commcell class
            commcell_name (str): commserve name of the service commcell

        Returns:
            object: instance of the ServiceCommcell class
        """
        self._commcell = commcell_object
        self.commcell_name = commcell_name
        self.associations = Associations(self._commcell, commcell_name)
        self._props = None
        self._details = None
        self._mongo_status = None

    def __repr__(self) -> str:
        """String representation of the instance of this class."""
        return f'service commcell {self.commcell_name} of router commcell: {self._commcell.webconsole_hostname}'

    def refresh(self) -> None:
        """
        Refreshes the properties of the service commcell.

        Usage:
            >>> service_commcell.refresh()
        """
        self._props = None
        self._details = None
        self._mongo_status = None
        self._commcell.service_commcells.refresh()
        self.associations.refresh()

    def _get_details(self) -> dict:
        """
        Gets the detailed props of the service commcell, using properties API

        Returns:
            dict: detailed properties of the service commcell
            {
                'associations': [...],
                'properties': {
                    'webServiceUrl': ...,
                    'commCellName': ...,
                    'commcellNumber': ...,
                    'servicePackInfo': ...,
                    ...
                }
            }

        Usage:
            >>> details = service_commcell._get_details()
        """
        return self._commcell.wrap_request(
            'GET', 'SERVICE_PROPS',
            req_kwargs={'params': {'commcellId': self.commcell_id}}
        )

    def update(self, properties: dict) -> str:
        """
        Updates the properties of the service commcell.

        Args:
            properties (dict): dict with properties to be updated
                example: {'displayName': '...', 'webconsoleUrl': '...'}

        Returns:
            str: The value of the 'comet-response' header from the response.

        Usage:
            >>> service_commcell.update({'displayName': 'New Display Name'})
        """
        payload = {
            "properties": {'csGUID': self.cs_guid.upper()} | properties
        }
        response = self._commcell.wrap_request(
            'POST', 'SERVICE_PROPS',
            req_kwargs={'payload': payload},
            sdk_exception=('ServiceCommcells', '106'),
            return_resp=True
        )
        self.refresh()
        return response.headers.get("comet-response")

    def reregister(self, username: str, password: str) -> None:
        """
        Reregisters this commcell with the provided username and password.

        Args:
            username (str): username of the user who has administrative
                                                rights on a commcell

            password (str): password of the user

        Usage:
            >>> service_commcell.reregister("admin", "password")
        """
        payload = {
            "username": username,
            "password": b64encode(password.encode()).decode(),
        }
        self._commcell.wrap_request(
            'POST', 'SERVICE_REREGISTER', (self.commcell_id,),
            req_kwargs={'payload': payload},
            sdk_exception=('ServiceCommcells', '107'),
        )
        self.refresh()

    def refresh_sync(self) -> None:
        """
        Refresh the service commcell's properties synced with the router commcell.

        Raises:
            SDKException: if sync fails, the response is empty, or there is no response.

        Usage:
            >>> service_commcell.refresh_sync()
        """
        payload = {'commcellId': self.commcell_id}
        self._commcell.wrap_request(
            'GET', 'SYNC_SERVICE_COMMCELL', (self.commcell_id,),
            req_kwargs={'params': payload},
            sdk_exception=('ServiceCommcells', '108'),
            error_check=True
        )
        self.refresh()

    @property
    def props(self) -> dict:
        """
        Returns the properties of the service commcell.

        Raises:
            SDKException: if no properties are returned for the service commcell.

        Returns:
            dict: The properties of the service commcell.

        Usage:
            >>> props = service_commcell.props
        """
        if self._props is None:
            self._props = self._commcell.service_commcells.all_service_commcells.get(self.commcell_name)
            if not self._props:
                raise SDKException(
                    'ServiceCommcells', '105', f'No props returned for: {self.commcell_name}'
                )
        return self._props

    @property
    def commcell_id(self) -> int:
        """
        Returns the commcell ID of the service commcell.

        Returns:
            int: The commcell ID.

        Usage:
            >>> commcell_id = service_commcell.commcell_id
        """
        return self.props.get('commCell', {}).get('commCellId')

    @property
    def cs_guid(self) -> str:
        """
        Returns the csGUID of the service commcell.

        Returns:
            str: The csGUID.

        Usage:
            >>> cs_guid = service_commcell.cs_guid
        """
        return self.props.get('commCell', {}).get('csGUID')

    @property
    def client_id(self) -> int:
        """
        Returns the client ID of the service commcell.

        Returns:
            int: The client ID.

        Usage:
            >>> client_id = service_commcell.client_id
        """
        return self.props.get('ccClientId')

    @property
    def client_name(self) -> str:
        """
        Returns the client name of the service commcell.

        Returns:
            str: The client name.

        Usage:
            >>> client_name = service_commcell.client_name
        """
        return self.props.get('ccClientName')

    @property
    def interface_name(self) -> str:
        """
        Returns the interface name of the service commcell.

        Returns:
            str: The interface name.

        Usage:
            >>> interface_name = service_commcell.interface_name
        """
        return self.props.get('interfaceName')

    @property
    def display_name(self) -> str:
        """
        Returns the display name of the service commcell.

        Returns:
            str: The display name.

        Usage:
            >>> display_name = service_commcell.display_name
        """
        return self.props.get('displayName')

    @display_name.setter
    def display_name(self, value: str) -> None:
        """
        Sets the display name of the service commcell.

        Args:
            value (str): new display name to set

        Usage:
            >>> service_commcell.display_name = "New Display Name"
        """
        self.update({'displayName': value})

    @property
    def webconsole_url(self) -> str:
        """
        Returns the webconsole URL of the service commcell.

        Returns:
            str: The webconsole URL.

        Usage:
            >>> webconsole_url = service_commcell.webconsole_url
        """
        return self.props.get('webconsoleUrl')

    @property
    def service_pack_info(self) -> str:
        """
        Returns the service pack information of the service commcell.

        Returns:
            str: The service pack information.

        Usage:
            >>> service_pack_info = service_commcell.service_pack_info
        """
        return self.props.get('servicePackInfo')

    @property
    def sync_status(self) -> bool:
        """
        Returns the sync status of the service commcell.

        Returns:
            bool: The sync status.

        Usage:
            >>> sync_status = service_commcell.sync_status
        """
        return self.props.get('syncStatus', {}).get('status') == 1

    @property
    def role_string(self) -> str:
        """
        Returns the role string of the service commcell.

        Returns:
            str: The role string.

        Usage:
            >>> role_string = service_commcell.role_string
        """
        return self.props.get('commcellRoleString', '')

    @property
    def details(self) -> dict:
        """
        Returns the detailed properties of the service commcell.

        Returns:
            dict: The detailed properties.

        Usage:
            >>> details = service_commcell.details
        """
        if self._details is None:
            self._details = self._get_details()
        return self._details

    @property
    def mongo_status(self) -> dict:
        """
        Returns the mongoDB status/health of the service commcell

        Returns:
            dict: consisting of mongoDB status details

        Usage:
            >>> mongo_status = service_commcell.mongo_status
        """
        if self._mongo_status is None:
            self._mongo_status = self._commcell.service_commcells.global_mongo_status.get(self.commcell_name)
        return self._mongo_status

class Associations:
    """
    Class for managing associations of service commcells.

    Attributes:
        entity_payload_map (dict): A mapping of entity types to payload generation functions.
    Usage:
        associations = Associations(commcell_object)
    """
    entity_payload_map = {
        'User': lambda entity: {
            'userOrGroup': {
                'userId': int(entity.user_id),
                'userName': entity.user_name,
                '_type_': 13
            }
        },
        'UserGroup': lambda entity: {
            'userOrGroup': {
                'userGroupId': int(entity.user_group_id),
                'userGroupName': entity.user_group_name,
                '_type_': 15
            }
        },
        'Organization': lambda entity: {
            'providerType': 5,  # todo: this may be 15 or 5 depending on something
            'userOrGroup': {
                'providerId': int(entity.organization_id),
                'providerDomainName': entity.domain_name,
                '_type_': 61,
                'GUID': entity.provider_guid,
                'entityInfo': {
                    "multiCommcellName": entity._commcell_object.commserv_client.client_name
                }
            }
        }
    }

    @staticmethod
    def lookup_entity_type(entity: Any) -> str:
        """
        Returns the entity type string for the given entity object.

        Args:
            entity (Any): object of User, UserGroup, Domain or Organization class
                              or Any Derived class of the Above

        Returns:
            str: entity type string

        Raises:
            SDKException: if the entity type is invalid.

        Usage:
            entity_type = Associations.lookup_entity_type(entity)
        """
        for cls in type(entity).__mro__:
            name = cls.__name__
            if name in Associations.entity_payload_map:
                return name
        raise SDKException('ServiceCommcells', '101', f'Invalid entity type: {type(entity)} : {entity}')

    @staticmethod
    def lookup_entities_type(entities: list[Any]) -> str:
        """
        Returns the entity type string for the given list of entity objects.

        Args:
            entities (list[Any]): list of objects of User, UserGroup, Domain or Organization class
                                      or Any Derived class of the Above

        Returns:
            str: entity type string

        Raises:
            SDKException: if the entity types are not all the same or invalid.

        Usage:
            entity_type = Associations.lookup_entities_type([entity1, entity2, ...])
        """
        if all(
            Associations.lookup_entity_type(entity) == 'Organization' for entity in entities
        ):
            return 'Organization'
        elif all(
            Associations.lookup_entity_type(entity) in ('User', 'UserGroup') for entity in entities
        ):
            return 'Security'
        else:
            raise SDKException(
                'ServiceCommcells', '101', 'Invalid/Mixed entity types in the provided list of entities.'
            )

    @staticmethod
    def lookup_entity_payload(entity: Any) -> dict:
        """
        Returns the payload for the given entity type.

        Args:
            entity (Any): object of User, UserGroup, Domain or Organization class
                              or Any Derived class of the Above

        Returns:
            dict: payload for the entity

        Raises:
            SDKException: if the entity type is invalid.

        Usage:
            payload = Associations.lookup_entity_payload(entity)
        """
        return Associations.entity_payload_map[
            Associations.lookup_entity_type(entity)
        ](entity)

    @staticmethod
    def reverse_lookup_assoc(assoc: dict) -> str:
        """
        Returns the entity type string for the given association dict.

        Args:
            assoc (dict): association dict

        Returns:
            str: entity type string
        """
        entity_type = assoc.get('userOrGroup', {}).get('_type_')
        if entity_type == 61:
            return 'Organization'
        elif entity_type in (13, 15):
            return 'Security'
        else:
            raise SDKException(
                'ServiceCommcells', '101', f'Invalid/Unknown association type: {entity_type} in : {assoc}'
            )

    @staticmethod
    def reverse_lookup_type(assocs: list[dict]) -> str:
        """
        Returns the entity type string for the given list of association dicts.

        Args:
            assocs (list[dict]): list of association dicts

        Returns:
            str: entity type string

        Raises:
            SDKException: if the association types are not all the same or invalid.
        """
        if all(
            Associations.reverse_lookup_assoc(assoc) == 'Organization' for assoc in assocs
        ):
            return 'Organization'
        elif all(
            Associations.reverse_lookup_assoc(assoc) == 'Security' for assoc in assocs
        ):
            return 'Security'
        else:
            raise SDKException(
                'ServiceCommcells', '101', 'Got Mixed association entity types'
            )

    def __init__(self, commcell_object: Any, filter_commcell: str = None) -> None:
        """
        Initialise the Associations class instance.

        Args:
            commcell_object (Any): instance of the Commcell class
            filter_commcell (str): commserv name of the service commcell to filter associations

        Usage:
            associations = Associations(commcell_object, filter_commcell='commserve1')
        """
        self._commcell = commcell_object
        self._filter_commcell = filter_commcell
        self._associations = None
        self._company_associations = None
        self._security_associations = None

    @property
    def _sc_id(self) -> int | None:
        """ Internal property to get the service commcell ID if any. """
        if self._filter_commcell:
            return self._commcell.service_commcells[self._filter_commcell].commcell_id
        return None

    def __repr__(self) -> str:
        """String representation of the instance of this class."""
        if not self._filter_commcell:
            return f'service commcell associations from router: {self._commcell.webconsole_hostname}'
        else:
            return (f'associations of service commcell: {self._filter_commcell} '
                    f'from router: {self._commcell.webconsole_hostname}')

    def refresh(self, ent_type: str = None) -> None:
        """
        Refreshes the cached associations information.

        Usage:
            associations.refresh()
        """
        self._associations = None
        if ent_type == 'Organization':
            self._company_associations = None
        elif ent_type == 'Security':
            self._security_associations = None
        else:
            self._company_associations = None
            self._security_associations = None

    def _assoc_endpoint(self, method: str, ent_type: str) -> str:
        """
        Returns the endpoint for service commcell associations based on the method and entity type.

        Args:
            method (str): HTTP method to use for the API call (e.g., 'GET', 'POST').
            ent_type (str): Entity type string.
        Returns:
            str: The endpoint for the API call.
        """
        url = self._commcell._services['SERVICE_COMMCELL_ASSOC']
        if method == 'POST':
            if ent_type == 'Organization':
                url = self._commcell._services['SERVICE_COMMCELL_COMP']
            elif ent_type == 'Security':
                url = self._commcell._services['SERVICE_COMMCELL_SEC']
        elif method == 'GET':
            url += '?'
            if ent_type == 'Organization':
                url += 'includeSecurities=false'
            elif ent_type == 'Security':
                url += 'includeCompanies=false'
            if self._sc_id:
                url += f'&commcellId={self._sc_id}'
        return url

    def _associations_api_call(
            self, method: str, exc_code: int, ent_type: str, payload: dict = None, **kwargs) -> dict:
        """
        Makes an API call to the Commcell for service commcell associations.

        Args:
            method (str): HTTP method to use for the API call (e.g., 'GET', 'POST').
            exc_code (int): Error code to raise in case of an exception.
            ent_type (str): Entity type string. "Organization" or "Security" or None
            payload (dict): Payload to send with the API call.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: JSON response from the API call.

        Raises:
            SDKException: If the API call returns a warning and include_warning is True.

        Usage:
            response = self._associations_api_call('GET', 109)
            response = self._associations_api_call('POST', 110, payload={'key': 'value'}, include_warning=True)
        """
        if method == 'POST':
            if payload and self._sc_id:
                payload['serviceCommcellId'] = self._sc_id

        response_json = self._commcell.wrap_request(
            method, self._assoc_endpoint(method, ent_type),
            req_kwargs={'payload': payload} if payload else {},
            sdk_exception=('ServiceCommcells', exc_code)
        )
        if kwargs.get('include_warning'):
            warning_code = response_json.get('warningCode', 0)
            if warning_code != 0:
                error_string = response_json.get('warningMessage')
                raise SDKException('ServiceCommcells', exc_code, error_string)
        return response_json

    def _form_assoc_dict(self, entity: Any, commcell: str) -> dict:
        """
        prepares the entity json for adding commcell associations.

        Args:
            entity (Any): object of User, UserGroup, Domain or Organization class
            commcell (str): commserv name of the service commcell

        Returns:
            dict: entity json for adding commcell associations

        Raises:
            SDKException: if commcell is not a string.

        Usage:
            assoc_dict = self._form_assoc_dict(entity, 'commserve1')
        """
        if not isinstance(commcell, str):
            raise SDKException('ServiceCommcells', '101', 'commcell must be a string')
        return {
            "entity": {
                "entityType": 194,
                "entityName": self._commcell.service_commcells[commcell].client_name,
                "_type_": 150,
                "entityId": self._commcell.service_commcells[commcell].commcell_id,
                # todo: "workloadRegionDisplayName": "..."
            },
            **self.lookup_entity_payload(entity)
        }

    def _form_assoc_list(self, entities: Any, commcells: Any) -> tuple[list[dict], str]:
        """
        prepares the entity json for adding commcell associations.

        Args:
            entities (Any): object(s) of User, UserGroup, Domain or Organization class
            commcells (Any): commserv name(s) of the service commcell(s)

        Returns:
            list[dict]: entity json for adding commcell associations
            str: entity type string

        Usage:
            assoc_list = self._form_assoc_list(entity, 'commserve1')
            assoc_list = self._form_assoc_list([entity1, entity2], ['commserve1', 'commserve2'])
        """
        if not isinstance(entities, list):
            entities = [entities]
        if not isinstance(commcells, list):
            commcells = [commcells]
        return [
            self._form_assoc_dict(entity, commcell) for entity in entities for commcell in commcells
        ], Associations.lookup_entities_type(entities)

    def get(self, entity: Any, commcell: str = None, ent_type: str = None) -> list[dict]:
        """
        Gets an entity's association details for every commcell it is associated to.

        Args:
            entity (Any): can be object of User,UserGroup,Domain and Organization Class
                                         or a string of the entity name
                                         or a list of the above

            commcell (str, optional): commserv name(s) of the service commcell(s) to filter associations. Defaults to None.

            ent_type (str, optional): entity type string 'Organization' or 'Security'. Defaults to None.

        Returns:
            list[dict]: list of dicts, each dict containing details of the entity's association with a service commcell

            Example:
                [
                    {
                        "userOrGroup": {
                            "userId": ,
                            "GUID": ,
                            "userName": ,
                            "_type_": ,
                        },
                        "entity": {
                            "entityType": ,
                            "entityName": ,
                            "entityId": ,
                            "_type_": ,
                            "flags": ,
                        },
                        "properties": ,
                    },
                    {
                        "userOrGroup": {...},
                        "entity": {...},
                        "properties": {...},
                    },
                    {
                        "userOrGroup": {...},
                        "entity": {...},
                        "properties": {...},
                    }
                ]

        """
        # commcell filter logic
        commcell = commcell or self._filter_commcell
        if isinstance(commcell, str):
            commcell = [commcell]

        # recurse logic
        if isinstance(entity, list):
            return [
                assoc for each_entity in entity for assoc in self.get(each_entity)
            ]

        # match logic
        if isinstance(entity, str):
            assoc_match = lambda assoc_dict: entity.lower() in [
                assoc_dict['userOrGroup'].get('userName', '').lower(),
                assoc_dict['userOrGroup'].get('userGroupName', '').lower(),
                assoc_dict['userOrGroup'].get('providerDomainName', '').lower()
            ]
        else:
            ent_type = ent_type or Associations.lookup_entity_type(entity)
            catch_assoc_dict = self.lookup_entity_payload(entity)
            assoc_match = lambda assoc_dict: all(
                assoc_dict.get('userOrGroup', {}).get(k) == v
                for k, v in catch_assoc_dict.get('userOrGroup', {}).items()
            )

        # fetch logic
        assocs_set = (
            self.all_company_associations if ent_type == 'Organization' else
            self.all_security_associations if ent_type == 'Security' else
            self.all_associations
        )
        entity_assocs = [
            assoc for assoc in assocs_set if assoc_match(assoc)
        ]
        if commcell:
            entity_assocs = [
                assoc for assoc in entity_assocs if assoc['entity']['entityName'] in commcell
            ]
        return entity_assocs

    def add(self, entity: Any, commcell: str = None, **kwargs) -> None:
        """
        Adds an association for the given entity to the specified service commcell.

        Args:
            entity (Any): object(s) of User, UserGroup, Domain or Organization class
            commcell (str, optional): commserv name of the service commcell(s). Defaults to None.
            **kwargs:
                include_warning (bool): if True, will raise exception for warning messages as well

        Raises:
            SDKException:
                if the entity is not valid
                if the response is empty
                if the response is not success

        Usage:
            associations.add(user_object, commcell='commserve1')
            associations.add([user_object1, user_object2], commcell=['commserve1', 'commserve2'], include_warning=True)
        """
        commcell = commcell or self._filter_commcell
        assoc_list, ent_type = self._form_assoc_list(entity, commcell)
        self._associations_api_call(
            'POST', 110,
            ent_type,
            {
                "associations": assoc_list,
                "associationsOperationType": 2
            },
            **kwargs
        )
        self.refresh(ent_type)

    def delete(self, entity: Any, commcell: str = None, ent_type: str = None, **kwargs) -> None:
        """
        Deletes an association for the given entity from the specified service commcell(s).

        Args:
            entity (Any): object(s) of User, UserGroup, Domain or Organization class
            commcell (str, optional): commserv name of the service commcell(s). Defaults to None.
            ent_type (str, optional): entity type string 'Organization' or 'Security'. Defaults to None.
            **kwargs:
                include_warning (bool): if True, will raise exception for warning messages as well

        Usage:
            associations.delete(user_object, commcell='commserve1')
            associations.delete([user_object1, user_object2], commcell=['commserve1', 'commserve2'], include_warning=True)
        """
        commcell = commcell or self._filter_commcell
        if assocs_to_delete := self.get(entity, commcell, ent_type):
            if not ent_type:
                ent_type = Associations.reverse_lookup_type(assocs_to_delete)
            self._associations_api_call(
                'POST', 111,
                ent_type,
                {
                    "associations": assocs_to_delete,
                    "associationsOperationType": 3
                },
                **kwargs
            )
            self.refresh(ent_type)

    @property
    def all_company_associations(self) -> list[dict]:
        """
        Returns all company associations of service commcells.

        Returns:
            list[dict]: consisting of all companies associated with service commcells

        Usage:
            all_company_assocs = associations.all_company_associations
        """
        if self._company_associations is None:
            self._company_associations = self._associations_api_call('GET', 109, 'Organization').get('associations', [])
        return self._company_associations

    @property
    def all_security_associations(self) -> list[dict]:
        """
        Returns all security associations of service commcells.

        Returns:
            list[dict]: consisting of all security entities associated with service commcells

        Usage:
            all_security_assocs = associations.all_security_associations
        """
        if self._security_associations is None:
            self._security_associations = self._associations_api_call('GET', 109, 'Security').get('associations', [])
        return self._security_associations

    @property
    def all_associations(self) -> list[dict]:
        """
        Returns all associations of service commcells.

        Returns:
            list[dict]: consisting of all entities associated with service commcells

        Usage:
            all_assocs = associations.all_associations
        """
        return self.all_company_associations + self.all_security_associations
