# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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


"""

from __future__ import unicode_literals

from ..backupset import Backupset


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
            fs_options=None):
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

        return self._instance_object._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            fs_options=fs_options
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
            fs_options=None):
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

        return self._instance_object._restore_out_of_place(
            client=client,
            destination_path=destination_path,
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            fs_options=fs_options
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
                                        "backupsetName": "defaultBackupSet"
                                    }, "netconfig": {
                                        "wins": {
                                            "useDhcp": False
                                        }, "firewall": {
                                            "certificatePath": "", "certificateBlob": "",
                                        "configBlob": ""
                                        }, "hosts": [
                                            {
                                                "fqdn": "", "alias": "", "ip": {
                                            }
                                            }
                                        ], "dns": {
                                            "suffix": "", "useDhcp": False
                                    }, "ipinfo": ipconfig
                                }, "platformConfig": {
                                    "platformCfgBlob": "", "win_passPhrase": "",
                                    "win_licenceKey": "", "type": 1,
                                    "goToMiniSetUp": 0, "Win_DomainCreds": {
                                        "isClientInDomain": True, "DomainCreds": {
                                            "password": "", "domainName": "idcprodcert.loc",
                                            "confirmPassword": "",
                                            "userName": ""
                                        }
                                    }
                                }, "firewallLocal": {
                                    "certificatePath": "", "certificateBlob": "", "configBlob": ""
                                }, "client": {
                                    "hostName": " ", "clientName": " ",
                                    "type": 0
                                }, "indexPathCreds": {
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
                            }, "hwconfig": hwconfig
                                           , "netconfig": {
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

                            }, "maInfo": {
                                "clientName": ""
                            }, "datastoreList": {

                            }
                        }, "vmInfo": {
                            "registerWithFailoverCluster": False, "proxyClient": {
                                "clientName": " "
                        }, "vmLocation": {
                            "pathName": " ", "inventoryPath": "",
                            "hostName": " ", "resourcePoolPath": "", "dataCenterName": "",
                            "vCenter": " ", "datastore": {
                                "name": " "
                            }
                        }, "expirationTime": {
                        }
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
                    "applicationId": "33",
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
        return hwconfig, ipconfig

    def run_bmr_restore(self, **restore_options):
        """
        Calling the create task API with the final restore JSON

        Args :
                isopath (String)    : The location of ISO in the datastore

                CS_IP   (String)    : The IP of the CS

                CS_Hostname   (String)    : The hostname of he CS

                CS_Username   (String)    : The username for the Comcell

                CS_Password   (String)     : The password for the comcell

                Datastore   (String)        : The ESX store in which the VM is provisioned

                vCenterServerName   (String)    : The ESX server used

                ClientHostName   (String)    : The hostname of the client being virtualized.

                vmName   (String)    : The name with which the VM is provisioned.

        Returns :
                    returns the task object

        """
        client_name = self._agent_object._client_object.client_name

        self._instance_object._restore_association = self._backupset_association

        hwconfig, ipconfig = self._get_responsefile()
        response_json = self._restore_json(paths=[''])

        restore_json_system_state = self._restore_bmr_admin_json(ipconfig, hwconfig)
        restore_json_virtualserver = self._restore_bmr_virtualserveropts_json()

        response_json['taskInfo']['subTasks'][0]['options'][
            'adminOpts'] = restore_json_system_state

        response_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'virtualServerRstOption'] = restore_json_virtualserver

        vm_option = response_json['taskInfo']['subTasks'][0]['options']['adminOpts'][
            'vmProvisioningOption']['virtualMachineOption'][0]

        vm_option['isoPath'] = restore_options.get('isopath')

        vm_option['oneTouchResponse']['clients'][0]['backupSet'][
            'backupsetName'] = self.backupset_name

        vm_option['oneTouchResponse']['csinfo']['ip'][
            'address'] = restore_options.get('CS_IP')

        vm_option['oneTouchResponse']['csinfo']['commservInfo'][
            'hostName'] = restore_options.get('CS_Hostname', None)

        vm_option['oneTouchResponse']['csinfo']['creds'][
            'password'] = restore_options.get('CS_Password', None)

        vm_option['oneTouchResponse']['csinfo']['creds'][
            'userName'] = restore_options.get('CS_Username', None)

        if 'scsi_disks' in vm_option['oneTouchResponse']['hwconfig']:
            vm_option['oneTouchResponse']['hwconfig']['scsi_disks'][0][
                'dataStoreName'] = restore_options.get('Datastore', None)

        if 'ide_disks' in vm_option['oneTouchResponse']['hwconfig']:
            vm_option['oneTouchResponse']['hwconfig']['ide_disks'][0][
                'dataStoreName'] = restore_options.get('Datastore', None)

        vm_option['vmInfo']['proxyClient'][
            'clientName'] = restore_options.get('vCenterServerName', None)

        vm_option['vmInfo']['vmLocation']['pathName'] = restore_options.get('isopath', None)

        vm_option['vmInfo']['vmLocation']['datastore'][
            'name'] = restore_options.get('Datastore', None)

        response_json['taskInfo']['subTasks'][0]['options'][
            'restoreOptions']['virtualServerRstOption']['diskLevelVMRestoreOption'][
                'esxServerName'] = restore_options.get('vCenterServerName', None)

        response_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination'][
            'destClient']['clientName'] = restore_options.get('vCenterServerName', None)

        vm_option['oneTouchResponse']['clients'][0]['client'][
            'hostName'] = restore_options.get('ClientHostname', None)

        vm_option['oneTouchResponse']['clients'][0]['client'][
            'clientName'] = restore_options.get('ClientName', None)

        vm_option['oneTouchResponse']['clients'][0]['netconfig']['ipinfo']['interfaces'][0][
            'networkLabel'] = "VM Network"

        vm_option['oneTouchResponse']['hwconfig']['vmName'] = restore_options.get('vmName', None)

        vm_option['oneTouchResponse']['hwconfig']['overwriteVm'] = True

        vm_option['vmInfo']['vmLocation']['hostname'] = restore_options.get('vCenterServerName')

        vm_option['vmInfo']['vmLocation']['vCenter'] = restore_options.get('vCenterServerName')

        response_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination'][
            'inPlace'] = False
        response_json['taskInfo']['subTasks'][0]['subTask']['subTaskType'] = 1
        response_json['taskInfo']['subTasks'][0]['subTask']['operationType'] = 4041

        return self._process_restore_response(response_json)
