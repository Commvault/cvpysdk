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
"""File for operating on an AD agent Backupset.

adbackupset is the only class defined in this file.

Class:

    ADBackupset:  Derived class from Backuset Base class, representing a
                            AD agent backupset, and to perform operations on that backupset

    AdBackupset:

        check_subclient()   --  Method to check existing subclient. if not, create new one
Usage
=====


Limitation:
 * current , update subclient content failed. this is limitation in sp12.will tyr in sp13

"""

from __future__ import unicode_literals

from ..backupset import Backupset
from ..exception import SDKException


class ADBackupset(Backupset):
    """ AD agent backupset class """

    def check_subclient(self,
                        backupset_ins,
                        subclientname,
                        storagepolicy=None,
                        subclientcontent=None,
                        deleteexist=False):
        """check if the subclient exsit, will create new one if not found

        Args:

            backupset_ins        (instance)       inherite backupset instance

            subclientname        (string)        subclient name

            storagepolicy        (string)        storage policy name

            subclinetconet        (list)        Ad subclinet content, each element start with path:

            deleteexist            (bool)        if subclient exist, delete or keep existing one

        Return:
            object     Subclient instance

        Raise:
            None
        """
        # add detail for the parameters
        subclients = backupset_ins.subclients
        if subclients.has_subclient(subclientname):
            subclient_ins = subclients.get(subclientname)
            if deleteexist:
                backupset_ins.delete(subclientname)
        else:
            if storagepolicy is None:
                raise SDKException("Subclient", 102, "No storage policy is defined")
            else:
                subclients.add(subclientname, storagepolicy)
                sc_ins = backupset_ins.subclients.get(subclientname)
                content = []
                for entry in subclientcontent:
                    entrydict = {"path" : ",{0}".format(entry)}
                    content.append(entrydict)
                sc_ins._set_subclient_properties("content", content)
                subclient_ins = sc_ins
        return subclient_ins
