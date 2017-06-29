#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a NAS Subclient

NASSubclient is the only class defined in this file.

NASSubclient: Derived class from Subclient Base class, representing a nas subclient,
                        and to perform operations on that subclient

NASSubclient:
    _get_subclient_content_()           --  gets the content of a nas subclient

    _set_subclient_content_()           --  sets the content of a nas subclient

    _initialize_subclient_properties()  --  initializes nas specific properties of subclient

    _get_subclient_filter_content_()    --  gets the filter content of a nas subclient

    _set_subclient_filter_content_()    --  sets the filter content of a nas subclient

    _update_content()                   --  updates the content/filter content of subclient

    filter_content()                    --  update the filter content of the subclient

    content()                           --  update the content of the subclient

    backup()                            --  run a backup job for the subclient

"""

from __future__ import unicode_literals

from past.builtins import basestring

from ..subclient import Subclient
from ..exception import SDKException
from ..job import Job


class NASSubclient(Subclient):
    """Derived class from Subclient Base class, representing a nas subclient,
        and to perform operations on that subclient."""

    def _get_subclient_content_(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient
        """
        content = []
        if 'content' in self._subclient_properties:
            subclient_content = self._subclient_properties['content']

            for path in subclient_content:
                if 'path' in path:
                    content.append(path["path"])

        return content

    def _set_subclient_content_(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            NAS Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []

        for path in subclient_content:
            nas_dict = {
                "path": path
            }
            content.append(nas_dict)

        return content

    def _initialize_subclient_properties(self):
        """Initializes the common properties for the subclient."""

        super(NASSubclient, self)._initialize_subclient_properties()

        self._filter = self._get_subclient_filter_content_()

    def _get_subclient_filter_content_(self):
        """Gets the subclient filter content

            Returns:
                list - list of filter content associated with subclient
        """
        filter_content = []

        if 'content' in self._subclient_properties:
            subclient_content = self._subclient_properties['content']

            for path in subclient_content:
                if 'excludePath' in path:
                    filter_content.append(path["excludePath"])

        return filter_content

    def _set_subclient_filter_content_(self, filter_content):
        """Creates the list of content JSON to pass to the API to add/update filter content of a
            NAS Subclient.

            Args:
                filter_content (list)  --  list of the filter content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []

        for path in filter_content:
            nas_dict = {
                "excludePath": path
            }
            content.append(nas_dict)

        return content

    def _update_content(self, content=None, filter_content=None):
        """Updates the properties of the subclient.

            Args:
                content        (str)   --  subclient content

                filter_content (str)   --  subclient filter content

            Returns:
                (bool, basestring, basestring):
                    bool -  flag specifies whether success / failure

                    str  -  error code received in the response

                    str  -  error message received

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        if content:
            final_content = self._set_subclient_content_(content) + \
                self._set_subclient_filter_content_(self.filter_content)
        elif filter_content:
            final_content = self._set_subclient_content_(self.content) + \
                self._set_subclient_filter_content_(filter_content)

        request_json = {
            "association": {
                "entity": [{
                    "clientName": self._backupset_object._agent_object._client_object.client_name,
                    "appName": self._backupset_object._agent_object.agent_name,
                    "instanceName": self._backupset_object._instance_object.instance_name,
                    "backupsetName": self._backupset_object.backupset_name,
                    "subclientName": self.subclient_name
                }]
            }, "subClientProperties": {
                "contentOperationType": 1,
                "subClientEntity": {
                    "clientName": self._backupset_object._agent_object._client_object.client_name,
                    "appName": self._backupset_object._agent_object.agent_name,
                    "instanceName": self._backupset_object._instance_object.instance_name,
                    "backupsetName": self._backupset_object.backupset_name,
                    "subclientName": self.subclient_name
                },
                "content": final_content
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            "POST", self._SUBCLIENT, request_json
        )

        self._initialize_subclient_properties()

        if flag:
            if response.json():
                if "response" in response.json():
                    error_code = str(response.json()["response"][0]["errorCode"])

                    if error_code == "0":
                        return (True, "0", "")
                    else:
                        error_message = ""

                        if "errorString" in response.json()["response"][0]:
                            error_message = response.json()["response"][0]["errorString"]

                        if error_message:
                            return (False, error_code, error_message)
                        else:
                            return (False, error_code, "")
                elif "errorCode" in response.json():
                    error_code = str(response.json()['errorCode'])
                    error_message = response.json()['errorMessage']

                    if error_code == "0":
                        return (True, "0", "")

                    if error_message:
                        return (False, error_code, error_message)
                    else:
                        return (False, error_code, "")
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def filter_content(self):
        """Treats the subclient filter content as a property of the Subclient class."""
        return self._filter

    @property
    def content(self):
        """Treats the subclient content as a property of the Subclient class."""
        return self._content

    @content.setter
    def content(self, value):
        """Sets the content of the subclient as the value provided as input.

            Raises:
                SDKException:
                    if failed to update content of subclient

                    if the type of value input is not list

                    if value list is empty
        """
        if isinstance(value, list) and value != []:
            output = self._update_content(content=value)

            if output[0]:
                return
            else:
                o_str = 'Failed to update the content of the subclient\nError: "{0}"'
                raise SDKException('Subclient', '102', o_str.format(output[2]))
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient content should be a list value and not empty'
            )

    @filter_content.setter
    def filter_content(self, value):
        """Sets the filter content of the subclient as the value provided as input.

            example: ['/vol/Test_Vol', '/vol/test/file*', '/vol/test2/file.txt']

            Raises:
                SDKException:
                    if failed to update filter content of subclient

                    if the type of value input is not list

                    if value list is empty
        """
        if isinstance(value, list) and value != []:
            output = self._update_content(filter_content=value)

            if output[0]:
                return
            else:
                o_str = 'Failed to update the filter content of the subclient\nError: "{0}"'
                raise SDKException('Subclient', '102', o_str.format(output[2]))
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient filter content should be a list value and not empty'
            )

    def backup(
            self,
            backup_level="Incremental",
            incremental_backup=False,
            incremental_level='BEFORE_SYNTH', on_demand_input=None, snap_name=None):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level        (str)   --  level of backup the user wish to run
                        Full / Incremental / Differential / Synthetic_full
                    default: Incremental

                incremental_backup  (bool)  --  run incremental backup
                        only applicable in case of Synthetic_full backup
                    default: False

                incremental_level   (str)   --  run incremental backup before/after synthetic full
                        BEFORE_SYNTH / AFTER_SYNTH

                        only applicable in case of Synthetic_full backup
                    default: BEFORE_SYNTH

                on_demand_input     (str)   --  input file location for on demand backupset
                    default: None

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success
        """
        if snap_name is None:
            return super(NASSubclient, self).backup(
                backup_level, incremental_backup, incremental_level, on_demand_input
            )
        else:
            request_json = self._backup_json(backup_level, incremental_backup, incremental_level)

            if not isinstance(snap_name, basestring):
                raise SDKException('Subclient', '101')

            if snap_name:
                nas_options = {
                    "nasOptions": {
                        "backupFromSnap": snap_name,
                        "backupQuotas": True,
                        "backupFromSnapshot": True,
                        "backupFromSnapshotYes": True,
                        "replicationVolumeId": 0
                    }
                }
                request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"].update(
                    nas_options
                )

            bakup_service = self._commcell_object._services['CREATE_TASK']

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', bakup_service, request_json
            )

            if flag:
                if response.json():
                    if "jobIds" in response.json():
                        return Job(self._commcell_object, response.json()['jobIds'][0])
                    elif "errorCode" in response.json():
                        o_str = 'Initializing backup failed\nError: "{0}"'.format(
                            response.json()['errorMessage']
                        )
                        raise SDKException('Subclient', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
