# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Instance.

VirualServerInstance is the only class defined in this file.

VirtualServerInstance: Derived class from Instance Base class, representing a
                            virtual server instance, and to perform operations on that instance

VirtualServerInstance:

     __new__                    --  Decides which instance object needs to be created

    __init__                    --  initialise object of vsinstance class associated with
                                            the specified agent, instance name and instance id

    _get_instance_properties()  --  Instance class method overwritten to add virtual server
                                        instance properties as well

    associated_clients                --  getter or setter for the associated clients

    co_ordinator                    --  getter

"""

from __future__ import unicode_literals
from past.builtins import basestring

from ..instance import Instance
from ..client import Client
from ..exception import SDKException
from .. import constants


class VirtualServerInstance(Instance):
    """Class for representing an Instance of the Virtual Server agent."""

    def __new__(cls, agent_object, instance_name, instance_id=None):
        """Decides which instance object needs to be created"""

        hv_type = constants.HypervisorType
        if instance_name == hv_type.VIRTUAL_CENTER.value.lower():
            from .virtualserver.VMwareInstance import VMwareInstance
            return object.__new__(VMwareInstance)

        elif instance_name == hv_type.MS_VIRTUAL_SERVER.value.lower():
            from .virtualserver.hypervinstance import HyperVInstance
            return object.__new__(HyperVInstance)

        elif instance_name == hv_type.AZURE_V2.value.lower():
            from .virtualserver.azureRMinstance import AzureRMInstance
            return object.__new__(AzureRMInstance)

        elif instance_name == hv_type.FUSION_COMPUTE.value.lower():
            from .virtualserver.fusioncomputeinstance import FusionComputeInstance
            return object.__new__(FusionComputeInstance)

        elif instance_name == hv_type.ORACLE_VM.value.lower():
            from .virtualserver.oraclevminstance import OracleVMInstance
            return object.__new__(OracleVMInstance)

        elif instance_name == hv_type.ALIBABA_CLOUD.value.lower():
            from .virtualserver.alibabacloudinstance import AlibabaCloudInstance
            return object.__new__(AlibabaCloudInstance)

        elif instance_name == hv_type.ORACLE_CLOUD.value.lower():
            from .virtualserver.oraclecloudinstance import OracleCloudInstance
            return object.__new__(OracleCloudInstance)

        elif instance_name == hv_type.OPENSTACK.value.lower():
            from .virtualserver.openstackinstance import OpenStackInstance
            return object.__new__(OpenStackInstance)

        elif instance_name == hv_type.GOOGLE_CLOUD.value.lower():
            from .virtualserver.googlecloudinstance import GoogleCloudInstance
            return object.__new__(GoogleCloudInstance)

        elif instance_name == hv_type.Azure_Stack.value.lower():
            from .virtualserver.azurestackinstance import AzureStackInstance
            return object.__new__(AzureStackInstance)

        elif instance_name == hv_type.Rhev.value.lower():
            from .virtualserver.rhevinstance import RhevInstance
            return object.__new__(RhevInstance)

        elif instance_name == hv_type.AMAZON_AWS.value.lower():
            from .virtualserver.amazoninstance import AmazonInstance
            return object.__new__(AmazonInstance)

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        super(VirtualServerInstance, self)._get_instance_properties()

        self._vsinstancetype = None
        self._asscociatedclients = None
        if 'virtualServerInstance' in self._properties:
            self._virtualserverinstance = self._properties["virtualServerInstance"]
            self._vsinstancetype = self._virtualserverinstance['vsInstanceType']
            self._asscociatedclients = self._virtualserverinstance['associatedClients']


    @property
    def server_name(self):
        """returns the PseudoClient Name of the associated isntance"""
        return self._agent_object._client_object.client_name


    @property
    def associated_clients(self):
        """Treats the clients associated to this instance as a read-only attribute."""
        self._associated_clients = []
        if "memberServers" in self._asscociatedclients:
            for client in self._asscociatedclients["memberServers"]:
                self._associated_clients.append(client["client"]["clientName"])
            return self._associated_clients

    @associated_clients.setter
    def associated_clients(self, clients_list):
        """sets the associated clients with Client Dict Provided as input

            it replaces the list of proxies in the GUI

        Args:
                client_list:    (list)       --- list of clients or client groups

        Raises:
            SDKException:
                if response is not success

                if input is not list of strings

                if input is not client of CS


        """
        for client_name in clients_list:
            if not isinstance(client_name, basestring):
                raise SDKException('Instance', '105')

        client_json_list = []

        associated_clients = {"memberServers":client_json_list}

        for client_name in clients_list:
            client_json = {
                "clientName": client_name
            }

            client_group_json = {
                "clientGroupName": client_name
            }

            common_json = {
                "srmReportSet": 0,
                "type": 0,
                "srmReportType": 0,
                "clientSidePackage": True,
                "_type_": 28,
                "consumeLicense": True
            }
            final_json = {}
            if self._commcell_object.clients.has_client(client_name):
                common_json['clientName'] = client_name
                final_json['client'] = common_json
            elif self._commcell_object.client_groups.has_clientgroup(client_name):
                common_json['clientName'] = client_name
                final_json['client'] = common_json
            else:
                raise SDKException('Instance', '105')

            client_json_list.append(final_json)

        associated_clients = {"memberServers": client_json_list}
        self._set_instance_properties("_virtualserverinstance['associatedClients']",
                                      associated_clients)


    @property
    def co_ordinator(self):
        """Returns the Co_ordinator of this instance it is read-only attribute"""
        _associated_clients = self.associated_clients
        return _associated_clients[0]
