#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for handling all the exceptions for the CVPySDK python package.

EXCEPTION_DICT: A python dictionary for holding all the exception messages for a specific event
                    or class.

SDKException: Class inheriting the "Exception" Base class for raising a specific exception for
                the CVPySDK python package.
"""

# Common dictionary for all exceptions among the python package
EXCEPTION_DICT = {
    'Response': {
        '101': 'Response was not success',
        '102': 'Response received is empty'
    },
    'Commcell': {
        '101': 'Commcell is not reachable. Please check the commcell name again'
    },
    'CVPySDK': {
        '101': 'Failed to Login with the credentials provided',
        '102': 'Connection Error. Please check your network connection',
        '103': '',
        '104': 'Did not receive the Auth token',
        '105': 'Reached the maximum attempts limit'
    },
    'Client': {
        '101': 'Client name should be specified',
        '102': 'Attribute name not provided',
        '103': 'Data type of the inputs is not valid',
        '104': '',
        '105': 'Attribute\'s value not provided'
    },
    'Agent': {
        '101': 'Agent name should be specified',
        '102': ''
    },
    'Backupset': {
        '101': 'Backupset name should be specified',
        '102': ''
    },
    'Subclient': {
        '101': 'Data type of the inputs is not valid',
        '102': '',
        '103': 'Backup Level not identified. Please check the backup level again',
        '104': 'Files/Folders to restore list is empty',
        '105': 'Type of client should either be the Client class instance or string',
        '106': 'Input date is incorrect',
        '107': 'End Date should be greater than the Start Date'
    },
    'Job': {
        '101': 'Incorrect JobId',
        '102': 'No job exists with the specified job id'
    },
    'Storage': {
        '101': '',
        '102': 'Data type of the inputs is not valid',
        '103': 'Type of media agent should either be the MediaAgent class instance or string',
        '104': 'Type of library should either be the DiskLibrary class instance or string'
    },
    'Schedules': {
        '101': 'Invalid Class object passed as argument to the Schedules class'
    },
    'ClientGroup': {
        '101': 'Client Group name should be specified',
        '102': 'Attribute name not provided',
        '103': 'Data type of the inputs is not valid',
        '104': '',
        '105': 'Attribute\'s value not provided'
    },
    'UserGroup': {
        '101': 'User Group name should be specified',
        '102': 'Attribute name not provided',
        '103': 'Data type of the inputs is not valid',
        '104': '',
        '105': 'Attribute\'s value not provided'
    },
    'Alert': {
        '101': 'Alert name should be specified',
        '102': 'Attribute name not provided',
        '103': 'Data type of the inputs is not valid',
        '104': '',
        '105': 'Attribute\'s value not provided'
    }
}


class SDKException(Exception):
    """Exception class for raising exception specific to a module."""

    def __init__(self, exception_module, exception_id, exception_message=""):
        """Initialize the SDKException class instance for the exception.

            Args:
                exception_module (str)  - name of the module where the exception was raised
                exception_id (str)      - id of the exception specific to the exception_module
                exception_message (str) - additional message about the exception

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
