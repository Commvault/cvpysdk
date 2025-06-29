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

"""Module for performing operations on a Backupset for the **File System** Agent.

FSBackupset is the only class defined in this file.

FSBackupset:

    restore_in_place()          --  Restores the files/folders specified in the
    input paths list to the same location

    restore_out_of_place()      --  Restores the files/folders specified in the input paths list
    to the input client, at the specified destionation location

    find_all_versions()         --  Returns the dict containing list of all the backuped up
    versions of specified file

    restore_bmr_admin_json()    --  Returns the restore JSON required for BMR operations.

    restore_bmr_virtualserveropts_json()    --  Returns the Virtual Server JSON options needed
                                                for BMR

    _get_responsefile()          --  Returns the 1-touch response file for that backupset

    run_bmr_restore()           --  Triggers the VIrtualize Me to VMWare job

    _get_cs_login_details()     --  Get the cs login information.

    _restore_aix_1touch_admin_json()    --Returns the restore JSON required for BMR operations.

    run_bmr_aix_restore()               --Triggers the Aix 1-touch restore Job

    index_pruning_type()                --  Sets the index pruning type

    index_pruning_days_retention()      --  Sets the number of days to be maintained in
                                            the index database

    index_pruning_cycles_retention()    --  Sets the number of cycles to be maintained in
                                            the index database

    create_replica_copy()               --  Triggers Replica Copy for live Replication.

    delete_replication_pair()           --  Delete Replication Pair

    get_mount_path_guid()               --  Get the mount path volume's GUID

    get_recovery_points()               --  Gets all the valid recovery points from the RPStore for the BLR pair

    create_fsblr_replication_pair()     --  Create Live/Granular Replication Pair

    create_granular_replica_copy()      --  Triggers  Granular replication permanent mount

    get_browse_volume_guid()            --  It returns browse volume guid

"""

from __future__ import unicode_literals

from ..backupset import Backupset
from ..client import Client
from ..exception import SDKException
from ..job import Job
from ..schedules import Schedules
import socket

class FSBackupset(Backupset):
    """Derived class from Backupset Base class, representing a fs backupset,
        and to perform operations on that backupset."""

    def restore_in_place(
            self,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            fs_options=None,
            restore_jobs=None,
            advanced_options=None
    ):
        """Restores the files/folders specified in the input paths list to the same location.

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl    (bool)  --  restore data and ACL files
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                fs_options      (dict)          -- dictionary that includes all advanced options

                    options:

                        all_versions        : if set to True restores all the versions of the
                                                specified file

                        versions            : list of version numbers to be backed up

                        validate_only       : To validate data backed up for restore

                        no_of_streams   (int)       -- Number of streams to be used for restore

                restore_jobs    (list)          --  list of jobs to be restored if the job is index free restore

                advanced_options    (dict)  -- Advanced restore options

                    Options:

                        job_description (str)   --  Restore job description

                        timezone        (str)   --  Timezone to be used for restore

                            **Note** make use of TIMEZONES dict in constants.py to pass timezone

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        self._instance_object._restore_association = self._backupset_association

        if fs_options is not None and fs_options.get('no_of_streams', 1) > 1 and not fs_options.get('destination_appTypeId', False):
            fs_options['destination_appTypeId'] = int(self._client_object.agents.all_agents.get('file system', self._client_object.agents.all_agents.get('windows file system', self._client_object.agents.all_agents.get('linux file system', self._client_object.agents.all_agents.get('big data apps', self._client_object.agents.all_agents.get('cloud apps', 0))))))
            if not fs_options['destination_appTypeId']:
                del fs_options['destination_appTypeId']

        return self._instance_object._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            fs_options=fs_options,
            restore_jobs=restore_jobs,
            advanced_options=advanced_options
        )

    def restore_out_of_place(
            self,
            client,
            destination_path,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            fs_options=None,
            restore_jobs=None,
            advanced_options=None
    ):
        """Restores the files/folders specified in the input paths list to the input client,
            at the specified destionation location.

            Args:
                client                (str/object) --  either the name of the client or
                                                           the instance of the Client

                destination_path      (str)        --  full path of the restore location on client

                paths                 (list)       --  list of full paths of
                                                           files/folders to restore

                overwrite             (bool)       --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl  (bool)       --  restore data and ACL files
                    default: True

                copy_precedence         (int)      --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)          --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)            --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                fs_options      (dict)             -- dictionary that includes all advanced options

                    options:

                        preserve_level      : preserve level option to set in restore

                        proxy_client        : proxy that needed to be used for restore

                        impersonate_user    : Impersonate user options for restore

                        impersonate_password: Impersonate password option for restore
                                                in base64 encoded form

                        all_versions        : if set to True restores all the versions of the
                                                specified file

                        versions            : list of version numbers to be backed up

                        validate_only       : To validate data backed up for restore

                        no_of_streams   (int)       -- Number of streams to be used for restore

                restore_jobs    (list)          --  list of jobs to be restored if the job is index free restore

                advanced_options    (dict)  -- Advanced restore options

                    Options:

                        job_description (str)   --  Restore job description

                        timezone        (str)   --  Timezone to be used for restore

                            **Note** make use of TIMEZONES dict in constants.py to pass timezone

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if client is not a string or Client instance

                    if destination_path is not a string

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        self._instance_object._restore_association = self._backupset_association

        if not isinstance(client, (str, Client)):
            raise SDKException('Subclient', '101')

        if isinstance(client, str):
            client = Client(self._commcell_object, client)

        if fs_options is not None and fs_options.get('no_of_streams', 1) > 1 and not fs_options.get('destination_appTypeId', False):
            fs_options['destination_appTypeId'] = int(client.agents.all_agents.get('file system', client.agents.all_agents.get('windows file system', client.agents.all_agents.get('linux file system', client.agents.all_agents.get('big data apps', client.agents.all_agents.get('cloud apps', 0))))))
            if not fs_options['destination_appTypeId']:
                del fs_options['destination_appTypeId']

        return self._instance_object._restore_out_of_place(
            client=client,
            destination_path=destination_path,
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            fs_options=fs_options,
            restore_jobs=restore_jobs,
            advanced_options=advanced_options
        )

    def find_all_versions(self, *args, **kwargs):
        """Searches the content of a Subclient, and returns all versions available for the content.

            Args:
                Dictionary of browse options:
                    Example:
                        find_all_versions({
                            'path': 'c:\\hello',
                            'show_deleted': True,
                            'from_time': '2014-04-20 12:00:00',
                            'to_time': '2016-04-31 12:00:00'
                        })

                    (OR)

                Keyword argument of browse options:
                    Example:
                        find_all_versions(
                            path='c:\\hello.txt',
                            show_deleted=True,
                            to_time='2016-04-31 12:00:00'
                        )

                Refer self._default_browse_options for all the supported options

        Returns:
            dict    -   dictionary of the specified file with list of all the file versions and
                            additional metadata retrieved from browse

        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['operation'] = 'all_versions'

        return self._do_browse(options)

    def _restore_bmr_admin_json(self, ipconfig, hwconfig):
        """"setter for the BMR options required  for 1-touch restore

        Args:
            ipconfig    (dict)  -- The IP Configuration details obtained form response file.

            hwconfig    (dict)  -- The hardware configuration details obtained form response file.

        Returns :
                    returns the JSON required for BMR
        """
        bmr_restore_vmprov_json = {
            "vmProvisioningOption": {
                "operationType": 14, "virtualMachineOption": [
                    {
                        "powerOnVM": True, "isoPath": " ", "flags": 0,
                        "useLinkedClone": False, "vendor": 1,
                        "doLinkedCloneFromLocalTemplateCopy": False,
                        "oneTouchResponse": {
                            "copyPrecedence": 0, "version": "10.0", "platform": 1,
                            "dateCreated": "",
                            "automationTest": False, "autoReboot": True, "clients": [
                                {
                                    "platform": 1, "isBlockLevelBackup": False,
                                    "indexCachePath": "",
                                    "isClientMA": False, "clone": False,
                                    "isIndexCacheInUSB": True, "firewallCS": "",
                                    "backupSet": {
                                        "backupsetName": self.backupset_name,
                                        "backupsetId": int(self.backupset_id)
                                    }, "netconfig":{
                                        "wins":{
                                            "useDhcp": False
                                        },
                                        "firewall": {
                                            "certificatePath": "", "certificateBlob": "",
                                            "configBlob": ""
                                        }, "hosts": [
                                            {
                                                "fqdn": "", "alias": "", "ip": {}
                                            }
                                        ],
                                        "dns":
                                        {
                                            "suffix": "", "useDhcp": False
                                        }, "ipinfo": ipconfig
                                    },
                                    "platformConfig":
                                        {
                                            "platformCfgBlob": "", "win_passPhrase": "",
                                            "win_licenceKey": "", "type": 1,
                                            "goToMiniSetUp": 0, "Win_DomainCreds":
                                            {
                                                "isClientInDomain": True, "DomainCreds":
                                                {
                                                    "password": "", "domainName": "#####",
                                                    "confirmPassword": "",
                                                    "userName": ""
                                                }
                                            }
                                        },
                                    "firewallLocal": {
                                        "certificatePath": "", "certificateBlob": "", "configBlob": ""
                                    },
                                    "client": {
                                        "hostName": " ", "clientName": " ",
                                        "type": 0
                                    },
                                    "indexPathCreds": {
                                        "password": "", "domainName": "", "confirmPassword": "",
                                        "userName": ""
                                    }, "newclient": {
                                        "hostName": "", "clientName": ""
                                    }
                                }
                            ], "csinfo": {
                                "firewallPort": 0, "cvdPort": 0, "evmgrPort": 0,
                                "fwClientGroupName": "",
                                "mediaAgentInfo": {

                                }, "mediaAgentIP": {

                                }, "ip": {
                                    "address": " "
                                }, "commservInfo": {
                                    "hostName": " ", "clientName": ""
                                }, "creds": {
                                    "password": " ",
                                    "domainName": "", "confirmPassword": "", "userName": "admin"
                                }
                            }, "hwconfig": hwconfig,
                            "netconfig": {
                                "wins": {
                                    "useDhcp": False
                                }, "firewall": {
                                    "certificatePath": "", "certificateBlob": "", "configBlob": ""
                                }, "dns": {
                                    "suffix": "", "useDhcp": False
                                }, "ipinfo": {
                                    "defaultgw": ""
                                }
                            }, "dataBrowseTime": {

                            }, "maInfo":
                                {
                                    "clientName": ""
                                }, "datastoreList": {}
                        }, "vmInfo": {
                            "registerWithFailoverCluster": False, "proxyClient": {
                                "clientName": " "
                            }, "vmLocation": {
                                "pathName": " ", "inventoryPath": "",
                                "hostName": " ", "resourcePoolPath": "", "dataCenterName": "",
                                "vCenter": " ", "datastore": {
                                    "name": " "
                                    },
                                "instanceEntity": {
                                    "clientName": "",
                                    "instanceName": "",
                                    "instanceId": 0
                                }
                                }, "expirationTime": {}
                        }
                    }
                ]
            }
        }
        return bmr_restore_vmprov_json

    def _restore_bmr_virtualserveropts_json(self):
        """Get the JSON for virtual server options


        Returns :
                    The virtualserver options JSON required for Virtualize Me restores

        """
        bmr_restore_json = {
            "diskLevelVMRestoreOption": {
                "esxServerName": " ", "userPassword": {

                }
            }
        }
        return bmr_restore_json

    def _restore_bmr_firewallopts_json(self, hostname, direction, port):
        """Get the JSON for firewall configuration options

        Args:
            hostname    (String)   -- The hostname of the machine.

            direction   (Integer)  -- The direction of the connection.

            port        (Integer)  -- The port at which the machine will communicate.

        Returns :
                    The firewall configuration options JSON required for Virtualize Me restores

        """
        bmr_firewall_restore_json = {
            "direction": direction,
            "connectionInfoList": [
                {
                    "hostname": hostname,
                    "port": port
                }
            ]
        }
        return bmr_firewall_restore_json

    def _azure_advancedrestoreopts_json(self):
        """Get the JSON for Advanced restore options for azure


        Returns :
                    The Advanced restore options JSON required for Virtualize Me to Azure restores

        """
        azure_adv_rest_opts_json = [
            {
                "vmSize": "",
                "securityGroups": [
                    {
                        "groupName": "--Auto Select--",
                        "groupId": ""
                    }
                ]
            }
        ]
        return azure_adv_rest_opts_json

    def _azure_advancedopts_json(self):
        """Get the JSON for Advanced restore options for azure


        Returns :
                    The Advanced restore options JSON required for Virtualize Me to Azure restores

        """
        azure_adv_opts_json = {
            "networkCards": [
                {
                    "privateIPAddress": "",
                    "networkName": "",
                    "label": "--Auto Select--",
                    "subnetNames": [
                        {
                            "subnetId": ""
                        }
                    ]
                }
            ]
        }
        return azure_adv_opts_json


    def _get_responsefile(self):
        """Get the response file for the backupset

        Returns :
            (dict, dict) - The hardware and IP configuration details from the response file obtained

        """
        request = {
            "CVGui_GetResponseFilesReq": {
                "entity": {
                    "_type_": "6",
                    "appName": "File System",
                    "applicationId": self._agent_object.agent_id,
                    "backupsetId": self.backupset_id,
                    "backupsetName": self.backupset_name,
                    "clientId": self._agent_object._client_object.client_id,
                    "clientName": self._agent_object._client_object.client_name,
                    "commCellId": "0",
                    "commCellName": "",
                    "instanceId": "1",
                    "instanceName": ""
                },
                "RecoveryTime": "",
                "platform": "1",
                "virtualizeME": "1"
            }
        }

        response = self._commcell_object._qoperation_execute(request)

        hwconfig = response['responseFile']['hwconfig']
        ipconfig = response['responseFile']['clients'][0]['netconfig']['ipinfo']
        cs_user = response['responseFile']['csinfo']['creds']['userName']
        cs_pwd = response['responseFile']['csinfo']['creds']['password']
        cs_token = response['responseFile']['csinfo']['creds']['password'][5:]
        return hwconfig, ipconfig,cs_user,cs_pwd,cs_token

    def run_bmr_restore(self, **restore_options):
        """
        Calling the create task API with the final restore JSON

        Args :
                IsoPath                 (String)    : The location of ISO in the datastore

                CommServIP              (String)    : The IP of the CS

                CommServHostname        (String)    : The hostname of he CS

                CommServUsername        (String)    : The username for the Comcell

                CommServPassword        (String)    : The password for the comcell

                Datastore               (String)    : The ESX store in which the VM is provisioned

                VcenterServerName       (String)    : The Vcenter to be used

                ClientHostName          (String)    : The hostname of the client being virtualized.

                VmName                  (String)    : The name with which the VM is provisioned.

                VirtualizationClient    (String)    : The vmware virualization client

                EsxServer               (String)    : The ESX server name

               NetworkLabel             (String)    : The network label to be assigned to the VM.

               HyperVHost               (String)    : The Hyper-V host

               GuestUser                (String)    : The Username of the guest OS

               GuestPassword            (String)    : The Password of the guest OS

               CloneClientName          (String)    : The clone client name

        Returns :
                    returns the task object

        """
        client_name = self._agent_object._client_object.client_name

        self._instance_object._restore_association = self._backupset_association

        hwconfig, ipconfig, cs_username, cs_password = self._get_responsefile()
        response_json = self._restore_json(paths=[''])

        restore_json_system_state = self._restore_bmr_admin_json(ipconfig, hwconfig)
        restore_json_virtualserver = self._restore_bmr_virtualserveropts_json()

        #Checking for Firewall rules
        if restore_options.get("FirewallClientGroup", "").strip():
            fwconfigtocs = self._restore_bmr_firewallopts_json(restore_options.get("FirewallHostname"),
                                                               restore_options.get("FirewallDirection"),
                                                               restore_options.get("FirewallPort"))
            restore_json_system_state['vmProvisioningOption']['virtualMachineOption'][0][
                'oneTouchResponse']['clients'][0]['fwconfigtocs'] = fwconfigtocs
            restore_json_system_state['vmProvisioningOption']['virtualMachineOption'][0]['oneTouchResponse']['csinfo'][
                'fwClientGroupName'] = restore_options.get("FirewallClientGroup")

        #Get instance Id of the virtual client
        virtual_client_object = self._commcell_object.clients.get(restore_options.get('VirtualizationClient'))
        virtual_agent_object = virtual_client_object.agents.get('Virtual Server')
        instances_list = virtual_agent_object.instances._instances
        instance_id = int(list(instances_list.values())[0])
        instance_name = list(instances_list.keys())[0]

        response_json['taskInfo']['subTasks'][0]['options'][
            'adminOpts'] = restore_json_system_state

        response_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'virtualServerRstOption'] = restore_json_virtualserver

        response_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination'][
            'inPlace'] = False
        response_json['taskInfo']['subTasks'][0]['subTask']['subTaskType'] = 1
        response_json['taskInfo']['subTasks'][0]['subTask']['operationType'] = 4041

        vm_option = response_json['taskInfo']['subTasks'][0]['options']['adminOpts'][
            'vmProvisioningOption']['virtualMachineOption'][0]

        vm_option['vmInfo']['vmLocation']['instanceEntity']['clientName'] = restore_options.get('VirtualizationClient')
        vm_option['vmInfo']['vmLocation']['instanceEntity']['instanceId'] = instance_id

        if(response_json['taskInfo']['subTasks'][0]['options']['adminOpts'][
            'vmProvisioningOption']['virtualMachineOption'][0]['oneTouchResponse'][
            'hwconfig']['mem_size']) < 4096:
            vm_option['oneTouchResponse']['hwconfig']['mem_size'] = 4096

        if restore_options.get('CommServIP'):
            cs_ip = restore_options.get('CommServIP')
        else:
            try:
                cs_ip = socket.gethostbyname(self._commcell_object.commserv_hostname)

            except Exception as e:
                raise SDKException('Backupset', '102', 'Error while reading CommServer IP : {}\n. Please set the CommServIP argument.'.format(e))

        vm_option['oneTouchResponse']['csinfo']['ip'][
            'address'] = cs_ip

        vm_option['oneTouchResponse']['csinfo']['commservInfo'][
            'clientName'] = self._commcell_object.commserv_name
        vm_option['oneTouchResponse']['csinfo']['commservInfo'][
            'hostName'] = self._commcell_object.commserv_hostname

        vm_option['oneTouchResponse']['csinfo']['creds'][
            'password'] = cs_password

        vm_option['oneTouchResponse']['csinfo']['creds'][
            'userName'] = cs_username

        vm_option['oneTouchResponse']['hwconfig']['vmName'] = restore_options.get('VmName', None)

        vm_option['oneTouchResponse']['hwconfig']['overwriteVm'] = True

        vm_option['oneTouchResponse']['clients'][0]['client'][
            'hostName'] = restore_options.get('ClientHostname', None)

        vm_option['oneTouchResponse']['clients'][0]['client'][
            'clientName'] = restore_options.get('ClientName', None)

        if instance_name == 'vmware' or instance_name == 'hyper-v':

            vm_option['isoPath'] = restore_options.get('IsoPath')

            vm_option['vmInfo']['vmLocation']['pathName'] = restore_options.get('IsoPath', None)

            vm_option['oneTouchResponse']['clients'][0]['netconfig']['ipinfo']['interfaces'][0][
                'protocols'][0]['useDhcp'] = True

            vm_option['oneTouchResponse']['clients'][0]['netconfig']['ipinfo']['interfaces'][0][
                'networkLabel'] = restore_options.get('NetworkLabel', None)

            if 'scsi_disks' in vm_option['oneTouchResponse']['hwconfig']:
                vm_option['oneTouchResponse']['hwconfig']['scsi_disks'][0][
                    'dataStoreName'] = restore_options.get('Datastore', None)

            if 'ide_disks' in vm_option['oneTouchResponse']['hwconfig']:
                vm_option['oneTouchResponse']['hwconfig']['ide_disks'][0][
                    'dataStoreName'] = restore_options.get('Datastore', None)

            vm_option['vmInfo']['vmLocation']['datastore'][
                'name'] = restore_options.get('Datastore', None)

            if instance_name == 'vmware':

                vm_option['vmInfo']['proxyClient'][
                    'clientName'] = restore_options.get('VirtualizationClient', None)

                response_json['taskInfo']['subTasks'][0]['options'][
                    'restoreOptions']['virtualServerRstOption']['diskLevelVMRestoreOption'][
                        'esxServerName'] = restore_options.get('VcenterServerName', None)

                response_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination'][
                    'destClient']['clientName'] = restore_options.get('VirtualizationClient', None)

                vm_option['vmInfo']['vmLocation']['hostName'] = restore_options.get(
                    'EsxServer')

                vm_option['vmInfo']['vmLocation']['vCenter'] = restore_options.get('VcenterServerName')

            if instance_name == 'hyper-v':

                if restore_options.get('OsType') == 'UNIX':

                    vm_option['vendor'] = 'MICROSOFT'

                response_json['taskInfo']['subTasks'][0]['options'][
                    'restoreOptions']['virtualServerRstOption']['diskLevelVMRestoreOption'][
                        'esxServerName'] = restore_options.get('VirtualizationClient', None)

                response_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination'][
                    'destClient']['clientName'] = restore_options.get('VirtualizationClient', None)

                vm_option['vmInfo']['vmLocation']['hostName'] = restore_options.get(
                    'HyperVHost')

                vm_option['vmInfo']['vmLocation']['vCenter'] = restore_options.get('VirtualizationClient')

        if 'azure' in instance_name:

            az_advanced_ops_json = self._azure_advancedopts_json()

            az_adv_restore_opts_json = self._azure_advancedrestoreopts_json()

            vm_option['vendor'] = 7

            vm_option['createPublicIp'] = restore_options.get('CreatePublicIP')

            vm_option['oneTouchResponse']['clients'][0]['isBlockLevelBackup'] = True

            vm_option['vmInfo']['vmLocation']['advancedProperties'] = az_advanced_ops_json

            vm_option['vmInfo']['vmLocation']['advancedProperties']['networkCards'][0]['label'] = "--Auto Select--"
            vm_option['vmInfo']['vmLocation']['hostName'] = restore_options.get('ResourceGroup')

            response_json['taskInfo']['subTasks'][0]['options'][
                'restoreOptions']['virtualServerRstOption']['diskLevelVMRestoreOption'][
                'advancedRestoreOptions'] = az_adv_restore_opts_json

            response_json['taskInfo']['subTasks'][0]['options'][
                'restoreOptions']['virtualServerRstOption']['diskLevelVMRestoreOption'][
                'advancedRestoreOptions'][0]['securityGroups'][0]['groupName'] = "--Auto Select--"

            response_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination'][
                'destClient']['clientName'] = restore_options.get('VirtualizationClient', None)

            if 'scsi_disks' in vm_option['oneTouchResponse']['hwconfig']:
                vm_option['oneTouchResponse']['hwconfig']['scsi_disks'][0][
                    'dataStoreName'] = restore_options.get('StorageAccount', None)

            if 'ide_disks' in vm_option['oneTouchResponse']['hwconfig']:
                vm_option['oneTouchResponse']['hwconfig']['ide_disks'][0][
                    'dataStoreName'] = restore_options.get('StorageAccount', None)

            vm_option['vmInfo']['vmLocation']['datastore'][
                'name'] = restore_options.get('StorageAccount', None)

        if instance_name == 'azure stack':

            vm_option['vmInfo']['vmLocation']['vCenter'] = restore_options.get('ManagementURL', None)

            vm_option['vendor'] = 17

    # Additional options

        if restore_options.get('CloneClientName'):
            vm_option['oneTouchResponse']['clients'][0]['clone'] = True
            vm_option['oneTouchResponse']['clients'][0]['newclient'][
                'clientName'] = restore_options.get('CloneClientName', None)
            vm_option['oneTouchResponse']['clients'][0]['newclient'][
                'hostName'] = restore_options.get('CloneClientName', None)

        if restore_options.get('OsType') == 'UNIX':
            vm_option['oneTouchResponse']['clients'][0]['newclient'][
                'hostName'] = ''

        if restore_options.get('UseDhcp'):
            vm_option['oneTouchResponse']['clients'][0]['netconfig']['ipinfo']['interfaces'][0][
                'protocols'][0]['useDhcp'] = True


        return self._process_restore_response(response_json)

    def _get_cs_login_details(self):
        """Get the cs login information.

        Returns :
            (dict, dict) - CS login details

        """
        request = {
            "CVGui_GetResponseFilesReq": {
                "entity": {
                    "_type_": "6",
                    "appName": "File System",
                    "applicationId": self._agent_object.agent_id,
                    "backupsetId": self.backupset_id,
                    "backupsetName": self.backupset_name,
                    "clientId": self._agent_object._client_object.client_id,
                    "clientName": self._agent_object._client_object.client_name,
                    "commCellId": "0",
                    "commCellName": "",
                    "instanceId": "1",
                    "instanceName": ""
                },
                "RecoveryTime": "",
                "platform": "1",
                "virtualizeME": "1"
            }
        }

        response = self._commcell_object._qoperation_execute(request)
        cs_user = self._commcell_object.commcell_username
        cs_pwd = self._commcell_object.auth_token
        cs_token = self._commcell_object.auth_token[5:]
        cs_name = self._commcell_object.commserv_name
        cs_hostname = self._commcell_object.commserv_hostname
        cs_ip_address = socket.gethostbyname(self._commcell_object.commserv_hostname)

        return cs_name, cs_hostname, cs_ip_address, cs_user, cs_pwd, cs_token

    def _restore_aix_1touch_admin_json(self):
        """"setter for the BMR options required  for 1-touch restore

                Returns :
                            returns the JSON required for BMR
                """

        bmr_restore_aix1touch_json = {

            "restoreFromBackupBeforeDate": False, "recoverAllVolumeGroups": True,
            "automaticClientReboot": True, "preserveExistingVolumeGroups": False, "responseData":
                [
                    {
                        "copyPrecedence": 0, "version": "", "platform": 0, "dateCreated": "",
                        "automationTest": False, "autoReboot": True, "clients": [
                            {
                                "platform": 0, "isBlockLevelBackup": False, "indexCachePath": "", "isClientMA": False,
                                "clone": True, "isIndexCacheInUSB": True, "firewallCS": "", "backupSet":
                                {
                                    "_type_": 6
                                }, "netconfig":
                                {
                                    "wins":
                                    {
                                        "useDhcp": False
                                    },
                                    "firewall":
                                        {
                                            "certificatePath": "", "certificateBlob": "", "configBlob": ""
                                        },
                                    "hosts": [
                                        {
                                            "fqdn": "", "alias": "",
                                            "ip": {}
                                        }
                                    ], "dns": {
                                        "suffix": "", "useDhcp": False, "nameservers":
                                        [
                                            {
                                                "address": "", "family": 32
                                            }
                                        ]
                                    }, "ipinfo": {
                                        "defaultgw": "", "interfaces":
                                            [
                                                {
                                                    "adapter": 0, "networkLabel": "", "vlan": 0,
                                                    "macAddressType": 0,
                                                    "isEnabled": True, "name": "", "mac": "",
                                                    "classicname": "", "wins":
                                                    {
                                                        "useDhcp": False
                                                    }, "dns":{
                                                        "suffix": "", "useDhcp": False
                                                    }, "protocols":[
                                                        {
                                                            "gw": "", "subnetId": "", "netmask": "",
                                                            "networkAddress": "", "useDhcp": False,
                                                            "ip":
                                                                {
                                                                    "address": ""
                                                                }
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    }, "platformConfig": {
                                        "platformCfgBlob": "", "win_passPhrase": "", "win_licenceKey": "", "type": 0,
                                        "goToMiniSetUp": 0, "Win_DomainCreds": {
                                            "isClientInDomain": False, "DomainCreds":{
                                                "password": "", "domainName": "", "confirmPassword": "", "userName": ""
                                            }
                                        }
                                    }, "firewallLocal": {
                                        "certificatePath": "", "certificateBlob": "", "configBlob": ""
                                    }, "client": {},
                                "indexPathCreds": {
                                    "password": "", "domainName": "", "confirmPassword": "", "userName": ""
                                }, "newclient": {
                                    "hostName": "", "clientName": ""
                                }
                            }
                        ], "csinfo": {
                            "firewallPort": 0, "cvdPort": 0, "evmgrPort": 0, "fwClientGroupName": "",
                            "mediaAgentInfo": {
                                "_type_": 3
                            }, "mediaAgentIP": {
                            }, "ip": {
                                "address": ""
                            }, "commservInfo": {
                                "hostName": "", "clientName": ""
                            }, "creds": {
                                "password": "", "domainName": "",
                                "confirmPassword": "", "userName": "", "token":""
                            }
                        }, "hwconfig": {
                            "minMemoryMB": 0, "vmName": "", "magicno": "", "enableDynamicMemory": False,
                            "bootFirmware": 0, "version": "", "mem_size": 0, "cpu_count": 1, "maxMemoryMB": 0,
                            "nic_count": 1, "overwriteVm": False, "useMtptSelection": False, "ide_count": 0,
                            "mtpt_count": 0, "scsi_count": 0, "diskType": 1, "optimizeStorage": False, "systemDisk": {
                                "forceProvision": False, "bus": 0, "refcnt": 0, "size": 0, "scsiControllerType": 0,
                                "name": "", "dataStoreName": "", "vm_disk_type": 0, "slot": 0, "diskType": 1,
                                "tx_type": 0
                            }
                        }, "netconfig": {
                            "wins": {
                                "useDhcp": False
                            }, "firewall": {
                                "certificatePath": "", "certificateBlob": "", "configBlob": ""
                            }, "dns": {
                                "suffix": "", "useDhcp": False
                            }, "ipinfo": {
                                "defaultgw": ""
                            }
                        }, "dataBrowseTime": {
                            "_type_": 55
                        }, "maInfo": {
                            "clientName": ""
                        }, "datastoreList": {
                        }
                    }
                ]
        }
        return bmr_restore_aix1touch_json

    def run_bmr_aix_restore(self, **restore_options):
        """
                Calling the create task API with the final restore JSON

                Args :


                        Clone Clinet Name  (String)     : Clone machine name

                        Clone Hostname  (String)        :Clone machine host name

                        DNS Suffix      (String)        :Dns suffix name

                        DNS IP  (Integer)                :Ip of Dns Address

                        Clone IP    (Integer)            :Clone Machine IP

                        Clone Netmask (Integer)          :Clone Machine NetMask

                        Clone Gateway (Integer)          :Clone Machine Gateway

                        Auto Reboot   (Boolean)          :Client machine Auto reboot(True or False)

                        Clone          (Boolean)         :Is Clone enabled(True or False)

                        CS_Username   (String)    : The username for the Comcell

                        CS_Password   (String)     : The password for the comcell

                Returns :
                            returns the task object

                """
        self._instance_object._restore_association = self._backupset_association
        request_json = self._restore_json(paths=[''])
        restore_json_aix_system_state = self._restore_aix_1touch_admin_json()
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'oneTouchRestoreOption'] = restore_json_aix_system_state
        hwconfig_aix = restore_json_aix_system_state['responseData'][0]['hwconfig']
        ipconfig_aix = restore_json_aix_system_state['responseData'][0]['clients'][0]['netconfig']['ipinfo']
        cs_name, cs_hostname, cs_ip_address, cs_user, cs_pwd, cs_token = self._get_cs_login_details()
        vmjson = self._restore_bmr_admin_json(ipconfig_aix, hwconfig_aix)
        request_json['taskInfo']['subTasks'][0]['options']['adminOpts'] = vmjson
        is_clone = restore_options.get('clone', None)
        subtask_json = {
            'subTaskType' : 3,
            'operationType': 1006
        }
        common_options = {
            'systemStateBackup' : True,
            'copyToObjectStore' :False,
            'restoreToDisk' : False,
            'skipIfExists' : restore_options.get('run_FS_restore', False),
            'SyncRestore' : False
        }
        response_data = {
                "clients": [{
                    "clone": is_clone,
                    "netconfig": {
                        "dns": {
                            "suffix": restore_options.get('dns_suffix', None),
                            "nameservers": [{
                                "address": restore_options.get('dns_ip', None),
                            }]
                        },
                        "ipinfo": {
                            "interfaces": [{
                                "protocols": [{
                                    "gw": restore_options.get('clone_machine_gateway', None),
                                    "netmask": restore_options.get('clone_machine_netmask', None),
                                    "ip": {
                                        "address": restore_options.get('clone_ip_address', None)
                                    }
                                }]
                            }]
                        }
                    },
                    "newclient": {
                        "hostName": restore_options.get('clone_client_hostname', None),
                        "clientName": restore_options.get('clone_client_name', None)
                    }
                }],
                "csinfo": {
                    "ip": {
                        "address": cs_ip_address
                    },
                    "commservInfo": {
                        "hostName": cs_hostname,
                        "clientName": cs_name
                    },
                    "creds": {
                        "password": cs_pwd,
                        "confirmPassword": cs_pwd,
                        "userName": cs_user,
                        "token":  cs_token
                    }
                },
            }
        request_json['taskInfo']['subTasks'][0]['subTask'] = subtask_json
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['commonOptions'] = common_options
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination']['destPath'] = (
            [restore_options.get('onetouch_server_directory', '')])
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination'][
            'destClient']['clientName'] = restore_options.get('onetouch_server', None)
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'oneTouchRestoreOption']['automaticClientReboot'] = restore_options.get('automaticClientReboot', None)

        if is_clone:
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['oneTouchRestoreOption'][
                'responseData'][0]['clients'][0]['netconfig'][
                    'dns']['nameservers'][0]['address'] = restore_options.get('dns_ip', None)
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['oneTouchRestoreOption']['responseData'][
            0] = response_data
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['oneTouchRestoreOption'][
            'restoreFromBackupBeforeDate'] = True if restore_options.get('restoreFromBackupBeforeDate') else False
        if restore_options.get('onetouch_backup_jobid') is not None:
            _job = self._commcell_object.job_controller.get(restore_options.get('onetouch_backup_jobid'))
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["browseOption"][
                "timeRange"]["toTime"] = _job.end_timestamp
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["browseOption"][
                "timeRange"]["fromTime"] = _job.start_timestamp

            request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['vmProvisioningOption'][
                'virtualMachineOption'][0]['oneTouchResponse']['dataBrowseTime'][
                'TimeZoneName'] = self._commcell_object.commserv_timezone
            request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['vmProvisioningOption'][
                'virtualMachineOption'][0]['oneTouchResponse']['dataBrowseTime']['time'] = _job.end_timestamp

            one_touch_option = {'fromTime': 0, 'toTime': _job.end_timestamp}
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['oneTouchOption'] = one_touch_option
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['fileOption'][
                'sourceItem'] = ([f'2:{_job.job_id}'])
        return self._process_restore_response(request_json)

    @property
    def index_server(self):
        """Returns the index server client set for the backupset"""

        client_name = None

        if 'indexSettings' in self._properties:
            if 'currentIndexServer' in self._properties['indexSettings']:
                client_name = self._properties['indexSettings']['currentIndexServer']['clientName']

        if client_name is not None:
            return Client(self._commcell_object, client_name=client_name)

        return None

    @index_server.setter
    def index_server(self, value):
        """Sets index server client for the backupset. Property value should be a client object

            Args:
                value   (object)    --  The cvpysdk client object of the index server client

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """

        if not isinstance(value, Client):
            raise SDKException('Backupset', '106')

        properties = self._properties
        index_server_id = int(value.client_id)
        index_server_name = value.client_name

        if 'indexSettings' in properties:
            qualified_index_servers = []
            if 'qualifyingIndexServers' in properties['indexSettings']:
                for index_server in properties['indexSettings']['qualifyingIndexServers']:
                    qualified_index_servers.append(index_server['clientId'])

            if index_server_id in qualified_index_servers:
                properties['indexSettings']['currentIndexServer'] = {
                    'clientId': index_server_id,
                    'clientName': index_server_name
                }
            else:
                raise SDKException(
                    'Backupset', '102', '{0} is not a qualified IndexServer client'.format(
                        index_server_name))
        else:
            properties['indexSettings'] = {
                'currentIndexServer': {
                    'clientId': index_server_id,
                    'clientName': index_server_name
                }
            }

        request_json = {
            'backupsetProperties': properties
        }

        self._process_update_reponse(request_json)

    @property
    def index_pruning_type(self):
        """Returns index pruning type for the backupset"""
        return self._properties["indexSettings"]["indexPruningType"]

    @property
    def index_pruning_days_retention(self):
        """Returns number of days to be maintained in index by index pruning for the backupset"""

        return self._properties["indexSettings"]["indexRetDays"]

    @property
    def index_pruning_cycles_retention(self):
        """Returns number of cycles to be maintained in index by index pruning for the backupset"""

        return self._properties["indexSettings"]["indexRetCycles"]

    @index_pruning_type.setter
    def index_pruning_type(self, value):
        """Updates the pruning type for the backupset when backupset level indexing is enabled.
        Can be days based pruning or cycles based pruning.
        Days based pruning will set index retention on the basis of days,
        cycles based pruning will set index retention on basis of cycles.

        Args:
            value    (str)  --  "days_based" or "cycles_based"

        """

        if value.lower() == "cycles_based":
            final_value = 1

        elif value.lower() == "days_based":
            final_value = 2

        elif value.lower() == "infinite":
            final_value = 0

        else:
            raise SDKException('Backupset', '104')

        request_json = {
            "backupsetProperties": {
                "indexSettings": {
                    "indexRetCycle": 0,
                    "overrideIndexPruning": 1,
                    "indexRetDays": 0,
                    "isPruningEnabled": 1,
                    "indexPruningType": final_value

                }
            }
        }

        self._process_update_reponse(request_json)

    @index_pruning_days_retention.setter
    def index_pruning_days_retention(self, value):
        """Sets index pruning days value at backupset level for days-based index pruning"""

        if isinstance(value, int) and value >= 2:
            request_json = {
                "backupsetProperties": {
                    "indexSettings": {
                        "indexRetCycle": 0,
                        "overrideIndexPruning": 1,
                        "indexRetDays": value,
                        "isPruningEnabled": 1,
                        "indexPruningType": 2
                    }
                }
            }

            self._process_update_reponse(request_json)
        else:
            raise SDKException('Backupset', '105')

    @index_pruning_cycles_retention.setter
    def index_pruning_cycles_retention(self, value):
        """Sets index pruning cycles value at backupset level for cycles-based index pruning"""

        if isinstance(value, int) and value >= 2:
            request_json = {
                "backupsetProperties": {
                    "indexSettings": {
                        "indexRetCycle": value,
                        "overrideIndexPruning": 1,
                        "indexRetDays": 0,
                        "isPruningEnabled": 1,
                        "indexPruningType": 1
                    }
                }
            }

            self._process_update_reponse(request_json)
        else:
            raise SDKException('Backupset', '105')


    def create_replica_copy(self, srcclientid, destclientid, scid, blrid,
                            srcguid, dstguid, **replication_options):

        """"setter for live  blklvl Replication replica copy...

        Args:
            srcclientid   (int)  --  Source client id.

            destclientid    (dict)  -- Destintion client id .

            scid           (int) --  Replication Subclient id

            blrid           (int) -- Blr pair id

            srcguid         (str) -- Browse guid of source

            dstguid          (str) -- Browse guid of destination volume

            **replication_options (dict) -- object instance


        """
        srcvol = replication_options.get('srcvol')
        restorepath = replication_options.get('RestorePath')
        replicacopyjson = {
            "taskInfo": {
                "task": {
                    "ownerId": 1,
                    "taskType": 1,
                    "ownerName": "",
                    "initiatedFrom": 1,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 4047
                        },
                        "options": {
                            "backupOpts": {
                                "mediaOpt": {
                                    "auxcopyJobOption": {
                                        "maxNumberOfStreams": 0,
                                        "allCopies": True,
                                        "useMaximumStreams": True,
                                        "useScallableResourceManagement": False
                                    }
                                }
                            },
                            "adminOpts": {
                                "blockOperation": {
                                    "operations": [
                                        {
                                            "appId": int(scid),
                                            "opType": 8,
                                            "dstProxyClientId": int(destclientid),
                                            "fsMountInfo": {
                                                "doLiveMount": True,
                                                "lifeTimeInSec": 7200,
                                                "blrPairId": int(blrid),
                                                "mountPathPairs": [
                                                    {
                                                        "mountPath": restorepath,
                                                        "srcPath": srcvol,
                                                        "srcGuid": srcguid,
                                                        "dstGuid": dstguid
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                }
                            },
                            "commonOpts": {
                                "subscriptionInfo": "<Api_Subscription subscriptionId =\"116\"/>"
                            }
                        }
                    }
                ]
            }
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._services['RESTORE'],
                                                           replicacopyjson)
        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])

                elif "taskId" in response.json():
                    return Schedules(self._commcell_object).get(task_id=response.json()['taskId'])

                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Restore job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Subclient', '102', o_str)
                else:
                    raise SDKException('Subclient', '102', 'Failed to run the restore job')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))


    def delete_replication_pair(self, blrid):
        """"Delete replication pair
        Args:
            blrid   (int)  --  blocklevel replication id.
        """
        flag, response = self._cvpysdk_object.make_request('DELETE', self._services['DELETE_BLR_PAIR']%blrid)

        if response.status_code != 200 and flag == False:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_mount_path_guid(self, volume):
        """
        Gets the mount points for the BLR pairs
        Args:
            volume (str): volume name eg: "E:"
        """
        volume_list = self.get_browse_volume_guid()
        for mount_path in volume_list['mountPathInfo']:
            if mount_path['accessPathList'][0] == volume:
                return mount_path['guid']
        return ''

    def get_recovery_points(self, client_id, subclient_id):
        """ Get all recovery points for the BLR pair from the associated RPStore.
        These recovery points are those to which BLR pairs can failover/permanent mount to
        Args:
            client_id       (int): The ID of the source client machine
            subclient_id    (int): The ID of the subclient associated with the BLR pair

        Returns:
            List of dictionary of recovery points in the format: {'timestamp': 12323, 'dataChangedSize': 1200,
            'sequenceNumber': 898}
        """
        client_name = [key for key, value in self._commcell_object.clients.all_clients.items()
                       if value['id'] == client_id]
        if not client_name:
            raise SDKException(f'Client not found with client id [{client_id}]')
        client = self._commcell_object.clients.get(client_name[0])
        flag, response = self._cvpysdk_object.make_request('GET', self._services['GRANULAR_BLR_POINTS']
                                                           %(client_id, subclient_id, client.client_guid))
        if not flag or response.status_code != 200:
            raise SDKException('Response', '101', self._update_response_(response.text))
        if 'vmScale' not in response.json():
            return []
        return response.json()['vmScale']['restorePoints']


    def create_fsblr_replication_pair(self, srcclientid, destclientid, srcguid, destguid,
                                      rpstoreid=None, replicationtype=None, **replication_options):
        """"
        Create FSBLR continuous replication pair
        Args:
            srcclientid   (int)  --  Source client id

            destclientid   (dict)  -- Destintion client id

            srcguid        (str) -- Browse guid of source volume

            dstguid        (str) -- Browse guid of destination volume

            rpstoreid      (str) -- Rp store id for replication

            replicationtype (int) -- Replication pair  type to create (1 for live, 4 for granular pairs)

            **replication_options (dict) --
            {
                srcvol          (str): Source volume name
                destvol         (str): Destination volume name
                srcclient       (str): Source volume name
                srcclient       (str): Destination volume name
                rpstore         (int): RPStore ID,
                ccrp            (str): Time in minutes for crash consistent recovery point
                arcp            (str): Time in minutes for app consistent recovery point
            }


        """
        srcvol = replication_options.get('srcvol')
        destvol = replication_options.get('destvol')
        destclient = replication_options.get('destclient')
        srcclient = replication_options.get('srcclient')
        rpstore = replication_options.get('rpstore')
        ccrp = replication_options.get('ccrp', "120")
        acrp = replication_options.get('acrp', "180")

        if replicationtype == 4:
            blr_options = f"<?xml version='1.0' encoding='UTF-8'?><BlockReplication_BLRRecoveryOptions recoveryType=\"4\"><granularV2 ccrpInterval=\"{ccrp}\" acrpInterval=\"{acrp}\" maxRpInterval=\"21600\" rpMergeDelay=\"172800\" rpRetention=\"604800\" maxRpStoreOfflineTime=\"0\" useOffPeakSchedule=\"0\" rpStoreId=\"{rpstoreid}\" rpStoreName=\"{rpstore}\"/></BlockReplication_BLRRecoveryOptions>"

        else:
            blr_options = "<?xml version='1.0' encoding='UTF-8'?><BlockReplication_BLRRecoveryOptions recoveryType=\"1\"><granularV2 ccrpInterval=\"300\" acrpInterval=\"0\" maxRpInterval=\"21600\" rpMergeDelay=\"172800\" rpRetention=\"604800\" maxRpStoreOfflineTime=\"0\" useOffPeakSchedule=\"0\"/></BlockReplication_BLRRecoveryOptions>"

        granularjson = {
            "destEndPointType": 2,
            "blrRecoveryOpts": blr_options,
            "srcEndPointType": 2,
            "srcDestVolumeMap": [
                {
                    "sourceVolumeGUID": srcguid,
                    "destVolume": destvol,
                    "destVolumeGUID": destguid,
                    "sourceVolume": srcvol
                }
            ],
            "destEntity": {
                "client": {
                    "clientId": int(destclientid),
                    "clientName": destclient
                }
            },
            "sourceEntity": {
                "client": {
                    "clientId": int(srcclientid),
                    "clientName": srcclient
                }
            }
        }
        flag, response = self._cvpysdk_object.make_request('POST', self._services['CREATE_BLR_PAIR'], granularjson)

        if flag:
            if response and response.json():
                if response.json().get('errorCode', 0) != 0:
                    raise SDKException('Response', '101', self._update_response_(response.text))
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')



    def create_granular_replica_copy(self, srcclientid, destclientid, scid, blrid, srcguid, dstguid, restoreguid,
                                     **replication_options):
        """"setter for granular blklvl Replication replica copy...

        Args:
            srcclientid   (int)  --  Source client id.

            destclientid    (dict)  -- Destintion client id .

            scid           (int) --  Replication Subclient id

            blrid           (int) -- Blr pair id

            srcguid         (str) -- source volume guid

            dstguid         (str) -- Destination relication guid

            restoreguid     (str) -- RP store guid

            timestamp        (int) -- Replication point timestamp

            **replication_options (dict) -- object instance


        """

        replicapoints = self.get_recovery_points(destclientid, scid)
        timestamp = replication_options.get('timestamp')
        if timestamp:
            restore_point = [replica_point for replica_point in replicapoints
                             if int(replica_point['timeStamp']) == timestamp]
        else:
            restore_point = replicapoints[-1]

        srcvol = replication_options.get('srcvol')
        restorepath = replication_options.get('RestorePath')
        replicacopyjson = {
            "taskInfo": {
                "task": {
                    "ownerId": 1,
                    "taskType": 1,
                    "ownerName": "",
                    "initiatedFrom": 1,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 4047
                        },
                        "options": {
                            "backupOpts": {
                                "mediaOpt": {
                                    "auxcopyJobOption": {
                                        "maxNumberOfStreams": 0,
                                        "allCopies": True,
                                        "useMaximumStreams": True,
                                        "useScallableResourceManagement": False
                                    }
                                }
                            },
                            "adminOpts": {
                                "blockOperation": {
                                    "operations": [
                                        {
                                            "appId": int(scid),
                                            "opType": 8,
                                            "dstProxyClientId": int(destclientid),
                                            "fsMountInfo": {
                                                "doLiveMount": False,
                                                "lifeTimeInSec": 7200,
                                                "blrPairId": int(blrid),
                                                "mountPathPairs": [
                                                    {
                                                        "mountPath": restorepath,
                                                        "srcPath": srcvol,
                                                        "srcGuid": dstguid,
                                                        "dstGuid": restoreguid
                                                    }
                                                ],
                                                "rp": {
                                                    "timeStamp": int(restore_point['timeStamp']),
                                                    "sequenceNumber": int(restore_point['sequenceNumber']),
                                                    "rpType": 1,
                                                    "appConsistent": False,
                                                    "dataChangedSize": int(restore_point['dataChangedSize'])
                                                }
                                            }
                                        }
                                    ]
                                }
                            },
                            "commonOpts": {
                                "subscriptionInfo": "<Api_Subscription subscriptionId =\"1451\"/>"
                            }
                        }
                    }
                ]
            }
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._services['RESTORE'], replicacopyjson)

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])

                elif "taskId" in response.json():
                    return Schedules(self._commcell_object).get(task_id=response.json()['taskId'])

                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Restore job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Subclient', '102', o_str)
                else:
                    raise SDKException('Subclient', '102', 'Failed to run the restore job')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))


    def get_browse_volume_guid(self):

        """"to get browse volume guids for client
            Returns:
                vguids (json) : Returns volume guids and properties

        """
        client_id= self._client_object.client_id
        flag, response = self._cvpysdk_object.make_request('GET', self._services['BROWSE_MOUNT_POINTS']
                                                           %(client_id))
        if flag:
            if response and response.json():
                vguids = response.json()
                if response.json().get('errorCode', 0) != 0:
                    raise SDKException('Response', '101', self._update_response_(response.text))
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

        return vguids
