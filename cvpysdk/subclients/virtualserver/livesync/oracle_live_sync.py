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

"""File for configuring and monitoring live sync on the VMW subclient.

OCILiveSync is the only class defined in this file.

OCILiveSync: Class for configuring and monitoring OCI subclient live sync

OCILiveSync:

    configure_live_sync()     -- To configure live sync from supplied parameters

"""

from .vsa_live_sync import VsaLiveSync
from ....exception import SDKException

class OCILiveSync(VsaLiveSync):
    """Class for configuring and monitoring OCI live sync operations"""
    def configure_live_sync(self,
                            schedule_name=None,
                            destination_client=None,
                            proxy_client=None,
                            copy_precedence=0,
                            vm_to_restore=None,
                            destination_network=None,
                            power_on=True,
                            overwrite=False,
                            distribute_vm_workload=None,
                            datastore=None,
                            restored_vm_name=None,
                            restore_option=None,
                            pattern_dict=None,
                            ):
        """To configure live

        Args:

            schedule_name               (str)   -- Name of the Live sync schedule to be created

            destination_client          (str)   -- OCI Host Client Name where VM needs to be restored

            proxy_client                (str)   -- Name of the proxy client to be used

            copy_precedence             (int)   -- Copy id from which restore needs to be performed
                                                    default: 0

            vm_to_restore               (list)  -- VM's to be restored

            destination_network         (str)   -- Network card name on the destination machine

            power_on                    (bool)  -- To validate destination VM power on and off
                                                    default: True

            overwrite                   (bool)  -- To overwrite VM and VHDs in destination path
                                                    default: False

            distribute_vm_workload      (int)   -- Virtual machines to be used per job

            datastore                   (str)   -- Datastore to restore the VM

            restored_vm_name            (str)   -- Name used for the VM when restored

            restore_option              (dict)  -- Restore options dictionary with advanced options

            pattern_dict                (dict)  -- Dictionary to generate the live sync schedule

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

        if not restored_vm_name:
            restored_vm_name = "LiveSync_"
        restore_option['restore_new_name'] = restored_vm_name

        if copy_precedence:
            restore_option["copy_precedence_applicable"] = True

        if vm_to_restore:
            vm_to_restore = [vm_to_restore]

        if bool(restore_option):
            if not (isinstance(overwrite, bool) and
                    isinstance(power_on, bool)):
                raise SDKException('Subclient', '101')

        # set attr for all the option in restore xml from user inputs
        self._subclient_object._set_restore_inputs(
            restore_option,
            vm_to_restore=self._subclient_object._set_vm_to_restore(vm_to_restore),
            unconditional_overwrite=overwrite,
            power_on=power_on,
            distribute_vm_workload=distribute_vm_workload,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            vcenter_client=destination_client,
            client_name=proxy_client,
            datastore=datastore,
            destination_network=destination_network,
            in_place=False
        )

        return self._configure_live_sync(schedule_name, restore_option, pattern_dict)
