# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from cvpysdk.exception import SDKException
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


class NullSubclient(VirtualServerSubclient):

    def __init__(self, backupset_object, subclient_name, subclient_id):
        raise SDKException('Subclient', '102',
                           'Subclient for Instance: "{0}" is not yet supported'.
                           format(backupset_object._instance_object.instance_name))

