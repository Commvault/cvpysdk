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
from typing import List, Optional, Dict, Any, Union, Tuple

class FSBackupset(Backupset):
    """
    Represents a file system (FS) backupset, derived from the Backupset base class.

    This class provides comprehensive management and operational capabilities for file system backupsets,
    including restore operations, version management, replication, and advanced configuration options.
    It is designed to facilitate both in-place and out-of-place restores, support for BMR (Bare Metal Restore),
    Azure-specific advanced restore options, and granular control over index server and pruning settings.

    Key Features:
        - In-place and out-of-place restore operations with advanced options
        - Find and manage all backup versions
        - Bare Metal Restore (BMR) support with administrative, virtual server, firewall, and AIX-specific options
        - Azure advanced restore and configuration options
        - Response file generation and login detail retrieval
        - Index server management and pruning configuration (type, days, cycles)
        - Replica copy creation and granular replica copy management
        - Replication pair creation and deletion for FSBLR and granular scenarios
        - Mount path GUID and browse volume GUID retrieval
        - Recovery point management for clients and subclients

    This class is intended for use in environments requiring robust file system backupset management,
    advanced restore capabilities, and flexible replication and recovery options.

    #ai-gen-doc
    """

    def restore_in_place(
            self,
            paths: List[str],
            overwrite: bool = True,
            restore_data_and_acl: bool = True,
            copy_precedence: Optional[int] = None,
            from_time: Optional[str] = None,
            to_time: Optional[str] = None,
            fs_options: Optional[Dict[str, Any]] = None,
            restore_jobs: Optional[List[Any]] = None,
            advanced_options: Optional[Dict[str, Any]] = None
        ):
        """Restore files or folders in-place to their original locations.

        This method restores the specified files or folders to their original locations on the client.
        You can customize the restore operation using various options such as overwrite behavior,
        restoring ACLs, copy precedence, time filters, advanced file system options, and job-specific settings.

        Args:
            paths: List of full file or folder paths to restore.
            overwrite: If True, unconditionally overwrite existing files during restore. Default is True.
            restore_data_and_acl: If True, restore both data and ACLs. Default is True.
            copy_precedence: Optional copy precedence value for the storage policy copy.
            from_time: Optional string specifying the start time for restore (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Optional string specifying the end time for restore (format: 'YYYY-MM-DD HH:MM:SS').
            fs_options: Optional dictionary of advanced file system restore options.
                Supported keys include:
                    - all_versions (bool): Restore all versions of the specified file.
                    - versions (List[int]): List of version numbers to restore.
                    - validate_only (bool): Validate data backed up for restore.
                    - no_of_streams (int): Number of streams to use for restore.
            restore_jobs: Optional list of job IDs for index-free restore.
            advanced_options: Optional dictionary of advanced restore options.
                Supported keys include:
                    - job_description (str): Description for the restore job.
                    - timezone (str): Timezone to use for restore (refer to TIMEZONES in constants.py).

        Returns:
            Job: Instance of the Job class representing the restore job.

        Raises:
            SDKException: If 'paths' is not a list, if job initialization fails, or if the restore response is empty or unsuccessful.

        Example:
            >>> backupset = FSBackupset(...)
            >>> restore_job = backupset.restore_in_place(
            ...     paths=['/data/file1.txt', '/data/folder2'],
            ...     overwrite=True,
            ...     fs_options={'all_versions': True, 'no_of_streams': 2},
            ...     advanced_options={'job_description': 'Restore critical files', 'timezone': 'UTC'}
            ... )
            >>> print(f"Restore job started: {restore_job}")

        #ai-gen-doc
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
            client: Union[str, 'Client'],
            destination_path: str,
            paths: List[str],
            overwrite: bool = True,
            restore_data_and_acl: bool = True,
            copy_precedence: Optional[int] = None,
            from_time: Optional[str] = None,
            to_time: Optional[str] = None,
            fs_options: Optional[Dict[str, Any]] = None,
            restore_jobs: Optional[List[Any]] = None,
            advanced_options: Optional[Dict[str, Any]] = None
        ):
        """Restore files or folders out-of-place to a specified client and destination path.

        This method restores the files and folders listed in `paths` to the given `client` at the
        specified `destination_path`. Advanced restore options can be provided via `fs_options` and
        `advanced_options`.

        Args:
            client: Either the name of the client as a string or an instance of the Client class.
            destination_path: Full path to the restore location on the target client.
            paths: List of full file or folder paths to restore.
            overwrite: If True, files at the destination will be overwritten unconditionally.
            restore_data_and_acl: If True, both data and ACL files will be restored.
            copy_precedence: Optional copy precedence value for the storage policy copy.
            from_time: Optional start time for restore (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Optional end time for restore (format: 'YYYY-MM-DD HH:MM:SS').
            fs_options: Optional dictionary of advanced file system restore options.
                Example options:
                    - preserve_level: Level of folder structure to preserve.
                    - proxy_client: Proxy client to use for restore.
                    - impersonate_user: User to impersonate during restore.
                    - impersonate_password: Base64-encoded password for impersonation.
                    - all_versions: If True, restores all versions of specified files.
                    - versions: List of version numbers to restore.
                    - validate_only: If True, validates data for restore without actual restore.
                    - no_of_streams: Number of streams to use for restore.
            restore_jobs: Optional list of job IDs for index-free restore.
            advanced_options: Optional dictionary of advanced restore options.
                Example options:
                    - job_description: Description for the restore job.
                    - timezone: Timezone to use for restore (refer to TIMEZONES dict in constants.py).

        Returns:
            Instance of the Job class representing the restore job.

        Raises:
            SDKException: If input parameters are invalid or restore initialization fails.

        Example:
            >>> # Restore files to a different client and location
            >>> paths_to_restore = ['/data/file1.txt', '/data/folder2']
            >>> fs_options = {'preserve_level': 2, 'all_versions': True}
            >>> advanced_options = {'job_description': 'Restore for audit', 'timezone': 'UTC'}
            >>> job = backupset.restore_out_of_place(
            ...     client='TargetClient01',
            ...     destination_path='/restore/location',
            ...     paths=paths_to_restore,
            ...     overwrite=True,
            ...     fs_options=fs_options,
            ...     advanced_options=advanced_options
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
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

    def find_all_versions(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Search the content of a Subclient and retrieve all available versions for the specified content.

        This method allows you to search for all versions of a file or folder within a subclient. 
        You can specify browse options either as a single dictionary argument or as keyword arguments.
        Supported options include 'path', 'show_deleted', 'from_time', 'to_time', and others as defined in self._default_browse_options.

        Args:
            *args: Optional positional argument containing a dictionary of browse options.
            **kwargs: Optional keyword arguments specifying browse options directly.
                Common options:
                    - path (str): Path to the file or folder to search.
                    - show_deleted (bool): Whether to include deleted items.
                    - from_time (str): Start time for version search (format: 'YYYY-MM-DD HH:MM:SS').
                    - to_time (str): End time for version search (format: 'YYYY-MM-DD HH:MM:SS').
                Refer to self._default_browse_options for all supported options.

        Returns:
            Dictionary containing the specified file or folder with a list of all available versions and additional metadata.

        Example:
            >>> # Using a dictionary of browse options
            >>> versions = backupset.find_all_versions({
            ...     'path': 'c:\\hello',
            ...     'show_deleted': True,
            ...     'from_time': '2014-04-20 12:00:00',
            ...     'to_time': '2016-04-31 12:00:00'
            ... })
            >>> print(versions)
            >>> 
            >>> # Using keyword arguments
            >>> versions = backupset.find_all_versions(
            ...     path='c:\\hello.txt',
            ...     show_deleted=True,
            ...     to_time='2016-04-31 12:00:00'
            ... )
            >>> print(versions)

        #ai-gen-doc
        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['operation'] = 'all_versions'

        return self._do_browse(options)

    def _restore_bmr_admin_json(self, ipconfig: Dict[str, Any], hwconfig: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the JSON structure required for BMR (Bare Metal Restore) 1-Touch restore.

        This method constructs and returns the JSON payload containing BMR options, 
        using the provided IP configuration and hardware configuration details. 
        The resulting JSON can be used for 1-Touch restore operations.

        Args:
            ipconfig: Dictionary containing IP configuration details obtained from the response file.
            hwconfig: Dictionary containing hardware configuration details obtained from the response file.

        Returns:
            Dictionary representing the JSON structure required for BMR restore.

        Example:
            >>> ipconfig = {'ip': '192.168.1.100', 'subnet': '255.255.255.0'}
            >>> hwconfig = {'cpu': 'Intel Xeon', 'ram': '16GB'}
            >>> fs_backupset = FSBackupset(...)
            >>> bmr_json = fs_backupset._restore_bmr_admin_json(ipconfig, hwconfig)
            >>> print(bmr_json)
            # The returned dictionary can be used for BMR 1-Touch restore operations

        #ai-gen-doc
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
                                            "goToMiniSetUp": 1, "Win_DomainCreds":
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

    def _restore_bmr_virtualserveropts_json(self) -> Dict[str, Any]:
        """Generate the JSON structure for virtual server options used in Virtualize Me restores.

        Returns:
            Dictionary containing the virtual server options JSON required for BMR (Bare Metal Restore) operations.

        Example:
            >>> fs_backupset = FSBackupset(...)
            >>> options_json = fs_backupset._restore_bmr_virtualserveropts_json()
            >>> print(options_json)
            >>> # The returned dictionary can be used to configure Virtualize Me restore requests

        #ai-gen-doc
        """
        bmr_restore_json = {
            "diskLevelVMRestoreOption": {
                "esxServerName": " ", "userPassword": {

                }
            }
        }
        return bmr_restore_json

    def _restore_bmr_firewallopts_json(self, hostname: str, direction: int, port: int) -> Dict[str, Any]:
        """Generate the JSON structure for BMR firewall configuration options.

        Args:
            hostname: The hostname of the machine for which firewall options are being configured.
            direction: The direction of the connection (as an integer).
            port: The port number used for communication.

        Returns:
            Dictionary containing the firewall configuration options required for Virtualize Me restores.

        Example:
            >>> fs_backupset = FSBackupset(...)
            >>> firewall_json = fs_backupset._restore_bmr_firewallopts_json('server01', 1, 8080)
            >>> print(firewall_json)
            {'direction': 1, 'connectionInfoList': [{'hostname': 'server01', 'port': 8080}]}

        #ai-gen-doc
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

    def _azure_advancedrestoreopts_json(self) -> List[Dict[str, Any]]:
        """Generate the JSON structure for advanced Azure restore options.

        This method returns the default advanced restore options required for "Virtualize Me" restores to Azure.
        The returned JSON includes VM size and security group configuration.

        Returns:
            List of dictionaries representing the advanced restore options for Azure restores.

        Example:
            >>> fs_backupset = FSBackupset(...)
            >>> azure_opts = fs_backupset._azure_advancedrestoreopts_json()
            >>> print(azure_opts)
            [{'vmSize': '', 'securityGroups': [{'groupName': '--Auto Select--', 'groupId': ''}]}]

        #ai-gen-doc
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

    def _azure_advancedopts_json(self) -> Dict[str, Any]:
        """Generate the advanced restore options JSON for Azure restores.

        This method constructs and returns the JSON structure required for 
        advanced restore operations when using the "Virtualize Me" feature to restore to Azure.

        Returns:
            Dictionary containing the advanced restore options for Azure, 
            including network card and subnet configuration.

        Example:
            >>> fs_backupset = FSBackupset(...)
            >>> azure_options = fs_backupset._azure_advancedopts_json()
            >>> print(azure_options)
            >>> # Use the returned JSON for Virtualize Me to Azure restore operations

        #ai-gen-doc
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


    def _get_responsefile(self) -> Tuple[Dict[str, Any], Dict[str, Any], str, str, str]:
        """Retrieve the response file details for the backupset.

        This method obtains hardware configuration, IP configuration, and credential details 
        from the response file associated with the backupset.

        Returns:
            A tuple containing:
                - hwconfig (dict): Hardware configuration details.
                - ipconfig (dict): IP configuration details for the client.
                - cs_user (str): User name for CommServe credentials.
                - cs_pwd (str): Password for CommServe credentials.
                - cs_token (str): Token extracted from the CommServe password.

        Example:
            >>> hwconfig, ipconfig, cs_user, cs_pwd, cs_token = backupset._get_responsefile()
            >>> print("Hardware config:", hwconfig)
            >>> print("IP config:", ipconfig)
            >>> print("CommServe user:", cs_user)
            >>> print("CommServe password:", cs_pwd)
            >>> print("CommServe token:", cs_token)
        #ai-gen-doc
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

    def run_bmr_restore(self, **restore_options: Any):
        """Run a Bare Metal Recovery (BMR) restore task using the provided options.

        This method initiates a BMR restore by constructing and submitting a restore task
        with the specified parameters. The restore can be performed for VMware, Hyper-V, Azure,
        or Azure Stack environments, depending on the options provided.

        Common restore options include:
            IsoPath: The location of the ISO file in the datastore.
            CommServIP: The IP address of the CommServe server.
            CommServHostname: The hostname of the CommServe server.
            CommServUsername: The username for the Commcell.
            CommServPassword: The password for the Commcell.
            Datastore: The ESX datastore where the VM is provisioned.
            VcenterServerName: The vCenter server to use.
            ClientHostname: The hostname of the client being virtualized.
            VmName: The name to assign to the provisioned VM.
            VirtualizationClient: The VMware virtualization client name.
            EsxServer: The ESX server name.
            NetworkLabel: The network label to assign to the VM.
            HyperVHost: The Hyper-V host name.
            GuestUser: The username for the guest OS.
            GuestPassword: The password for the guest OS.
            CloneClientName: The name of the clone client.
            OsType: The operating system type (e.g., 'UNIX').
            UseDhcp: Whether to use DHCP for network configuration.
            FirewallClientGroup: The firewall client group name.
            FirewallHostname: The firewall hostname.
            FirewallDirection: The firewall direction.
            FirewallPort: The firewall port.
            CreatePublicIP: Whether to create a public IP (Azure only).
            ResourceGroup: The Azure resource group name.
            StorageAccount: The Azure storage account name.
            ManagementURL: The Azure Stack management URL.

        Args:
            **restore_options: Arbitrary keyword arguments specifying restore parameters.
                See above for commonly used options.

        Returns:
            The task object representing the submitted restore job.

        Example:
            >>> backupset = FSBackupset(...)
            >>> task = backupset.run_bmr_restore(
            ...     IsoPath="/datastore/iso/bmr.iso",
            ...     CommServIP="192.168.1.10",
            ...     CommServHostname="commserv01",
            ...     CommServUsername="admin",
            ...     CommServPassword="password",
            ...     Datastore="VM_Datastore",
            ...     VcenterServerName="vcenter01",
            ...     ClientHostname="client01",
            ...     VmName="RestoredVM",
            ...     VirtualizationClient="vmware_client",
            ...     EsxServer="esx01",
            ...     NetworkLabel="VM Network",
            ...     HyperVHost="hyperv01",
            ...     GuestUser="guestuser",
            ...     GuestPassword="guestpass",
            ...     CloneClientName="clone01",
            ...     OsType="UNIX",
            ...     UseDhcp=True
            ... )
            >>> print(f"Restore task submitted: {task}")

        #ai-gen-doc
        """
        client_name = self._agent_object._client_object.client_name

        self._instance_object._restore_association = self._backupset_association

        hwconfig, ipconfig, cs_username, cs_password, cs_token = self._get_responsefile()
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

        restore_json_system_state["vmProvisioningOption"]["virtualMachineOption"][0]["oneTouchResponse"]["clients"][0]["backupSet"] = response_json["taskInfo"]["associations"][0]

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

    def _get_cs_login_details(self) -> Tuple[str, str, str, str, str, str]:
        """Retrieve CommServe login details for the current backupset.

        This method gathers essential CommServe authentication and connection information,
        including CommServe name, hostname, IP address, username, password, and token.

        Returns:
            Tuple containing:
                - CommServe name (str)
                - CommServe hostname (str)
                - CommServe IP address (str)
                - CommServe username (str)
                - CommServe password/token (str)
                - CommServe authentication token (str)

        Example:
            >>> cs_details = backupset._get_cs_login_details()
            >>> cs_name, cs_hostname, cs_ip, cs_user, cs_pwd, cs_token = cs_details
            >>> print(f"CommServe Hostname: {cs_hostname}, User: {cs_user}")

        #ai-gen-doc
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

    def _restore_aix_1touch_admin_json(self) -> Dict[str, Any]:
        """Generate the JSON configuration required for AIX 1-Touch BMR restore.

        This method constructs and returns a dictionary containing all necessary 
        options and parameters for performing a 1-Touch restore on AIX systems. 
        The returned JSON includes settings for volume groups, client reboot, 
        network configuration, hardware configuration, and other BMR-specific options.

        Returns:
            Dictionary containing the BMR options and configuration required for AIX 1-Touch restore.

        Example:
            >>> fs_backupset = FSBackupset(...)
            >>> bmr_json = fs_backupset._restore_aix_1touch_admin_json()
            >>> print(bmr_json)
            >>> # Use the returned JSON for initiating a 1-Touch restore operation

        #ai-gen-doc
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

    def run_bmr_aix_restore(self, **restore_options: Any):
        """Run a Bare Metal Recovery (BMR) restore for an AIX system using provided options.

        This method initiates a BMR restore operation for an AIX client by constructing the required restore JSON 
        and calling the create task API. The restore options should be provided as keyword arguments to customize 
        the restore process, such as network configuration, clone settings, and Commcell credentials.

        Common restore options include:
            - clone_client_name (str): Name of the clone machine.
            - clone_client_hostname (str): Hostname of the clone machine.
            - dns_suffix (str): DNS suffix for the client.
            - dns_ip (int): IP address of the DNS server.
            - clone_ip_address (int): IP address for the clone machine.
            - clone_machine_netmask (int): Netmask for the clone machine.
            - clone_machine_gateway (int): Gateway IP for the clone machine.
            - automaticClientReboot (bool): Whether to automatically reboot the client after restore.
            - clone (bool): Whether clone is enabled.
            - CS_Username (str): Username for the Commcell.
            - CS_Password (str): Password for the Commcell.
            - onetouch_server (str): Name of the OneTouch server.
            - onetouch_server_directory (str): Directory path on the OneTouch server.
            - restoreFromBackupBeforeDate (bool): Restore from backup before a specific date.
            - onetouch_backup_jobid (int): Job ID of the backup to restore from.
            - run_FS_restore (bool): Whether to skip restore if files exist.

        Returns:
            The task object representing the restore operation.

        Example:
            >>> backupset = FSBackupset(...)
            >>> task = backupset.run_bmr_aix_restore(
            ...     clone_client_name="AIXClone01",
            ...     clone_client_hostname="aixclone01.example.com",
            ...     dns_suffix="example.com",
            ...     dns_ip=192168110,
            ...     clone_ip_address=192168120,
            ...     clone_machine_netmask=2552552550,
            ...     clone_machine_gateway=19216811,
            ...     automaticClientReboot=True,
            ...     clone=True,
            ...     CS_Username="admin",
            ...     CS_Password="password",
            ...     onetouch_server="OneTouchServer01",
            ...     onetouch_server_directory="/restore/dir",
            ...     restoreFromBackupBeforeDate=True,
            ...     onetouch_backup_jobid=123456
            ... )
            >>> print(f"Restore task created: {task}")

        #ai-gen-doc
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
    def index_server(self) -> Optional['Client']:
        """Get the index server client configured for this backupset.

        Returns:
            Client instance representing the index server if set, otherwise None.

        Example:
            >>> backupset = FSBackupset(commcell_object, ...)
            >>> index_server_client = backupset.index_server  # Use dot notation for property
            >>> if index_server_client:
            ...     print(f"Index server client name: {index_server_client.client_name}")
            ... else:
            ...     print("No index server client is configured for this backupset.")

        #ai-gen-doc
        """

        client_name = None

        if 'indexSettings' in self._properties:
            if 'currentIndexServer' in self._properties['indexSettings']:
                client_name = self._properties['indexSettings']['currentIndexServer']['clientName']

        if client_name is not None:
            return Client(self._commcell_object, client_name=client_name)

        return None

    @index_server.setter
    def index_server(self, value: 'Client') -> None:
        """Set the index server client for the backupset.

        This property setter assigns a Client object as the index server for the backupset.
        The provided client must be a qualified index server client.

        Args:
            value: Client object representing the index server to assign.

        Raises:
            SDKException: If the provided client is not a valid Client object,
                or if the client is not a qualified index server.

        Example:
            >>> index_server_client = Client(...)
            >>> backupset = FSBackupset(...)
            >>> backupset.index_server = index_server_client  # Use assignment for property setters
            >>> # The index server for the backupset is now set

        #ai-gen-doc
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
    def index_pruning_type(self) -> str:
        """Get the index pruning type configured for this backupset.

        Returns:
            The index pruning type as a string.

        Example:
            >>> backupset = FSBackupset(...)
            >>> pruning_type = backupset.index_pruning_type  # Use dot notation for properties
            >>> print(f"Index pruning type: {pruning_type}")

        #ai-gen-doc
        """
        return self._properties["indexSettings"]["indexPruningType"]

    @property
    def index_pruning_days_retention(self) -> int:
        """Get the number of days for which index data is retained by index pruning for this backupset.

        Returns:
            The number of days index data is maintained before pruning, as an integer.

        Example:
            >>> backupset = FSBackupset(...)
            >>> retention_days = backupset.index_pruning_days_retention  # Use dot notation for property
            >>> print(f"Index pruning retention: {retention_days} days")
            >>> # This value determines how long index data is kept before being pruned

        #ai-gen-doc
        """

        return self._properties["indexSettings"]["indexRetDays"]

    @property
    def index_pruning_cycles_retention(self) -> int:
        """Get the number of index pruning cycles retained for this backupset.

        This property returns the configured number of cycles that are maintained in the index 
        by index pruning for the backupset. Index pruning helps manage storage and performance 
        by retaining only a specified number of index cycles.

        Returns:
            The number of index pruning cycles retained as an integer.

        Example:
            >>> backupset = FSBackupset(...)
            >>> cycles_retained = backupset.index_pruning_cycles_retention  # Use dot notation for property
            >>> print(f"Index pruning cycles retained: {cycles_retained}")
            >>> # This value indicates how many index cycles are kept for the backupset

        #ai-gen-doc
        """

        return self._properties["indexSettings"]["indexRetCycles"]

    @index_pruning_type.setter
    def index_pruning_type(self, value: str) -> None:
        """Set the index pruning type for the backupset when backupset-level indexing is enabled.

        This property setter allows you to configure index retention based on either days, cycles, or infinite retention.
        Supported values are:
            - "days_based": Sets index retention based on the number of days.
            - "cycles_based": Sets index retention based on the number of cycles.
            - "infinite": Disables pruning, retaining indexes indefinitely.

        Args:
            value: Pruning type as a string. Must be one of "days_based", "cycles_based", or "infinite".

        Raises:
            SDKException: If an invalid pruning type is provided.

        Example:
            >>> backupset = FSBackupset(...)
            >>> backupset.index_pruning_type = "days_based"    # Set retention by days
            >>> backupset.index_pruning_type = "cycles_based"  # Set retention by cycles
            >>> backupset.index_pruning_type = "infinite"      # Disable pruning

        #ai-gen-doc
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
    def index_pruning_days_retention(self, value: int) -> None:
        """Set the index pruning retention period in days for the backupset.

        This property setter configures the number of days to retain index data at the backupset level,
        enabling days-based index pruning. The value must be an integer greater than or equal to 2.

        Args:
            value: Number of days to retain index data. Must be at least 2.

        Raises:
            SDKException: If the provided value is less than 2 or not an integer.

        Example:
            >>> backupset = FSBackupset(...)
            >>> backupset.index_pruning_days_retention = 7  # Set retention to 7 days
            >>> # Index pruning will now retain data for 7 days

        #ai-gen-doc
        """

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
    def index_pruning_cycles_retention(self, value: int) -> None:
        """Set the index pruning cycles retention value for cycles-based index pruning at the backupset level.

        The value must be an integer greater than or equal to 2. This property controls how many index cycles are retained for the backupset.

        Args:
            value: Number of index cycles to retain (must be >= 2).

        Raises:
            SDKException: If the value is not an integer or is less than 2.

        Example:
            >>> backupset = FSBackupset(...)
            >>> backupset.index_pruning_cycles_retention = 5  # Sets retention to 5 cycles
            >>> # If value is less than 2, an SDKException will be raised

        #ai-gen-doc
        """

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


    def create_replica_copy(
        self,
        srcclientid: int,
        destclientid: int,
        scid: int,
        blrid: int,
        srcguid: str,
        dstguid: str,
        **replication_options: Any
    ):
        """Create a live block-level replication replica copy.

        This method initiates a replica copy operation between a source and destination client
        using block-level replication. Additional replication options can be provided as keyword arguments.

        Args:
            srcclientid: Source client ID as an integer.
            destclientid: Destination client ID as an integer.
            scid: Replication subclient ID as an integer.
            blrid: Block-level replication pair ID as an integer.
            srcguid: Browse GUID of the source volume as a string.
            dstguid: Browse GUID of the destination volume as a string.
            **replication_options: Additional replication options such as 'srcvol' (source volume path)
                and 'RestorePath' (destination restore path).

        Returns:
            Job or Schedules object representing the initiated replica copy operation.

        Raises:
            SDKException: If the replica copy operation fails or returns an error response.

        Example:
            >>> fs_backupset = FSBackupset(...)
            >>> job = fs_backupset.create_replica_copy(
            ...     srcclientid=101,
            ...     destclientid=202,
            ...     scid=301,
            ...     blrid=401,
            ...     srcguid="SRC-GUID-123",
            ...     dstguid="DST-GUID-456",
            ...     srcvol="/mnt/source",
            ...     RestorePath="/mnt/destination"
            ... )
            >>> print(f"Replica copy job started: {job}")
        #ai-gen-doc
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


    def delete_replication_pair(self, blrid: int) -> None:
        """Delete a block-level replication pair by its ID.

        Args:
            blrid: The block-level replication ID to delete.

        Raises:
            SDKException: If the deletion request fails or the response is invalid.

        Example:
            >>> backupset = FSBackupset(...)
            >>> backupset.delete_replication_pair(12345)
            >>> print("Replication pair deleted successfully")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('DELETE', self._services['DELETE_BLR_PAIR']%blrid)

        if response.status_code != 200 and flag == False:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_mount_path_guid(self, volume: str) -> str:
        """Retrieve the GUID for the specified mount path volume.

        This method searches through the available mount points and returns the GUID
        associated with the given volume name (e.g., "E:"). If the volume is not found,
        an empty string is returned.

        Args:
            volume: The name of the volume to search for (e.g., "E:").

        Returns:
            The GUID string corresponding to the specified volume, or an empty string if not found.

        Example:
            >>> backupset = FSBackupset(...)
            >>> guid = backupset.get_mount_path_guid("E:")
            >>> print(f"Mount path GUID for E:: {guid}")
            >>> # If the volume does not exist, guid will be an empty string

        #ai-gen-doc
        """
        volume_list = self.get_browse_volume_guid()
        for mount_path in volume_list['mountPathInfo']:
            if mount_path['accessPathList'][0] == volume:
                return mount_path['guid']
        return ''

    def get_recovery_points(self, client_id: int, subclient_id: int) -> List[Dict[str, Any]]:
        """Retrieve all recovery points for the BLR pair from the associated RPStore.

        These recovery points represent the points to which BLR pairs can failover or be permanently mounted.

        Args:
            client_id: The ID of the source client machine as an integer.
            subclient_id: The ID of the subclient associated with the BLR pair as an integer.

        Returns:
            A list of dictionaries, each representing a recovery point with keys:
                - 'timestamp': The recovery point timestamp.
                - 'dataChangedSize': The size of data changed at this point.
                - 'sequenceNumber': The sequence number of the recovery point.

        Example:
            >>> fs_backupset = FSBackupset(...)
            >>> recovery_points = fs_backupset.get_recovery_points(101, 202)
            >>> for rp in recovery_points:
            ...     print(f"Timestamp: {rp['timestamp']}, Data Changed: {rp['dataChangedSize']}, Sequence: {rp['sequenceNumber']}")
            >>> # Use the returned recovery points for failover or permanent mount operations

        #ai-gen-doc
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


    def create_fsblr_replication_pair(
        self,
        srcclientid: int,
        destclientid: int,
        srcguid: str,
        destguid: str,
        rpstoreid: Optional[str] = None,
        replicationtype: Optional[int] = None,
        **replication_options: Any
    ) -> None:
        """Create a FSBLR continuous replication pair between source and destination clients.

        This method sets up a continuous replication pair for file system block-level replication (FSBLR)
        between the specified source and destination clients and volumes. Additional replication options
        can be provided via keyword arguments to customize the replication behavior.

        Args:
            srcclientid: Source client ID as an integer.
            destclientid: Destination client ID as an integer.
            srcguid: GUID of the source volume as a string.
            destguid: GUID of the destination volume as a string.
            rpstoreid: Optional RP store ID for replication as a string.
            replicationtype: Optional replication pair type (1 for live, 4 for granular pairs).
            **replication_options: Additional replication options such as:
                - srcvol (str): Source volume name.
                - destvol (str): Destination volume name.
                - srcclient (str): Source client name.
                - destclient (str): Destination client name.
                - rpstore (int): RPStore ID.
                - ccrp (str): Crash consistent recovery point interval in minutes.
                - acrp (str): App consistent recovery point interval in minutes.

        Raises:
            SDKException: If the replication pair creation fails or the response contains an error.

        Example:
            >>> fs_backupset = FSBackupset(...)
            >>> fs_backupset.create_fsblr_replication_pair(
            ...     srcclientid=101,
            ...     destclientid=202,
            ...     srcguid="SRC-GUID-123",
            ...     destguid="DEST-GUID-456",
            ...     rpstoreid="RPSTORE-789",
            ...     replicationtype=4,
            ...     srcvol="C:\\",
            ...     destvol="D:\\",
            ...     srcclient="SourceClient",
            ...     destclient="DestinationClient",
            ...     rpstore=789,
            ...     ccrp="120",
            ...     acrp="180"
            ... )
            >>> print("FSBLR replication pair created successfully")
        #ai-gen-doc
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



    def create_granular_replica_copy(
        self,
        srcclientid: int,
        destclientid: int,
        scid: int,
        blrid: int,
        srcguid: str,
        dstguid: str,
        restoreguid: str,
        **replication_options: Any
    ):
        """Create a granular block-level replication replica copy.

        This method initiates a granular replica copy operation between source and destination clients
        using block-level replication. It allows specifying various replication options such as
        timestamp, source volume, and restore path.

        Args:
            srcclientid: Source client ID as an integer.
            destclientid: Destination client ID as an integer.
            scid: Replication subclient ID as an integer.
            blrid: Block-level replication pair ID as an integer.
            srcguid: Source volume GUID as a string.
            dstguid: Destination replication GUID as a string.
            restoreguid: Restore point store GUID as a string.
            **replication_options: Additional replication options such as:
                - timestamp (int): Replication point timestamp.
                - srcvol (str): Source volume path.
                - RestorePath (str): Path to restore the replica copy.

        Returns:
            Job or Schedules: Returns a Job object if a job is created, or a Schedules object if a scheduled task is created.

        Raises:
            SDKException: If the restore job fails or the response is invalid.

        Example:
            >>> fs_backupset = FSBackupset(...)
            >>> job = fs_backupset.create_granular_replica_copy(
            ...     srcclientid=101,
            ...     destclientid=202,
            ...     scid=301,
            ...     blrid=401,
            ...     srcguid="SRC-GUID-123",
            ...     dstguid="DST-GUID-456",
            ...     restoreguid="RESTORE-GUID-789",
            ...     timestamp=1650000000,
            ...     srcvol="/mnt/source",
            ...     RestorePath="/mnt/restore"
            ... )
            >>> print(f"Replica copy job created: {job}")
        #ai-gen-doc
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


    def get_browse_volume_guid(self) -> Dict[str, Any]:
        """Retrieve the volume GUIDs and their properties for the associated client.

        This method sends a request to the Commcell to obtain the browse volume GUIDs for the client
        linked to this FSBackupset instance. The returned data includes GUIDs and related properties
        in a dictionary format.

        Returns:
            Dictionary containing volume GUIDs and their properties.

        Raises:
            SDKException: If the response from the Commcell is invalid or contains an error code.

        Example:
            >>> fs_backupset = FSBackupset(...)
            >>> volume_guids = fs_backupset.get_browse_volume_guid()
            >>> print(volume_guids)
            >>> # Access specific GUIDs and their properties as needed

        #ai-gen-doc
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
