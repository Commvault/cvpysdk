#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Instance.

VirualServerInstance is the only class defined in this file.

VirtualServerInstance: Derived class from Instance Base class, representing a
                            virtual server instance, and to perform operations on that instance

VirtualServerInstance:
    _get_instance_properties()  --  Instance class method overwritten to add virtual server
                                        instance properties as well

"""

from __future__ import unicode_literals

from ..instance import Instance
from ..client import Client
from ..exception import SDKException
from .. import constants



class VirtualServerInstance(Instance):
    """Class for representing an Instance of the Virtual Server agent."""

    def __new__(cls,agent_object, instance_name, instance_id=None):
        """Decides which instance object needs to be created"""
        
        hv_type = constants.hypervisor_type
        if(instance_name == hv_type.VIRTUAL_CENTER.value):
            return object.__new__(VMwareInstance)
        
        elif(instance_name  == hv_type.MS_VIRTUAL_SERVER.value):
            from virtualserver.hypervinstance import HyperVInstance
            return object.__new__(HyperVInstance)
    
    def __init__(self,agent_object,instance_name,instance_id):
        
        super(VirtualServerInstance,self).__init__(agent_object,instance_name,instance_id)
        self._properties_dict = {}
        self._INSTANCE = self._commcell_object._services['INSTANCE']% (
                                        self.instance_id)
    
    
    @property
    def _vendor_id(self):
        return self._vendor_id_
    
    @_vendor_id.setter
    def _vendor_id(self,value):
        self._vendor_id_ = int(value)
        
    @property
    def _default_FBRWindows_MediaAgent(self):
        """getter for default FBR Windows Media agent. it is read only attribute"""
    
        _default_FBR_Windows = {
                    "_type_" :11
        }
        
        return _default_FBR_Windows
	
    @property
    def _default_FBRUnix_MediaAgent(self):
        """getter for the default FBR Unix MediaAgent . it is read only attribute"""
        
        return self._default_FBR_unix
    
    @_default_FBRUnix_MediaAgent.setter
    def _default_FBRUnix_MediaAgent(self,value):
        """"setter for Default FBR Unix Media Agent"""
        
        if(not(isinstance(value,dict))):
            raise SDKException('Instance','101')
        
        self._default_FBR_unix = 	{
                "mediaAgentId":int(value.get("browse_ma_id","")),
                "_type_" :11,
                "mediaAgentName":value.get("browse_ma","")
                                }

    @property
    def _vcPassword(self):
        """getter for vcpassword attribute. it is read only attribute"""
        return self._vc_password
    
    @_vcPassword.setter
    def _vcPassword(self,value):
        """ setter for Credential tag  in Instance Property Json"""
        
        if(not(isinstance(value,dict))):
            raise SDKException('Instance','101')
        
        self._vc_password = {
                "userName":value.get("user_name","")
        }

    @property
    def _appId(self):
        """getter for App id tag in Instance Property Json . it is read only attribute"""
        
        _appid_json = {
            "subclientId":0,
            "clientId":int(self._agent_object._client_object.client_id),
            "instanceId":int(self._instance_id),
            "instanceName":self._instance_name,
            "apptypeId":int(self._agent_object.agent_id),
            "subclientName":"",
            "applicationName":self._agent_object.agent_name
        }
        return _appid_json

    @property
    def _docker(self):
        """getter for docker id tag in Instance prop Json. It is read only attribute"""
        return self._docker_json
    
    @_docker.setter
    def _docker(self,value):
        """setter Docker id tag in Instance Property Json"""
        
        if(not(isinstance(value,dict))):
            raise SDKException('Instance','101')
        
        self._docker_json = {
                "serverName":value.get("server_name",""),
                "credentials":{
                    "userName":value.get("user_name","")
                }
        }
        
    @property
    def _open_stack(self):
        """getter for the openstack json. it is read only attribute"""
        return self._openstack_json
    
    @_open_stack.setter
    def _open_stack(self,value):
        """setter for openstack id tag in Instance Property Json"""
        
        if(not(isinstance(value,dict))):
            raise SDKException('Instance','101')
        
        self._openstack_json = {
                "serverName":value.get("server_name",""),
                "credentials":{
                    "userName":value.get("user_name","")
                }
        }	

    @property
    def _azure(self):
        """getter for the Azure tag in Instance property Json . It is read only attribute"""
        return self._azure_json
    
    @_azure.setter
    def _azure(self,value):
        """setter for the Azure tag in Instance property Json"""
        
        if(not(isinstance(value,dict))):
            raise SDKException('Instance','101')
        
        self._azure_json =  {
                "serverName":value.get("server_name",""),
                "credentials":{
                    "userName":value.get("user_name","")
                }
        }

    @property
    def _azure_Resource_Manager(self):
        """getter for the Azure Resource Manager. it is read only attribute"""
        return self._azure_rm_json
    
    @_azure_Resource_Manager.setter
    def _azure_Resource_Manager(self,value):
        """setter for the Azure RM tag in Instance property Json"""
        
        if(not(isinstance(value,dict))):
            raise SDKException('Instance','101')
        
        self._azure_rm_json =  {
                "serverName":value.get("server_name",""),
                "credentials":{
                    "userName":value.get("user_name","")
                }
        }
        
    @property
    def _oracle_cloud(self):
        """getter for the Oracle cloud. it is read only attribute"""
        return self._oracle_cloud_json
    
    @_oracle_cloud.setter
    def _oracle_cloud(self,value):
        """setter for the Azure RM tag in Instance property Json"""
        
        if(not(isinstance(value,dict))):
            raise SDKException('Instance','101')
        
        self._oracle_cloud_json =  {
                "serverName":value.get("server_name",""),
                "credentials":{
                    "userName":value.get("user_name","")
                }
        }
        
    @property
    def _associated_Member_Server(self):
        """getter for the associated member server . it is read only attribute"""
        
        _associated_list = []
        for each_client in self.associated_clients["Clients"]:
            _associated_member_json  = {
                "srmReportSet":0,
                "type":0,
                "hostName":"",
                "clientName":each_client["client_name"],
                "srmReportType":0,
                "clientSidePackage":True,
                "clientId":int(each_client["client_id"]),
                "_type_":3,
                "consumeLicense":True
            }
            _associated_list.append(_associated_member_json)
        
        return _associated_list
		
    def _get_instance_common_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
       
        self._associated_clients = None

        if 'virtualServerInstance' in self._properties:
            virtual_server_instance  = self._properties["virtualServerInstance"]
            if 'associatedClients' in virtual_server_instance:
                associated_clients = virtual_server_instance['associatedClients']

                self._associated_clients = {
                    'Clients': [],
                    'ClientGroups': []
                }

                for member in associated_clients['memberServers']:
                    client = member['client']

                    if 'clientName' in client:
                        temp_dict = {
                            'client_name': str(client['clientName']),
                            'client_id': str(client['clientId'])
                        }
                        self._associated_clients['Clients'].append(temp_dict)
                    elif 'clientGroupName' in client:
                        temp_dict = {
                            'client_group_name': str(client['clientGroupName']),
                            'client_group_id': str(client['clientGroupId'])
                        }
                        self._associated_clients['ClientGroups'].append(temp_dict)
                    else:
                        continue
    
    def _prepare_instance_json(self):
        """Builds the Instance property Json from getters specified"""
    
        _request_json  = {
				  "prop":{
                        "lockId":0,
                        "creatFailIndex":0,
                        "creatFullIndex":True,
                        "dataCollection":0,
						"virtualServerInfo":{
							"hostName":"",
							"description":"",
							"vendor":self._vendor_id,
							"virtualCenter":True,
							"vcloudhostName":"",
							"virtualCenterIsRegistered":False,
							"createClientsForAllVms":False,
							"vcenterWebPluginHost":"",
							"defaultFBRWindowsMediaAgent":self._default_FBRWindows_MediaAgent,
							"defaultFBRUnixMediaAgent":self._default_FBRUnix_MediaAgent,
							"docker":self._docker,
							"appId":self._appId,
							"openStack":self._open_stack,
							"vcPassword":self._vcPassword,
							"esxServersToMount":[""],
							"azure":self._azure,
							"azureResourceManager":self._azure_Resource_Manager,
							"oracleCloud":self._oracle_cloud,
							"associatedMemberServer":self._associated_Member_Server
						},
					"appId":self._appId
					}
			}
        return _request_json
	
    def _update_instance_properties_request(self,request_json):
        """
        receives the request json and make update Instance proeprties request
        
        args:
            request_json  : Makes request to update isntance property with request json
        
        exception:
            raise SDK Exception if
                response is not success
        """
          
                
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST',self._INSTANCE,request_json)
        
        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorString' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorString']

                    o_str = 'Failed to Update Instance Property\nError: "{0}"'.format(error_message)
                    raise SDKException('Instance', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
 
    @property
    def vs_instance_type(self):
        """Treats the vs instance type as a read-only attribute."""
        return self._vs_instance_type

    @property
    def server_name(self):
        """Treats the v-center name as a read-only attribute."""
        return self._server_name


    @property
    def associated_clients(self):
        """Treats the clients associated to this instance as a read-only attribute."""
        
        return self._associated_clients
    
    @associated_clients.setter
    def associated_clients(self,client_name):
        """sets the associated clients with Client Dict Provided as input
        
        Args:
                client_name:    (str)       --- client_name which needed to be added as proxy
        
        Raises:
            SDKException:
                if response is not success
                
                if input is not str
                
                if input is not client of CS
        """
        
        if isinstance(client_name, Client):
            client = client
        elif isinstance(client_name, str):
            client = Client(self._commcell_object, client)
        else:
            raise SDKException('Subclient', '105')
        
        _client_dict["client_name"] = client.client_name
        _client_dict["client_id"] = client.client_id
    
        self.associated_clients["Clients"].append(_client_dict)
        
    @property
    def co_ordinator(self):
        """Returns the Co_ordinator of this instance it is read-only attribute"""
        _associated_clients = self.associated_clients
        return _associated_clients['Clients'][0]
    
    @property
    def fbr_MA_unix(self):
        """Returns the FBRMA of this instance if associated . it is read only attribute"""
        #no such attribute check it
        
    @fbr_MA_unix.setter
    def fbr_MA_unix(self,client_name):
        """ sets FBRMA for this instance
        Args:
                client_name:    (str)       --- client_name which needed to be added as proxy
        
        Raises:
            SDKException:
                if response is not success
                
                if input is not str
                
                if input is not client of CS
        """
        
        if isinstance(client_name, Client):
            client = client
        elif isinstance(client_name, str):
            client = Client(self._commcell_object, client_name)
        else:
            raise SDKException('Subclient', '105')
    
        self._properties_dict["browse_ma"] = client.client_name
        self._properties_dict["browse_ma_id"] = client.client_id
    

            
        

            
            
                