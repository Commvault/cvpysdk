# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for License operations.

LicenseDetails        : Class for representing license details information

LicenseDetails:
__init__(Commcell_object)--  initialise with object of CommCell

refresh()                --  refeshes the license details data

"""
from __future__ import absolute_import
from __future__ import unicode_literals
from .exception import SDKException


class LicenseDetails(object):
    """Class for accessing license details information"""
    def __init__(self, commcell_object):
        self._commcell_object = commcell_object
        self._LICENSE = self._commcell_object._services['LICENSE']
        self._get_license_details()

    def _get_license_details(self):
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._LICENSE
        )
        if flag:
            if response.json():
                self._commcell_id = response.json()['commcellId']
                self._oemname = response.json()['oemName']
                self._regcode = response.json()['regCode']
                self._serialno = response.json()['serialNo']
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def refresh(self):
        """updates metrics object with the latest configuration"""
        self._get_license_details()

    @property
    def commcell_id(self):
        """returns the CommCell Id in decimal value"""
        return self._commcell_id

    @property
    def oem_name(self):
        """returns the oem_name"""
        return self._oemname

    @property
    def registration_code(self):
        """returns the registration code of CommCell"""
        return self._regcode

    @property
    def serial_number(self):
        """returns the serial number of CommCell"""
        return self._serialno
