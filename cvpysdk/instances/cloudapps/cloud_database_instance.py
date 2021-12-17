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

""" File for operating on a cloud database instance.

CloudDatabaseInstance is the only class defined in this file.

CloudDatabaseInstance:   Derived class from CloudAppsInstance Base class, representing a
                        Cloud Database instance( Amazon RDS,Redshift,DocumentDB and DynamoDB), and to
                        perform operations on that instance

CloudDatabaseInstance:

    __init__()                      --  Initializes cloud database instance object with associated
    agent_object, instance name and instance id

    _get_instance_properties()      --  Retrieves cloud database related instance properties

    _browse_request_json()          --  Retrieves and sets browse request json based on browse options

    _process_browse_response()      --  Process the response received from browse request

    browse()                        --  Browse and returns the contents of this instance backup

    restore()                       -- Submits a restore request based on restore options

"""

from __future__ import unicode_literals
import time
from past.builtins import basestring
from ..cainstance import CloudAppsInstance
from ...exception import SDKException


class CloudDatabaseInstance(CloudAppsInstance):
    """
    Class for representing an Instance of the Cloud Database such as
    Amazon RDS/Redshift/DocumentDB/DynamoDB/Cloud Spanner

    """

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initializes the object of the CloudDatabaseInstance class

            Args:
                agent_object    (object)  --  instance of the Agent class

                instance_name   (str)     --  name of the instance

                instance_id     (str)     --  id of the instance
                    default: None

            Returns:
                object - instance of the Instance class

        """

        self._ca_instance_type = None
        self._browse_request = {}
        self._browse_url = None

        super(
            CloudDatabaseInstance,
            self).__init__(
                agent_object,
                instance_name,
                instance_id)

    def _get_instance_properties(self):
        """Gets the properties of this instance"""
        super(CloudDatabaseInstance, self)._get_instance_properties()
        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance['instanceType']

    @property
    def ca_instance_type(self):
        """Returns the CloudApps instance type as a read-only attribute."""
        return self._ca_instance_type

    @property
    def _browse_request_json(self):
        """Returns the CloudApps instance browse request json"""
        return self._browse_request

    @_browse_request_json.setter
    def _browse_request_json(self, value):
        """ Creates CloudApps instance browse request json based on the options

            Args: Dictionary of browse options

                Example:
                    {
                        'start_time': 0,
                        'end_time': 1570808875,
                        'include_aged_data': 0,
                        'copy_precedence': 0,
                    }

        """
        start_time = value.get('start_time', 0)
        end_time = value.get('end_time', int(time.time()))
        include_aged_data = value.get('include_aged_data', 0)
        copy_precedence = value.get('copy_precedence', 0)
        self._browse_request = {
            "entity": {
                "instanceId": int(self.instance_id)
            },
            "copyPresedence": copy_precedence,
            "includeAgedData": include_aged_data,
            "startTime": start_time,
            "endTime": end_time
        }

    def _process_browse_response(self, flag, response):
        """ Process browse request response

            Args:

                flag -- indicates whether the rest API request is successful

                response -- response returned if the request was successful.

            Returns:

                dict    - The JSON response received from the browse request

                Exception - If the browse request failed

        """
        if flag:
            return response.json()

        o_str = 'Failed to browse content of this instance backups.\nError: "{0}"'
        raise SDKException('Subclient', '102', o_str.format(response))

    def browse(self, *args, **kwargs):
        """
            Browses the content of cloud database instance

            args: Dictionary of browse options

                Example:

                        {
                            'start_time': 0,
                            'end_time': 1570808875,
                            'include_aged_data': 0,
                            'copy_precedence': 0,
                        }

            kwargs: keyword argument of browse options

                Example:

                        {
                            start_time: 0,
                            end_time: 1570808875,
                            include_aged_data: 0,
                            copy_precedence: 0,
                        }

            Returns:
                dict - Browse response json

        """

        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        self._browse_request_json = options
        flag, response = self._cvpysdk_object.make_request('POST', self._browse_url, self._browse_request)
        return self._process_browse_response(flag, response)

    def restore(self,
                destination,
                source,
                options):
        """
            Restores the content of this instance content

            Args:

                destination : Destination cluster name we want to restore to.

                source   : Source snapshot we want to restore from.

                options  : Restore options needed to submit a restore request.

                    Example:    Restore of amazon redshift instance cluster from snapshot
                        {
                            destination : 'cluster',
                            source : 'snapshot',
                            options :   {
                                            'allowVersionUpgrade' : true,
                                            'publicallyAccessible' : true,
                                            'restoreTags' : false,
                                            'enableDeletionProtection': false,
                                            'availabilityZone': 'us-east-2a',
                                            'targetParameterGroup': 'param',
                                            'targetSubnetGroup': 'subnet',
                                            'nodeType': 'dc-large-8',
                                            'targetPort': 2990,
                                            'numberOfNodes': 1
                                        }
                        }

            Returns:

                object - instance of the Job class for this restore job
        """
        if not (isinstance(source, basestring) or
                isinstance(destination, basestring) or
                isinstance(options, dict)):
            raise SDKException('Instance', '101')
        request_json = self._restore_json(destination=destination, source=source, options=options)
        return self._process_restore_response(request_json)
