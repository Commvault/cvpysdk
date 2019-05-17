# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Alibaba Cloud Instance.

AlibabaCloudInstance is the only class defined in this file.

AlibabaCloudInstance: Derived class from VirtualServer  Base class, representing a
                           Alibaba Cloud instance, and to perform operations on that instance

AlibabaCloudInstance:

    __init__(agent_object,instance_name,instance_id)    --  initialize object of Alibaba Cloud
                                                            Instance object associated with the
                                                            VirtualServer Instance


    _get_instance_properties()                          --  VirtualServer Instance class method
                                                            overwritten to get Alibaba Cloud
                                                            Specific instance properties as well

    _set_instance_properties()                          --  Alibaba Cloud Instance class method
                                                            to set Alibaba Cloud
                                                            Specific instance properties


"""

from ..vsinstance import VirtualServerInstance


class AlibabaCloudInstance(VirtualServerInstance):
    """Class for representing an Alibaba cloud instance of the Virtual Server agent."""

    def __init__(self, agent, instance_name, instance_id=None):
        """Initialize the Instance object for the given Virtual Server instance.

        Args:
            agent               (object)    --  the instance of the agent class

            instance_name       (str)       --  the name of the instance

            instance_id         (int)       --  the instance id

        """
        self._vendor_id = 18
        self._server_name = []
        self._server_host_name = None
        self._username = None
        super(AlibabaCloudInstance, self).__init__(agent, instance_name, instance_id)

    def _get_instance_properties(self):
        """
        Get the properties of this instance

        Raise:
            SDK Exception:
                if response is not empty
                if response is not success
        """

        super(AlibabaCloudInstance, self)._get_instance_properties()
        if "vmwareVendor" in self._virtualserverinstance:
            self._server_host_name = [self._virtualserverinstance['vmwareVendor'][
                'virtualCenter']['domainName']]

            self._username = self._virtualserverinstance['vmwareVendor'][
                'virtualCenter']['userName']

        for _each_client in self._asscociatedclients['memberServers']:
            client = _each_client['client']
            if 'clientName' in client.keys():
                self._server_name.append(str(client['clientName']))

    def _get_instance_properties_json(self):
        """get the all instance related properties of this subclient.

          Returns:
               instance_json    (dict)  --  all instance properties put inside a dict

        """
        instance_json = {
            "instanceProperties":{
                "isDeleted": False,
                "instance": self._instance,
                "instanceActivityControl": self._instanceActivityControl,
                "virtualServerInstance": {
                    "vsInstanceType": self._virtualserverinstance['vsInstanceType'],
                    "associatedClients": self._virtualserverinstance['associatedClients'],
                    "vmwareVendor": self._virtualserverinstance['vmwareVendor'],
                    "xenServer": {}
                    }
            }
        }
        return instance_json

    @property
    def server_host_name(self):
        """return the Alibaba Cloud endpoint

        Returns:
            _server_host_name   (str)   --  the hostname of the Alibaba cloud server
        """
        return self._server_host_name

    @property
    def server_name(self):
        """
        returns the list of all associated clients with the instance

        Returns:
            _server_name    (str)   --  the list of all proxies associated to the instance
        """
        return self._server_name

    @property
    def instance_username(self):
        """returns the username of the instance

        Returns:
            _username   (str)   --  the user name of the Alibaba cloud endpoint
        """
        return self._username
