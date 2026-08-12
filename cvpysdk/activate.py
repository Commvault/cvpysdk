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

"""Main file for performing operations on Activate apps.

Activate : Base class for all activate apps

        __init__()                  --  initialize instance of the Activate class

        __del__()                   --  destructor class for deleting referenced apps instances


Activate instance Attributes
============================

    **entity_manager**              --  returns object of entity_manager class based on entity type specified

    **inventory_manager**           --  returns object of Inventories class

    **file_storage_optimization**   --  returns object of file_storage_optimization based on FSO type

    **sensitive_data_governance**   --  returns object of sensitive data governance app

    **request_manager**             --  returns object of Requests class

"""

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .commcell import Commcell

from .exception import SDKException

from .activateapps.file_storage_optimization import FsoTypes, FsoServers, FsoServerGroups

from .activateapps.sensitive_data_governance import Projects

from .activateapps.inventory_manager import Inventories

from .activateapps.request_manager import Requests

from .activateapps.entity_manager import EntityManagerTypes, ActivateEntities, Tags, Classifiers, YaraRules, HashFeeds

from .activateapps.compliance_utils import ComplianceSearchUtils

class Activate(object):
    """
    Class for managing and interacting with Activate apps within the Commcell environment.

    The Activate class provides a unified interface to access and control various Activate applications
    in the Commcell, enabling users to perform compliance searches, manage inventory, handle requests,
    optimize file storage, govern sensitive data, and manage entities. It is designed to facilitate
    seamless integration and operation of Activate functionalities for data governance and management.

    Key Features:
        - Initialize with a Commcell object for context-aware operations
        - Perform compliance searches across data sources
        - Access and manage inventory using the inventory manager
        - Handle requests through the request manager
        - Optimize file storage with support for different FSO types
        - Govern sensitive data for regulatory and security compliance
        - Manage entities with support for various entity types

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize an instance of the Activate class with a Commcell connection.

        Args:
            commcell_object: Instance of the Commcell class used for Activate operations.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> activate = Activate(commcell)
            >>> # The Activate object is now initialized and ready for use

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._entity = None
        self._tags = None
        self._classifiers = None
        self._yara_rules = None
        self._hash_feeds = None
        self._inventories = None
        self._fso_servers = None
        self._fso_server_groups = None
        self._sdg_projects = None
        self._req_mgr = None
        self._compliance_search = None

    def __del__(self) -> None:
        """Destructor method to clean up resources associated with the Activate instance.

        This method deletes all internal references to app-related entities, tags, classifiers, inventories,
        FSO servers, FSO server groups, SDG projects, and request managers to help with resource cleanup
        when the object is destroyed.

        Example:
            >>> activate = Activate(...)
            >>> del activate  # Triggers resource cleanup for all referenced apps

        #ai-gen-doc
        """
        del self._entity
        del self._tags
        del self._classifiers
        del self._yara_rules
        del self._hash_feeds
        del self._inventories
        del self._fso_servers
        del self._fso_server_groups
        del self._sdg_projects
        del self._req_mgr

    def compliance_search(self) -> 'ComplianceSearchUtils':
        """Get the ComplianceSearchUtils instance for compliance search operations in Activate apps.

        Returns:
            ComplianceSearchUtils: An instance for performing compliance searches.

        Example:
            >>> activate = Activate(commcell_object)
            >>> compliance_utils = activate.compliance_search()
            >>> print(f"Compliance search utility: {compliance_utils}")
            >>> # Use the returned ComplianceSearchUtils object for compliance-related tasks

        #ai-gen-doc
        """
        if self._compliance_search is None:
            self._compliance_search = ComplianceSearchUtils(self._commcell_object)
        return self._compliance_search

    def inventory_manager(self) -> 'Inventories':
        """Get the Inventories instance from the inventory manager app in Activate.

        Returns:
            Inventories: An instance for managing inventory data within the Activate application.

        Example:
            >>> activate = Activate(commcell_object)
            >>> inventories = activate.inventory_manager  # Use dot notation for property access
            >>> print(f"Inventories object: {inventories}")
            >>> # The returned Inventories object can be used for inventory operations

        #ai-gen-doc
        """
        if self._inventories is None:
            self._inventories = Inventories(self._commcell_object)
        return self._inventories

    def request_manager(self) -> 'Requests':
        """Get the Requests object from the request manager app in Activate.

        Returns:
            Requests: An instance of the Requests class for managing requests within the Activate apps.

        Example:
            >>> activate = Activate(commcell_object)
            >>> requests = activate.request_manager
            >>> print(f"Requests object: {requests}")
            >>> # The returned Requests object can be used to interact with request manager features

        #ai-gen-doc
        """
        if self._req_mgr is None:
            self._req_mgr = Requests(self._commcell_object)
        return self._req_mgr

    def file_storage_optimization(self, fso_type: 'FsoTypes' = FsoTypes.SERVERS):
        """Retrieve the file storage optimization object based on the specified FSO type.

        Depending on the provided FsoTypes enum value, this method returns an instance of
        FsoServers or FsoServerGroups. If the type is unsupported or invalid, an SDKException is raised.

        Args:
            fso_type: FsoTypes enum value specifying the type of file storage optimization object to retrieve.
                      Default is FsoTypes.SERVERS.

        Returns:
            Instance of FsoServers or FsoServerGroups corresponding to the specified FSO type.

        Raises:
            SDKException: If the input data is not valid or the entity type is not supported.

        Example:
            >>> activate = Activate(commcell_object)
            >>> # Retrieve FsoServers object
            >>> fso_servers = activate.file_storage_optimization(FsoTypes.SERVERS)
            >>> print(f"FSO Servers object: {fso_servers}")
            >>>
            >>> # Retrieve FsoServerGroups object
            >>> fso_server_groups = activate.file_storage_optimization(FsoTypes.SERVER_GROUPS)
            >>> print(f"FSO Server Groups object: {fso_server_groups}")

        #ai-gen-doc
        """
        if not isinstance(fso_type, FsoTypes):
            raise SDKException('FileStorageOptimization', '101')
        if fso_type.value == FsoTypes.SERVERS.value:
            if self._fso_servers is None:
                self._fso_servers = FsoServers(self._commcell_object)
            return self._fso_servers
        elif fso_type.value == FsoTypes.SERVER_GROUPS.value:
            if self._fso_server_groups is None:
                self._fso_server_groups = FsoServerGroups(self._commcell_object)
            return self._fso_server_groups
        raise SDKException('FileStorageOptimization', '102', 'Unsupported FSO type specified')

    def sensitive_data_governance(self) -> 'Projects':
        """Get the Projects instance for Sensitive Data Governance.

        Returns:
            Projects: An instance of the Projects class from Sensitive Data Governance.

        Example:
            >>> activate = Activate(commcell_object)
            >>> sdg_projects = activate.sensitive_data_governance
            >>> print(f"Sensitive Data Governance Projects: {sdg_projects}")
            >>> # The returned Projects object can be used for project management tasks

        #ai-gen-doc
        """
        if self._sdg_projects is None:
            self._sdg_projects = Projects(self._commcell_object)
        return self._sdg_projects

    def entity_manager(self, entity_type: 'EntityManagerTypes' = EntityManagerTypes.ENTITIES) -> object:
        """Retrieve the appropriate entity manager object based on the specified entity type.

        Depending on the provided entity_type, this method returns an instance of ActivateEntities,
        Classifiers, Tags, YaraRules, or HashFeeds for managing entities, classifiers, tagsets, YARA rules,
        or hash feeds within Activate.

        Args:
            entity_type: An EntityManagerTypes enum value specifying which entity manager to retrieve.
                - EntityManagerTypes.ENTITIES: Returns ActivateEntities instance.
                - EntityManagerTypes.TAGS: Returns Tags instance.
                - EntityManagerTypes.CLASSIFIERS: Returns Classifiers instance.
                - EntityManagerTypes.YARA_RULES: Returns YaraRules instance.
                - EntityManagerTypes.HASH_FEEDS: Returns HashFeeds instance.
                Default is EntityManagerTypes.ENTITIES.

        Returns:
            An instance of ActivateEntities, Classifiers, Tags, YaraRules, or HashFeeds corresponding to the entity_type.

        Raises:
            SDKException: If the input data is not valid or the entity type is not supported.

        Example:
            >>> activate = Activate(commcell_object)
            >>> entities = activate.entity_manager(EntityManagerTypes.ENTITIES)
            >>> print(f"Entities manager: {entities}")
            >>> tags = activate.entity_manager(EntityManagerTypes.TAGS)
            >>> print(f"Tags manager: {tags}")
            >>> classifiers = activate.entity_manager(EntityManagerTypes.CLASSIFIERS)
            >>> print(f"Classifiers manager: {classifiers}")
            >>> yara_rules = activate.entity_manager(EntityManagerTypes.YARA_RULES)
            >>> print(f"YARA Rules manager: {yara_rules}")
            >>> hash_feeds = activate.entity_manager(EntityManagerTypes.HASH_FEEDS)
            >>> print(f"Hash Feeds manager: {hash_feeds}")

        #ai-gen-doc
        """
        if not isinstance(entity_type, EntityManagerTypes):
            raise SDKException('EntityManager', '101')
        if entity_type.value == EntityManagerTypes.ENTITIES.value:
            if self._entity is None:
                self._entity = ActivateEntities(self._commcell_object)
            return self._entity
        elif entity_type.value == EntityManagerTypes.TAGS.value:
            if self._tags is None:
                self._tags = Tags(self._commcell_object)
            return self._tags
        elif entity_type.value == EntityManagerTypes.CLASSIFIERS.value:
            if self._classifiers is None:
                self._classifiers = Classifiers(self._commcell_object)
            return self._classifiers
        elif entity_type.value == EntityManagerTypes.YARA_RULES.value:            
            if self._yara_rules is None:
                self._yara_rules = YaraRules(self._commcell_object)
            return self._yara_rules
        elif entity_type.value == EntityManagerTypes.HASH_FEEDS.value:            
            if self._hash_feeds is None:
                self._hash_feeds = HashFeeds(self._commcell_object)
            return self._hash_feeds
        raise SDKException('EntityManager', '102', 'Unsupported entity type specified')
