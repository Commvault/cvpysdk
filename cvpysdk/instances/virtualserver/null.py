# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from cvpysdk.exception import SDKException
from cvpysdk.instances.vsinstance import VirtualServerInstance


class NullSubclient(VirtualServerInstance):

    def __init__(self, agent_object, instance_name, instance_id=None):
        raise SDKException('Instance', '102',
                           'Instance: "{0}" is not yet supported'.
                           format(instance_name))

