#!/usr/bin/env python
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

"""File for operating on a SAP Oracle iDa Subclient

SAPOracleSubclient is the only class defined in this file.

SAPOracleSubclient: Derived class from Subclient Base class, representing a SAPOracle subclient,
                        and to perform operations on that subclient

SAPOracleSubclient:
    __init__                             --   Constructor for the class

    data_sp()                           --  Getter for getting data storage policy

    _get_subclient_properties()         --  gets the subclient related properties of
                                             SAP Oracle subclient.

    _get_subclient_properties_json()    --  gets the subclient related properties
                                            of SAP Oracle  subclient.


"""
from __future__ import unicode_literals

from ..subclient import Subclient
from past.builtins import basestring
from ..exception import SDKException



class SAPOracleSubclient(Subclient):
    """Derived class from Subclient Base class, representing a SAP oracle iDa subclient,
        and to perform operations on that subclient."""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """
        Constructor for the class
        Args:
            backupset_object  (object)  -- instance of the Backupset class
            subclient_name    (str)     -- name of the subclient
            subclient_id      (str)     -- id of the subclient
        """
        super(SAPOracleSubclient, self).__init__(backupset_object, subclient_name, subclient_id)
        self._subclientprop = {}    # variable to hold subclient properties to be changed

    @property
    def data_sp(self):
        """
        Getter for data storage policy
        Returns:
            string - string representing data storage policy
        """
        return self._commonProperties['storageDevice']\
            ['dataBackupStoragePolicy']['storagePolicyName']

    @property
    def sapBackupMode(self):
        """
        Getter for sap backup mode
        Returns:
            string - string representing sapBackupMode
            sapBackupMode--0 means Online Db
        """
        return self._sapForOracleSubclientProp['sapBackupMode']

    @property
    def sapBackupDevice(self):
        """
        Getter for sapBackupDevice
        Returns:
            string - string representing sapBackupDevice
            sapBackupDevice--1 means util_file device
        """
        return self._sapForOracleSubclientProp['sapBackupDevice']

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of SAP Oracle subclient.

        """
        #subclient_options={}
        #saporaclesubclient_options={}
        
        if not bool(self._subclient_properties):
            super(SAPOracleSubclient, self)._get_subclient_properties()

        if 'sapForOracleSubclientProp' in self._subclient_properties:
            self._sapForOracleSubclientProp = self._subclient_properties\
                    ['sapForOracleSubclientProp']
        self._sapForOracleSubclientProp["sapSelectiveOnlineFull"]=False
        self._sapForOracleSubclientProp["sapData"]=True
        self._sapForOracleSubclientProp["sapBackupArchiveLog"]=True
        self._sapForOracleSubclientProp["sapArchiveDelete"]=True
        

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.
           Returns:
                dict - all subclient properties put inside a dict
        """
        subclient_json = {
            "subClientProperties":
                {
                    "subClientEntity": self._subClientEntity,
                    "commonProperties": self._commonProperties,
                    "sapForOracleSubclientProp":self._sapForOracleSubclientProp
                }
        }
        #print (subclient_json)
        return subclient_json
    
    def _update_subclient_properties(self):
        """Gets the subclient  related properties of SAP Oracle subclient.

        """

        if not bool(self._subclient_properties):
            super(SAPOracleSubclient, self)._get_subclient_properties()

        if 'sapForOracleSubclientProp' in self._subclient_properties:
            self._sapForOracleSubclientProp = self._subclient_properties\
                    ['sapForOracleSubclientProp']
