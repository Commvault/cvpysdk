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

"""File for configuring and monitoring live sync on the AzureRM subclient.

AzureLiveSync is the only class defined in this file.
AzureLiveSync: Class for configuring and monitoring Hyper-V subclient live sync

AzureLiveSync:

    generate_restore_options_json()     -- To generate the restore
                                            options json for Hyper-V live sync

"""

from .vsa_live_sync import VsaLiveSync
from ....exception import SDKException


class AzureLiveSync(VsaLiveSync):
    """Class for configuring and monitoring Hyper-V live sync operations"""

    def configure_live_sync(self,
                            schedule_name=None,
                            unconditional_overwrite=None,
                            destination_client=None,
                            power_on=True,
                            copy_precedence=0,
                            resource_group=None,
                            storage_account=None,
                            createpublicip=None,
                            restoreasmanagedvm=None,
                            instancesize=None,
                            restored_vm_name=None,
                            proxy_client=None,
                            restore_option=None,
                            networkdisplayname=None,
                            vm_to_restore=None,
                            pattern_dict=None,
                            region=None,
                            destsubid=None,
                            networkrsg=None
                            ):
        """To configure live

        Args:

            schedule_name               (str)   -- Name of the Live sync schedule to be created

            destination_client          (str)   --  Client Name where
                                                    VM needs to be restored

            proxy_client                (str)   -- Name of the proxy client to be used

            copy_precedence             (int)   -- Copy id from which restore needs to be performed
                                                    default: 0

            vm_to_restore               (list)  -- VM's to be restored


            power_on                    (bool)  -- To validate destination VM power on and off
                                                    default: True

            unconditional_overwrite     (bool)  -- To overwrite VM and disk in destination

            resource_group              (str)  -- Destination Resource Group

            storage_account             (str)  -- storage account to be used for destiantion VM

            restored_vm_name            (str)   -- Name used for the VM when restored

            createpublicip             (bool)  -- To create public IP in destination vm

            datacenter                 (str)   -- region of the destionation VM

            restoreasmanagedvm          (bool)  -- To Restore VM as a maganed VM

            networkdisplayname          (str)   -- Network Display name
                                                    which has used for destination VM

            networkrsg                  (str)   -- Resource group of the Network
                                                    to be used by destination VM

            restore_option              (dict)  -- Restore options
                                                    dictionary with advanced options

            pattern_dict                (dict)  -- Dictionary to generate
                                                    the live sync schedule

            instancesize                (str)   -- instance size of destination vm

            destsubid                   (str)   -- subscription id destination client

            region                       (str)  -- region of the destination VM

            restored_vm_name            (str)   -- Name used for the VM when restored

                Sample:

                    for after_job_completes :
                    {
                        "freq_type": 'after_job_completes',
                        "active_start_date": date_in_%m/%d/%y (str),
                        "active_start_time": time_in_%H/%S (str),
                        "repeat_days": days_to_repeat (int)
                    }

                    for daily:
                    {
                         "freq_type": 'daily',
                         "active_start_time": time_in_%H/%S (str),
                         "repeat_days": days_to_repeat (int)
                    }

                    for weekly:
                    {
                         "freq_type": 'weekly',
                         "active_start_time": time_in_%H/%S (str),
                         "repeat_weeks": weeks_to_repeat (int)
                         "weekdays": list of weekdays ['Monday','Tuesday']
                    }

                    for monthly:
                    {
                         "freq_type": 'monthly',
                         "active_start_time": time_in_%H/%S (str),
                         "repeat_months": weeks_to_repeat (int)
                         "on_day": Day to run schedule (int)
                    }

                    for yearly:
                    {
                         "active_start_time": time_in_%H/%S (str),
                         "on_month": month to run schedule (str) January, Febuary...
                         "on_day": Day to run schedule (int)
                    }

        Returns:
            object - instance of the Schedule class for this Live sync

        """
        # restore options
        if restore_option is None:
            restore_option = {}

        if vm_to_restore and not isinstance(vm_to_restore, str):
            raise SDKException('Subclient', '101')

        if not restored_vm_name and isinstance(vm_to_restore, str):
            restored_vm_name = "LiveSync_"
        restore_option['restore_new_name'] = restored_vm_name

        if copy_precedence:
            restore_option["copy_precedence_applicable"] = True

        if vm_to_restore:
            vm_to_restore = [vm_to_restore]

        # check mandatory input parameters are correct
        if bool(restore_option):
            if not (isinstance(unconditional_overwrite, bool) and
                    isinstance(power_on, bool)):
                raise SDKException('Subclient', '101')

        # set attr for all the option in restore xml from user inputs
        self._subclient_object._set_restore_inputs(
            restore_option,
            vm_to_restore=self._subclient_object._set_vm_to_restore(vm_to_restore),
            vcenter_client=destination_client,
            unconditional_overwrite=unconditional_overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            client_name=proxy_client,
            esx_host=resource_group,
            datastore=storage_account,
            in_place=False,
            networkDisplayName=networkdisplayname,
            datacenter=region,
            restoreAsManagedVM=restoreasmanagedvm,
            instanceSize=instancesize,
            createPublicIP=createpublicip,
            destsubid=destsubid,
            networkrsg=networkrsg
            )

        return self._configure_live_sync(schedule_name, restore_option, pattern_dict)
