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

    **entity_manager**           --  returns object of entity_manager class based on entity type specified

"""
from .exception import SDKException

from .activateapps.entity_manager import EntityManagerTypes, ActivateEntities


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

    def __del__(self):
        """Destructor method to delete all instances of apps referenced by this class"""
        del self._entity

    def entity_manager(self, entity_type=EntityManagerTypes.ENTITIES):
        """Returns the ActivateEntities or Classifiers or Tagsets object in entity manager based on input type

            Args:

                entity_type     (enum)      --  EntityManagerTypes enum

                                            Default : ENTITIES

            Returns:

                object      --  Instance of ActivateEntities or Classifiers or Tagsets class based on entity_type

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
        raise SDKException('EntityManager', '102', 'Unsupported entity type specified')
