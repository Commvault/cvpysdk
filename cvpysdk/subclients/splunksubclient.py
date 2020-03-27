# -*- coding: utf-8 -*-
# pylint: disable=R1705, R0205

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

"""
Module for operating with splunk subclient

SplunkSubClient is the only class defined in this file

SplunkSubClient:    Derived class from BigDataAppsSubclient Base class, representing
splunk subclient, and to perform operations on that subclient

SplunkSubclient:
===============

splunk_restore()            --      performs a restore job by taking index name as
the argument

subclient_content()     --      sets backup content at subclient level

"""
from cvpysdk.subclients.bigdataappssubclient import BigDataAppsSubclient

class SplunkSubclient(BigDataAppsSubclient):
    """
    Derived class from BigDataAppsSubclient, representing splunk subclient,
    and to perform operations on that subclient
    """

    def restore_in_place(self, index_list):
        """
        Performs a restore job on the splunk subclient

        Args:
            index_list  (list)       --  list containing the indexes to be restored
            Example: ["index1",index2"]

        Returns:
            job_obj     (obj)       --  job object associated with the restore job

        """

        subclient_properties = self.properties["subClientEntity"]
        subclient_id = int(self.subclient_id)
        backupset_id = int(subclient_properties["backupsetId"])

        for count, ele in enumerate(index_list):
            index_list[count] = "/Indexes/" + ele

        instance_obj = self._instance_object

        instance_obj._restore_association = self._subClientEntity

        parameter_dict = self._restore_json(paths=index_list)
        parameter_dict["taskInfo"]["associations"] \
            [0]["subclientId"] = subclient_id
        parameter_dict["taskInfo"]["associations"] \
            [0]["backupsetId"] = backupset_id
        parameter_dict["taskInfo"]["subTasks"][0]["options"] \
            ["restoreOptions"]["browseOption"]["backupset"]["backupsetId"] = backupset_id

        return self._process_restore_response(parameter_dict)

    @property
    def subclient_content(self):
        """
        Returns the appropriate content associated with the subclient

        Returns:
            index_list  (list)  -- list of subclient content
        """

        subclient_prop = self.properties
        index_list = []
        content_list = subclient_prop["splunkProps"]["contentList"]

        for content in content_list:
            index_list.append(content["title"])

        return index_list

    @subclient_content.setter
    def subclient_content(self, index_list):
        """
        Sets content of subclient entity

        Args:
             index_list (list)  --  list of the indexes to be backed up
             Example:["index1","index2"]

        Returns:
            Nothing

        """

        subclient_prop = self.properties
        index_list_copy = list(index_list)
        content_prop_dict = {
            "path": "indexes/" + index_list_copy[0],
            "level": 1,
            "type": 1,
            "title": index_list_copy[0]
        }
        subclient_prop["splunkProps"]["contentList"][0] = content_prop_dict
        del index_list_copy[0]
        for index in index_list_copy:
            content_prop_dict = {
                "path": "indexes/" + index,
                "level": 1,
                "type": 1,
                "title": index
            }
            subclient_prop["splunkProps"]["contentList"].append(content_prop_dict)

        self.update_properties(subclient_prop)
