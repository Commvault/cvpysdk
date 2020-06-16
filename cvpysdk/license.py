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
                self._cs_hostname = response.json()['csHostNameOrAddress']
                self._license_ipaddress = response.json()['licenseIpAddress']
                self._oemname = response.json()['oemName']
                self._regcode = response.json()['regCode']
                self._serialno = response.json()['serialNo']
                self._license_mode = response.json()['licenseMode']
                self._expiry_date = response.json()['expiryDate']
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
    def commcell_id_hex(self):
        """returns the hexadecimal value of commcell id"""
        ccid = self._commcell_id
        if ccid == -1:
            return 'FFFFF'
        return hex(ccid).split('x')[1].upper()

    @property
    def cs_hostname(self):
        """ Returns the csHostName Or Address of CommCell"""
        return self._cs_hostname

    @property
    def license_ipaddress(self):
        """ Returns the license Ip Address """
        return self._license_ipaddress

    @property
    def oem_name(self):
        """returns the oem_name"""
        return self._oemname

    @property
    def license_mode(self):
        """ Returns the license mode of license"""
        return self._license_mode

    @property
    def registration_code(self):
        """returns the registration code of CommCell"""
        return self._regcode

    @property
    def serial_number(self):
        """returns the serial number of CommCell"""
        return self._serialno

    @property
    def expiry_date(self):
        """ Returns the expiry date of License"""
        return self._expiry_date
