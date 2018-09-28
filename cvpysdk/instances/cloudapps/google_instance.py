# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Google Instance.

GoogleInstance is the only class defined in this file.

GoogleInstance: Derived class from CloudAppsInstance Base class, representing a
Google (GMail/GDrive) and OneDrive instance,
and to perform operations on that instance

GoogleInstance:

    _get_instance_properties()  --  Instance class method overwritten to add cloud apps
    instance properties as well

    restore_out_of_place()      --  runs out-of-place restore for the instance

"""

from __future__ import unicode_literals
from past.builtins import basestring
from ...exception import SDKException
from ..cainstance import CloudAppsInstance


class GoogleInstance(CloudAppsInstance):
    """Class for representing an Instance of the GMail/Gdrive instance type."""

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        super(GoogleInstance, self)._get_instance_properties()
        # Common properties for Google and OneDrive
        self._ca_instance_type = None
        self._manage_content_automatically = None
        self._auto_discovery_enabled = None
        self._auto_discovery_mode = None
        self._proxy_client = None

        # Google instance related properties
        self._app_email_id = None
        self._google_admin_id = None
        self._service_account_key_file = None
        self._app_client_id = None

        # OneDrive instance related properties
        self._client_id = None
        self._tenant = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance['instanceType']

            if 'gInstance' in cloud_apps_instance:
                ginstance = cloud_apps_instance['gInstance']

                self._manage_content_automatically = ginstance['manageContentAutomatically']
                self._auto_discovery_enabled = ginstance['isAutoDiscoveryEnabled']
                self._auto_discovery_mode = ginstance['autoDiscoveryMode']
                self._app_email_id = ginstance['appEmailId']
                self._google_admin_id = ginstance['emailId']
                self._service_account_key_file = ginstance['appKey']
                self._app_client_id = ginstance['appClientId']

            if 'oneDriveInstance' in cloud_apps_instance:
                onedrive_instance = cloud_apps_instance['oneDriveInstance']

                self._manage_content_automatically = onedrive_instance['manageContentAutomatically']
                self._auto_discovery_enabled = onedrive_instance['isAutoDiscoveryEnabled']
                self._auto_discovery_mode = onedrive_instance['autoDiscoveryMode']
                self._client_id = onedrive_instance['clientId']
                self._tenant = onedrive_instance['tenant']

            if 'generalCloudProperties' in cloud_apps_instance:
                self._proxy_client = cloud_apps_instance[
                    'generalCloudProperties']['proxyServers'][0]['clientName']

    @property
    def ca_instance_type(self):
        """Returns the CloudApps instance type"""
        if self._ca_instance_type == 1:
            return 'GMAIL'
        elif self._ca_instance_type == 2:
            return 'GDRIVE'
        elif self._ca_instance_type == 7:
            return 'ONEDRIVE'
        return self._ca_instance_type

    @property
    def manage_content_automatically(self):
        """Returns the CloudApps Manage Content Automatically property"""
        return self._manage_content_automatically

    @property
    def auto_discovery_status(self):
        """Treats the Auto discovery property as a read-only attribute."""
        return self._auto_discovery_enabled

    @property
    def auto_discovery_mode(self):
        """Returns the Auto discovery mode property"""
        return self._auto_discovery_mode

    @property
    def app_email_id(self):
        """Returns the service account mail id"""
        return self._app_email_id

    @property
    def google_admin_id(self):
        """Returns the Google admin mail id"""
        return self._google_admin_id

    @property
    def key_file_path(self):
        """Returns the service account key file path"""
        return self._service_account_key_file

    @property
    def google_client_id(self):
        """Returns the service account client id"""
        return self._app_client_id

    @property
    def onedrive_client_id(self):
        """Returns the OneDrive app client id"""
        return self._client_id

    @property
    def onedrive_tenant(self):
        """Returns the OneDrive tenant id"""
        return self._tenant

    @property
    def proxy_client(self):
        """Returns the proxy client name to this instance"""
        return self._proxy_client

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
            to_disk=False):
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

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_disk             (bool)       --  If True, restore to disk will be performed

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
        from cvpysdk.client import Client

        if not ((isinstance(client, basestring) or isinstance(client, Client)) and
                isinstance(destination_path, basestring) and
                isinstance(paths, list) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        if isinstance(client, Client):
            client = client
        elif isinstance(client, basestring):
            client = Client(self._commcell_object, client)
        else:
            raise SDKException('Subclient', '105')

        paths = self._filter_paths(paths)

        destination_path = self._filter_paths([destination_path], True)

        if paths == []:
            raise SDKException('Subclient', '104')

        request_json = self._restore_json(
            paths=paths,
            in_place=False,
            client=client,
            destination_path=destination_path,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
        )
        dest_user_account = destination_path
        rest_different_account = True
        restore_to_google = True

        if to_disk:
            dest_user_account = ''
            rest_different_account = False
            restore_to_google = False
        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]['cloudAppsRestoreOptions'] = {
                "instanceType": self._ca_instance_type,
                "googleRestoreOptions": {
                    "strDestUserAccount": dest_user_account,
                    "folderGuid": "",
                    "restoreToDifferentAccount": rest_different_account,
                    "restoreToGoogle": restore_to_google
                }
        }
        return self._process_restore_response(request_json)

    def enable_auto_discovery(self, mode='REGEX'):
        """Enables auto discovery on instance.

           Args:

                mode    (str)   -- Auto Discovery mode

                Valid Values:

                    REGEX
                    GROUP

        """
        auto_discovery_dict = {
            'REGEX': 0,
            'GROUP': 1
        }
        instance_dict = {
            1: 'gInstance',
            2: 'gInstance',
            7: 'oneDriveInstance'
        }
        auto_discovery_mode = auto_discovery_dict.get(mode.upper(), None)

        if auto_discovery_mode is None:
            raise SDKException('Instance', '107')
        instance_prop = self._properties['cloudAppsInstance'].copy()

        instance_prop[instance_dict[instance_prop['instanceType']]]['isAutoDiscoveryEnabled'] = True
        instance_prop[instance_dict[instance_prop['instanceType']]]['autoDiscoveryMode'] = auto_discovery_mode

        self._set_instance_properties("_properties['cloudAppsInstance']", instance_prop)
        self.refresh()

    def _get_instance_properties_json(self):
        """Returns the instance properties json."""

        return {'instanceProperties': self._properties}