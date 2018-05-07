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

    def _snap_operation(self, operation, volume_id, client_name=None, mountpath=None):
        """ Common Method for Snap Operations

            Args :

                operation    (int)        -- snap Operation value

                volume_id    (int)        -- volume id of the snap backup job

                client_name  (str)        -- name of the destination client, default: None

                MountPath    (str)        -- MountPath for Snap operation, default: None

            Return :

                object : Job object of Snap Operation job
        """

        if volume_id is None:
            raise SDKException('Snap', '101')
        if client_name is None:
            client_id = ""
        else:
            client_id = self._commcell_object.clients.get(client_name).client_id

        xml = """
        <EVGui_SnapBackupOperationRequest CopyId="0" operation="{0}">
            <volumes volumeId="{1}" commCellId="2" doVSSProtection="0" destClientId="{2}" destPath="{3}"
        serverType="0">
                <userCredentials />
            </volumes>
        </EVGui_SnapBackupOperationRequest>""".format(operation, volume_id, client_id, mountpath)

        response_json = self._commcell_object._qoperation_execute(xml)

        if "jobId" in response_json:
            return Job(self._commcell_object, response_json['jobId'])
        elif "errorCode" in response_json:
            error_message = response_json['errorMessage']

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
