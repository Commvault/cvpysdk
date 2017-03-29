#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for handling all the exceptions for the CVPySDK python package.

EXCEPTION_DICT:     A python dictionary for holding all the exception messages
                        for a specific event or class.

SDKException:       Class inheriting the "Exception" Base class for raising
                        a specific exception for the CVPySDK python package.
"""

from __future__ import absolute_import

# Common dictionary for all exceptions among the python package
EXCEPTION_DICT = {
    'Response': {
        '101': 'Response was not success',
        '102': 'Response received is empty'
    },
    'Commcell': {
        '101': 'Commcell is not reachable. Please check the commcell name and services again',
        '102': 'Authtoken not received. Please try again.'
    },
    'CVPySDK': {
        '101': 'Failed to Login with the credentials provided',
        '102': '',
        '103': 'Reached the maximum attempts limit',
        '104': 'This session has expired. Please login again'
    },
    'Client': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Time Value should be greater than current time',
        '104': 'Time Value entered is not of correct format'
    },
    'Agent': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Time Value should be greater than current time',
        '104': 'Time Value entered is not of correct format'
    },
    'Backupset': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
    },
    'Instance': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'Subclient': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Backup Level not identified. Please check the backup level again',
        '104': 'File/Folder(s) to restore list is empty',
        '105': 'Type of client should either be the Client class instance or string',
        '106': 'Input date is incorrect',
        '107': 'End Date should be greater than the Start Date',
        '108': 'Time Value should be greater than current time',
        '109': 'Time Value entered is not of correct format',
        '110': 'No data found at the path specified',
        '111': 'No File/Folder matched the input value',
        '112': 'Method Not Implemented'
    },
    'Job': {
        '101': 'Incorrect JobId',
        '102': '',
        '103': 'No job exists with the specified Job ID',
        '104': 'No records found for this Job'
    },
    'Storage': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Type of media agent should either be the MediaAgent class instance or string',
        '104': 'Type of library should either be the DiskLibrary class instance or string',
        '105': 'No storage policies exist for this user'
    },
    'Schedules': {
        '101': 'Invalid Class object passed as argument to the Schedules class',
        '102': 'Data type of the input(s) is not valid'
    },
    'ClientGroup': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Time Value should be greater than current time',
        '104': 'Time Value entered is not of correct format'
    },
    'UserGroup': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'Alert': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'Workflow': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    }
}


class SDKException(Exception):
    """Exception class for raising exception specific to a module."""

    def __init__(self, exception_module, exception_id, exception_message=""):
        """Initialize the SDKException class instance for the exception.

            Args:
                exception_module  (str)  --  name of the module where the exception was raised

                exception_id      (str)  --  id of the exception specific to the exception_module

                exception_message (str)  --  additional message about the exception

            Returns:
                object - instance of the SDKException class of type Exception
        """
        self.exception_module = str(exception_module)
        self.exception_id = str(exception_id)
        self.exception_message = EXCEPTION_DICT[exception_module][exception_id]

        if exception_message:
            if self.exception_message:
                self.exception_message = '\n'.join([self.exception_message, exception_message])
            else:
                self.exception_message = exception_message

        Exception.__init__(self, self.exception_message)
