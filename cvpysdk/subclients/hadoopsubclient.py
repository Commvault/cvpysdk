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

"""Module for operating with Hadoop subclient."""

from __future__ import unicode_literals

from cvpysdk.subclients.bigdataappssubclient import BigDataAppsSubclient


class HadoopSubclient(BigDataAppsSubclient):
    """Derived class from BigDataAppsSubclient for Hadoop workloads."""

    @property
    def subclient_content(self):
        """
        Returns the appropriate content associated with the subclient

        Returns:
            content_list  (list)  -- list of subclient content
        """

        content = self.properties.get("content", [])
        return [entry.get("path") for entry in content if isinstance(entry, dict) and entry.get("path")]

    def set_subclient_content(self, content_list):
        """
        Sets content of subclient entity

        Args:
                content_list (list)  --  list of the indexes to be backed up
                Example:["index1","index2"]

        Returns:
            Nothing

        """

        content_list_copy = list(content_list)
        content_payload = [{"path": content} for content in content_list_copy]

        self.update_properties({
            "content": content_payload,
            "useContentFromPlan": False,
            "fsContentOperationType": 1,
        })