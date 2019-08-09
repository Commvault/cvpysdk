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

"""File for operating on a Informix Subclient

InformixSubclient is the only class defined in this file.

InformixSubclient: Derived class from Subclient Base class, representing a Informix subclient,
                        and to perform operations on that subclient

InformixSubclient:

    _get_subclient_properties()         --  gets the subclient related properties of
    Informix subclient

    _get_subclient_properties_json()    --  gets all the subclient related properties of
    Informix subclient

    restore_in_place()                  --  restores the Informix data/log files specified
    in the input db_space list to the same location

InformixSubclient instance Attributes
==================================

    **backup_mode**                     --  returns the `backup_mode` of Informix subclient

"""

from __future__ import unicode_literals

from ..subclient import Subclient


class InformixSubclient(Subclient):
    """Derived class from Subclient Base class, representing a Informix subclient,
        and to perform operations on that subclient.
    """

    def _get_subclient_properties(self):
        """Gets the subclient related properties of Informix subclient.
        """
        super(InformixSubclient, self)._get_subclient_properties()
        if 'informixSubclientProp' not in self._subclient_properties:
            self._subclient_properties['informixSubclientProp'] = {}
        self._informix_subclient_prop = self._subclient_properties['informixSubclientProp']

    def _get_subclient_properties_json(self):
        """ Gets all the subclient related properties of Informix subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties":
                {
                    "informixSubclientProp": self._informix_subclient_prop,
                    "subClientEntity": self._subClientEntity
                }
        }
        return subclient_json

    def restore_in_place(
            self,
            path,
            restore_type="ENTIRE INSTANCE",
            copy_precedence=None,
            physical_restore=True,
            logical_restore=True):
        """Restores the Informix data/log files specified in the input db_space\
            list to the same location.

            Args:

                path               (list)  -- List of dbspaces to be restored

                restore_type       (str)   --  Restore type for informix instance
                                                Accepted Values:
                                                    ENTIRE INSTANCE/WHOLE SYSTEM

                copy_precedence    (str)   --  Copy precedence associted with storage
                policy

                physical_restore   (bool)  --  Physical restore flag

                logical_restore    (bool)  --  Logical restore flag

            Returns:
                object - instance of the Job class for this restore job
        """
        self._backupset_object._instance_object._restore_association = self._subClientEntity
        return self._backupset_object._instance_object.restore_in_place(
            path,
            restore_type,
            copy_precedence,
            physical_restore,
            logical_restore
        )

    @property
    def backup_mode(self):
        """ Returns the `backup_mode` of Informix subclient """
        return self._informix_subclient_prop.get('backupMode', "")

    @backup_mode.setter
    def backup_mode(self, backup_mode):
        """ Setter for informix subclient backup_mode

            Args:

                backup_mode (str)  -- backup mode of the subclient

                    Acceptable Values:

                            Entire_instance/Whole_System
        """
        content = {'backupMode': backup_mode}
        self._set_subclient_properties("_informix_subclient_prop", content)
