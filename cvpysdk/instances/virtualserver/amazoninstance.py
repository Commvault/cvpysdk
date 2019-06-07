# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Amazon Instance.

AmazonInstance is the only class defined in this file.

AmazonInstance: Derived class from VirtualServer  Base class, representing a
                           Amazon instance, and to perform operations on that instance

AmazonInstance:
    __init__(agent_object,instance_name,instance_id)    --  initialize object of amazon Instance
                                                            object associated with the
                                                            VirtualServer Instance

"""

from ..vsinstance import VirtualServerInstance
from ...exception import SDKException
from ...instance import Instance


class AmazonInstance(VirtualServerInstance):
    def __init__(self, agent, name, iid):
        self._vendor_id = 4
        self._server_name = []
        super(AmazonInstance, self).__init__(agent, name, iid)

    def _get_instance_properties(self):
        """
        Get the properties of this instance

        Raise:
            SDK Exception:
                if response is not empty
                if response is not success
        """

        super(AmazonInstance, self)._get_instance_properties()
        self._server_name = []
        if 'virtualServerInstance' in self._properties:
            _member_servers = self._properties["virtualServerInstance"] \
                ["associatedClients"]["memberServers"]
            for _each_client in _member_servers:
                client = _each_client['client']
                if 'clientName' in client.keys():
                    self._server_name.append(str(client['clientName']))

    def _get_instance_properties_json(self):
        """get the all instance related properties of this subclient.

           Returns:
                dict - all instance properties put inside a dict

        """
        instance_json = {
            "instanceProperties": {
                "isDeleted": False,
                "instance": self._instance,
                "instanceActivityControl": self._instanceActivityControl,
                "virtualServerInstance": {
                    "vsInstanceType": self._vendor_id,
                    "associatedClients": self._virtualserverinstance['associatedClients'],
                    "vmwareVendor": self._virtualserverinstance['vmwareVendor']
                }
            }
        }

        return instance_json

    @property
    def server_name(self):
        """getter for the domain name in the AWS vendor json"""
        return self._server_name

    @property
    def server_host_name(self):
        """getter for the domain name in the AWS vendor json"""
        return self._server_name
