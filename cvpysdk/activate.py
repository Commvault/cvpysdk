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

from .exception import SDKException

from .activateapps.file_storage_optimization import FsoTypes, FsoServers, FsoServerGroups

from .activateapps.sensitive_data_governance import Projects

from .activateapps.inventory_manager import Inventories

from .activateapps.request_manager import Requests

from .activateapps.entity_manager import EntityManagerTypes, ActivateEntities, Tags, Classifiers

from .activateapps.compliance_utils import ComplianceSearchUtils


class Activate(object):
    """Class for representing activate apps in the commcell."""

    def __init__(self, commcell_object):
        """Initializes an instance of the Activate class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

            Returns:
                object  -   instance of the Activate class

        """
        self._commcell_object = commcell_object
        self._entity = None
        self._tags = None
        self._classifiers = None
        self._inventories = None
        self._fso_servers = None
        self._fso_server_groups = None
        self._sdg_projects = None
        self._req_mgr = None
        self._compliance_search = None

    def __del__(self):
        """Destructor method to delete all instances of apps referenced by this class"""
        del self._entity
        del self._tags
        del self._classifiers
        del self._inventories
        del self._fso_servers
        del self._fso_server_groups
        del self._sdg_projects
        del self._req_mgr

    def compliance_search(self):
        """Returns the Compliance Search utility class object from activate apps"""
        if self._compliance_search is None:
            self._compliance_search = ComplianceSearchUtils(self._commcell_object)
        return self._compliance_search

    def inventory_manager(self):
        """Returns the Inventories class object from inventory manager app from activate apps"""
        if self._inventories is None:
            self._inventories = Inventories(self._commcell_object)
        return self._inventories

    def request_manager(self):
        """Returns the Requests class object from request manager app from activate apps"""
        if self._req_mgr is None:
            self._req_mgr = Requests(self._commcell_object)
        return self._req_mgr

    def file_storage_optimization(self, fso_type=FsoTypes.SERVERS):
        """returns object of FsoServers/FsoServerGroups/Projects based on FSO type

                Args:

                    fso_type        (enum)      --  FsoTypes enum (Default : FsoServers)

                Returns:

                    obj --  Instance of FsoServers/FsoServerGroups/Projects based on type

                Raises:

                SDKException:

                        if input data is not valid

                        if entity type is not supported

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

    def sensitive_data_governance(self):
        """returns object of Sensitive data governance - Projects class

                Args:

                    None

                Returns:

                    obj --  Instance of Projects class from sensitive data governance

                Raises:

                    None

        """
        if self._sdg_projects is None:
            self._sdg_projects = Projects(self._commcell_object)
        return self._sdg_projects

    def entity_manager(self, entity_type=EntityManagerTypes.ENTITIES):
        """Returns the ActivateEntities or Classifiers or Tagsets object in entity manager based on input type

            Args:

                entity_type     (enum)      --  EntityManagerTypes enum

                                            Default : ENTITIES

            Returns:

                object      --  Instance of ActivateEntities or Classifiers or Tags class based on entity_type

            Raises:

                SDKException:

                        if input data is not valid

                        if entity type is not supported

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
        raise SDKException('EntityManager', '102', 'Unsupported entity type specified')
