# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
File for performing IntelliSnap and Array Management operations on Commcell via REST API

ArrayManagement:   Class for handling all Array Management Operations

ArrayManagement:

    __init__()                  --  initialize instance of the ArrayManagement class

    _snap_operation()           --  Common Method for Snap Operations

    mount()                     --  Method for mount operation

    unmount()                   --  Method for unmount operation

    delete()                    --  Method for delete operation

    revert()                    --  Method for revert operation

    reconcile()                     --  Method for recon operation

"""

from __future__ import unicode_literals

from .job import Job
from .exception import SDKException


class ArrayManagement(object):
    """Class for representing all the array management activities with the commcell."""

    def __init__(self, commcell_object):
        """ Initialize the ArrayManagement class instance for performing Snap related operations

            Args:
                commcell_object     (object)    --  instance of the Commcell class

            Returns:
                object  -   instance of the ArrayManagement class
        """

        self._commcell_object = commcell_object
        self._SNAP_OPS = self._commcell_object._services['SNAP_OPERATIONS']

    def _snap_operation(self,
                        operation,
                        volume_id=None,
                        client_name=None,
                        mountpath=None,
                        control_host=None,
                        reconcile=False):
        """ Common Method for Snap Operations

            Args :

                operation    (int)        -- snap Operation value

                volume_id    (int)        -- volume id of the snap backup job

                client_name  (str)        -- name of the destination client, default: None

                MountPath    (str)        -- MountPath for Snap operation, default: None

                control_host (int)        -- Control host for the Snap recon operation,
                defaullt: None
                
                reconcile    (bool)       -- Uses Reconcile json if true

            Return :

                object : Job object of Snap Operation job
        """

        if client_name is None:
            client_id = 0
        else:
            client_id = int(self._commcell_object.clients.get(client_name).client_id)

        if reconcile:
            request_json = {
                "reserveField": 0,
                "doVSSProtection": 0,
                "serverName": "",
                "controlHostId": control_host,
                "CopyId": 0,
                "smArrayId": "",
                "destClientId": 0,
                "destPath": "",
                "serverType": 0,
                "operation": operation,
                "userCredentials": {},
                "scsiServer": {
                    "_type_": 3
                }
            }

        else:
            request_json = {
                "reserveField": 0,
                "serverType": 0,
                "operation": operation,
                "userCredentials": {},
                "volumes": [
                    {
                        "doVSSProtection": 1,
                        "destClientId": client_id,
                        "destPath": mountpath,
                        "serverType": 0,
                        "volumeId": volume_id,
                        "flags": 0,
                        "commCellId": 2,
                        "serverName": "",
                        "userCredentials": {}
                        }
                    ],
                "scsiServer": {
                    "_type_": 3
                    }
                }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._SNAP_OPS, request_json)

        if flag:
            if response.json():
                if "jobId" in response.json():
                    return Job(self._commcell_object, response.json()['jobId'])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'job for Snap Operation failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Snap', '102', o_str)
        else:
            raise SDKException('Snap', '102')

    def mount(self, volume_id, client_name, mountpath):
        """ Mounts Snap of the given volume id

            Args:

                volume_id    (int)        -- volume id of the snap backup job

                client_name  (str)        -- name of the destination client, default: None

                MountPath    (str)        -- MountPath for Snap operation, default: None
        """
        return self._snap_operation(0, volume_id, client_name, mountpath)

    def unmount(self, volume_id):
        """ UnMounts Snap of the given volume id

            Args:

                volume_id    (int)        -- volume id of the snap backup job
        """
        return self._snap_operation(1, volume_id)

    def delete(self, volume_id):
        """ Deletes Snap of the given volume id

            Args:

                volume_id    (int)        -- volume id of the snap backup job
        """
        return self._snap_operation(2, volume_id)

    def revert(self, volume_id):
        """ Reverts Snap of the given volume id

            Args:

                volume_id    (int)        -- volume id of the snap backup job
        """
        return self._snap_operation(3, volume_id)

    def reconcile(self, control_host):
        """ Runs Reconcile Snap of the given control host id

            Args:

                control_host    (int)        -- control host id of the array
        """
        return self._snap_operation(7, control_host=control_host, reconcile=True)
