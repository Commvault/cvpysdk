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
Main file for performing additional setting operations

AdditionalSettings is the only class defined in this file.

AdditionalSettings: Class for managing Additional Settings on various entities within the commcell.

AdditionalSettings:
    __init__                    --  initialise the AdditionalSettings class instance

    add_additional_setting      --  Adds an additional setting

    edit_additional_setting     --  Edits an additional setting

    delete_additional_setting   --  Deletes an additional setting

    get_additional_settings     --  Returns all the additional settings for the entity

    additional_settings         --  Cached property to access all additional settings

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING

from .exception import SDKException

if TYPE_CHECKING:
    from .client import Client
    from .clientgroup import ClientGroup
    from .organization import Organization
    from .security.user import User
    from .security.usergroup import UserGroup
    from .commcell import Commcell
    from .subclient import Subclient


class AdditionalSettings(object):
    """Class for performing activity control operations.

    Description:
        This class is used to manage additional settings for various entities within the Commcell.
        It provides methods to add, edit, delete, and retrieve additional settings.

    Attributes:
        entity_type_ids_map (dict): A dictionary mapping entity types to their corresponding IDs.
        entity_id_prop (dict): A dictionary mapping entity types to the property name that holds their ID.
        _entity_object (object): The entity object for which additional settings are managed.
        _entity_type_id (int): The ID of the entity type.
        _entity_id (int): The ID of the entity.
        _additional_settings (dict): A dictionary to cache the additional settings.
        _commcell_object (Commcell): The Commcell object associated with the entity.

    Usage:
        >>> from pycommcell import Commcell
        >>> commcell = Commcell('hostname', 'username', 'password')
        >>> client = commcell.getClient('client_name')
        >>> additional_settings = AdditionalSettings(client)
    """
    entity_type_ids_map: Dict[str, int] = {
        'Client': 3,
        'Subclient': 7,
        'ClientGroup': 28,
        'Organization': 189,
        'User': 13,
        'UserGroup': 15,
    }
    entity_id_prop: Dict[str, str] = {
        'Client': 'client_id',
        'Subclient': 'subclient_id',
        'ClientGroup': 'clientgroup_id',
        'Organization': 'organization_id',
        'User': 'user_id',
        'UserGroup': 'user_group_id',
    }

    @staticmethod
    def lookup_entity_type(entity: Any) -> Optional[str]:
        """
        Looks up the entity type based on the entity object's class hierarchy.

        Args:
            entity (Any): The entity object to look up the type for.

        Returns:
            Optional[str]: The name of the entity type if found, otherwise None.

        Usage:
            >>> entity_type = AdditionalSettings.lookup_entity_type(client_object)
        """
        for cls in type(entity).__mro__:
            name = cls.__name__
            if name in AdditionalSettings.entity_id_prop:
                return name
        return None

    def __init__(self, entity_object: Any) -> None:
        """Initialise the Activity control class instance.

        Args:
            entity_object (Any): instance of the entity object

        Raises:
            SDKException: if the entity type is not supported.

        Usage:
            >>> additional_settings = AdditionalSettings(client_object)
        """

        self._entity_object: Any = entity_object
        entity_class: Optional[str] = self.lookup_entity_type(entity_object)
        if not entity_class:
            raise SDKException('AdditionalSettings', '101',
                               f'Unsupported entity of type: {type(entity_object)}')

        self._entity_type_id: int = self.entity_type_ids_map[entity_class]
        self._entity_id: int = getattr(self._entity_object, self.entity_id_prop.get(entity_class))

        self._additional_settings: Dict = {}

        self._commcell_object: 'Commcell' = self._entity_object._commcell_object

    def __repr__(self) -> str:
        """String representation of the instance of this class.

        Returns:
            str: String representation of the AdditionalSettings instance.

        Usage:
            >>> str(additional_settings)
        """
        return f'AdditionalSettings class instance for entity: {self._entity_object}'

    def _v4_workload_settings_api_caller(self, request_type: str, other_props: Optional[Dict] = None):
        """
        A helper function to call the workload settings API.

        Args:
            request_type (str): The type of request to make (e.g., 'POST', 'PUT').
            other_props (Optional[Dict]): Additional properties to include in the request payload. Defaults to None.

        Returns:
            callable: A function that takes key_name, category, data_type, value, comment, and enabled as arguments
                      and makes the API call.

        Raises:
            SDKException: If the API call fails.

        Usage:
            >>> api_caller = self._v4_workload_settings_api_caller('POST')
            >>> api_caller('key_name', 'category', 'STRING', 'value', 'comment', True)
        """
        other_props = other_props or {}

        def api_caller(key_name: str, category: str, data_type: str, value: str, comment: str, enabled: bool):
            properties_dict: Dict[str, Any] = {
                "additionalSettings": [
                    {
                        "entityInfo": {
                            "entityId": int(self._entity_id),
                            "entityType": self._entity_type_id,
                            "_type_": self._entity_type_id
                        },
                        "registryKeys": [
                            {
                                "relativepath": category,
                                "keyName": key_name,
                                "type": data_type,
                                "value": value,
                                "enabled": int(enabled),
                                "comment": comment
                            } | other_props
                        ]
                    }
                ]
            }
            self._commcell_object.wrap_request(
                request_type, 'SET_ADDITIONAL_SETTINGS',
                req_kwargs={'payload': properties_dict},
                sdk_exception=('AdditionalSettings', '102')
            )
            self.refresh()
        return api_caller

    def add_additional_setting(
            self, key_name: str, category: str, data_type: str, value: str, comment: str = "Added using automation", enabled: bool = True
    ) -> None:
        """
        Adds additional settings on entity

        Args:
            key_name (str):          Name of the key to be added
            category (str):          Category under which the key should be added
            data_type (str):         Data type of the additional setting ('BOOLEAN', 'INTEGER', 'STRING', etc.)
            value (str):             Value to be set for the key
            comment (str):           Comment for the key. Defaults to "Added using automation".
            enabled (bool):          Whether the setting is enabled. Defaults to True.

        Usage:
            >>> additional_settings.add_additional_setting('key_name', 'category', 'STRING', 'value')
            >>> additional_settings.add_additional_setting('key_name', 'category', 'INTEGER', '123', comment='custom comment', enabled=False)
        """
        self._v4_workload_settings_api_caller('POST')(key_name, category, data_type, value, comment, enabled)

    def edit_additional_setting(self, key_name: str, value: Optional[str] = None, comment: Optional[str] = None, enabled: Optional[bool] = None) -> None:
        """
        Edits an additional setting for the entity

        Args:
            key_name (str):    Name of the key to be edited
            value (str):      New value for the key
            comment (str):    New comment for the key
            enabled (bool):   Whether the setting is enabled. Defaults to None.

        Raises:
            SDKException: if the key does not exist on the entity.

        Usage:
            >>> additional_settings.edit_additional_setting('key_name', value='new_value')
            >>> additional_settings.edit_additional_setting('key_name', comment='new comment', enabled=True)
        """
        key_details: Optional[Tuple[str, str, str, str, str, bool]] = self.all_additional_settings.get(key_name)
        if not key_details:
            raise SDKException('AdditionalSettings', '102',
                               f'Key {key_name} does not exist on entity: {self._entity_object}')
        category: str = key_details[1]
        data_type: str = key_details[2]
        value: str = value or key_details[3]
        comment: str = comment or key_details[4]
        enabled: bool = enabled if enabled is not None else key_details[5]
        self._v4_workload_settings_api_caller('PUT')(key_name, category, data_type, value, comment, enabled)

    def delete_additional_setting(self, key_name: str) -> None:
        """
        Deletes an additional setting from the entity

        Args:
            key_name (str):  Name of the key to be deleted

        Usage:
            >>> additional_settings.delete_additional_setting('key_name')
        """
        key_details: Optional[Tuple[str, str, str, str, str, bool]] = self.all_additional_settings.get(key_name)
        if not key_details:
            return
        self._v4_workload_settings_api_caller('PUT', {'deleted': 1})(*key_details)

    def get_additional_settings(self) -> Dict[str, Tuple[str, str, str, str, str, bool]]:
        """
        Returns all the additional settings for the entity

        Returns:
            Dict[str, Tuple[str, str, str, str, str, bool]]: A dictionary containing additional settings.
                The keys are the names of the settings, and the values are tuples containing:
                (name, category, type, value, comment, enabled).

        Usage:
            >>> settings = additional_settings.get_additional_settings()
        """
        response_json: Dict = self._commcell_object.wrap_request(
            'GET', 'GET_ADDITIONAL_SETTINGS', (self._entity_type_id, self._entity_id)
        )
        return {
            setting['name']: (
                setting['name'],
                setting['category'],
                setting['type'],
                setting.get('values', [{}])[0].get('value', ''),
                setting.get('comment', ''),
                bool(setting.get('enabled', True))
            )
            for setting in response_json.get('additionalSettings', [])
        }

    @property
    def all_additional_settings(self) -> Dict[str, Tuple[str, str, str, str, str, bool]]:
        """
        Returns the additional settings for the entity

        Returns:
            Dict[str, Tuple[str, str, str, str, str, bool]]: A dictionary containing additional settings.
                The keys are the names of the settings, and the values are tuples containing:
                (name, category, type, value, comment, enabled).

        Usage:
            >>> all_settings = additional_settings.all_additional_settings
        """
        if not self._additional_settings:
            self._additional_settings: Dict[str, Tuple[str, str, str, str, str, bool]] = self.get_additional_settings()
        return self._additional_settings

    def refresh(self) -> None:
        """Refreshes the additional settings for the entity.

        Usage:
            >>> additional_settings.refresh()
        """
        self._additional_settings: Dict[str, Tuple[str, str, str, str, str, bool]] = {}
