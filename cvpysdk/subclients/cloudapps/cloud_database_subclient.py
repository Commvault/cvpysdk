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

"""File for operating on a Cloud Database Subclient.

CloudDatabaseSubclient is the only class defined in this file.

CloudDatabaseSubclient:  Derived class from CloudAppsSubclient Base class, representing a
                        Cloud Database subclient(Amazon RDS/Redshift/DocumentDB and DynamoDB), and
                        to perform operations on that subclient

CloudDatabaseSubclient:

    _get_subclient_properties()         --  gets the properties of Cloud Database Subclient

    _get_subclient_properties_json()    --  gets the properties JSON of Cloud Database Subclient

    content()                           --  gets the content of the subclient

    _set_content()                      --  sets the content of the subclient

    browse()                            --  Browse and returns the content of this subclient's instance backups

    restore()                           --  Restores a cloud database from the specified source and restore options

"""
from ..casubclient import CloudAppsSubclient
from ...exception import SDKException


class CloudDatabaseSubclient(CloudAppsSubclient):
    """ Derived class from Subclient Base class, representing a Cloud Database subclient,
            and to perform operations on that subclient. """

    def _get_subclient_properties(self):
        """ Gets the subclient related properties of Cloud Database subclient. """

        super(CloudDatabaseSubclient, self)._get_subclient_properties()

        if 'cloudDbContent' in self._subclient_properties:
            self._cloud_db_content = self._subclient_properties["cloudDbContent"]
        else:
            self._cloud_db_content = {}

    def _get_subclient_properties_json(self):
        """ Gets the properties JSON of Cloud Database Subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "commonProperties": self._commonProperties,
                    "cloudAppsSubClientProp": {
                        "instanceType": self._backupset_object._instance_object.ca_instance_type
                    },
                    "planEntity": {
                        "planName": self.storage_policy
                    },
                    "cloudDbContent": self._cloud_db_content
                }
        }
        return subclient_json

    def _set_content(self, content=None):
        """ Sets the subclient content dictionary

            Args:
                content         (list)      --  list of subclient content

        """
        if content is not None:
            self._cloud_db_content = {
                "children": content
            }

        self._set_subclient_properties("_cloud_db_content", self._cloud_db_content)

    @property
    def content(self):
        """ Gets the appropriate content from the Subclient relevant to the user.

           Returns:
               dict - dict of cloud database content associated with the subclient

       """
        return self._cloud_db_content

    @content.setter
    def content(self, subclient_content):
        """ Creates the dict of content JSON to pass to the API to add/update content of a
            Cloud Database Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                dict - dict of the appropriate JSON for an agent to send to the POST Subclient API

            Raises :
                SDKException : if the subclient content is not a list value and if it is empty

        """
        if isinstance(subclient_content, list) and subclient_content != []:
            self._set_content(content=subclient_content)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient content should be a list value and not empty'
            )

    def browse(self, *args, **kwargs):
        """
            Browses the content of this cloud database subclient's instance

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
                dict - Browse response json that contains list of snapshot information

        """
        return self._instance_object.browse(*args, **kwargs)

    def restore(
            self,
            destination,
            source,
            restore_options):
        """
            Restores the content of this subclient's instance content

            Args:
                destination : Destination cluster name we want to restore to.

                source   : Source snapshot we want to restore from.

                restore_options  : Restore options needed to submit a restore request.

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
        return self._instance_object.restore(destination, source, restore_options)
