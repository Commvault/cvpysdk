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
    __init__(Commcell_object)    --  initialise with object of CommCell
    
    _get_detailed_licenses()      --  Gets all types of license details associated to the commcell object
    
    _get_capacity_details()       -- GET request to get capacity licenses property
    
    _get_complete_oi_licenses()    --   GET request to get OI licenses property
    
    _get_virtualization_licenses()    --   GET request to get virtualization licenses property
    
    _get_user_licenses()    --   GET request to get user licenses property
    
    _get_activate_licenses()    --   GET request to get activate licenses property
    
    _get_metallic_licenses()    --   GET request to get metallic licenses property
    
    _get_other_licenses()    --   GET request to get other licenses property
    
    _get_license_details    --   GET request to get detailed license information
    
    
    refresh()    --    Updates License object with the latest configuration
    
    

LicenseDetails Attributes
-------------------------
    commcell_id   --    Returns the CommCell Id in decimal value
    
    commcell_id_hex   --    Returns the hexadecimal value of commcell id
    
    cs_hostname   --    Returns the csHostName Or Address of CommCell
    
    license_ipaddress   --    Returns the license Ip Address 
    
    oem_name   --    Returns the oem_name
    
    license_mode   --    Returns the license mode of license
    
    registration_code   --    Returns the registration code of CommCell
    
    serial_number   --    Returns the serial number of CommCell
    
    expiry_date   --    Returns the expiry date of License
    
    capacity_licenses   --    Returns dictionary with the capacity licenses
    
    complete_oi_licenses   --    Returns dictionary with the complete oi licenses
    
    virtualization_licenses   --    Returns dictionary with the virtualization licenses
    
    user_licenses   --    Returns dictionary with the user licenses
    
    activate_licenses   --    Returns dictionary with the activate licenses
    
    metallic_licenses   --    Returns dictionary with the metallic licenses
    
    other_licenses   --    Returns dictionary with the other licenses

"""
from __future__ import absolute_import
from __future__ import unicode_literals
from .exception import SDKException


class LicenseDetails(object):
    """Class for accessing license details information"""    

    def __init__(self, commcell_object):
        """Initialize object of the LicenseDetails class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the LicenseDetails class
        """
        self._commcell_object = commcell_object
        self._LICENSE = self._commcell_object._services['LICENSE']
        self._APPLY_LICENSE = self._commcell_object._services['APPLY_LICENSE']
        self._capacity_licenses = None
        self._complete_oi_licenses = None
        self._virtualization_licenses = None
        self._user_licenses = None
        self._activate_licenses = None
        self._metallic_licenses = None
        self._other_licenses = None
        self._get_license_details()

    def _get_detailed_licenses(self):
        """
        Gets all types of license details associated to the commcell object
        """
        self._get_capacity_details()
        self._get_complete_oi_licenses()
        self._get_virtualization_licenses()
        self._get_user_licenses()
        self._get_activate_licenses()
        self._get_metallic_licenses()
        self._get_other_licenses()

    def _get_capacity_details(self):
        """
        Request to get capacity licenses property

        Raises:
            SDKException:

                if response is not success

                if response is empty

        """

        self._CAPACITY_LICENSE = self._commcell_object._services['CAPACITY_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._CAPACITY_LICENSE)

        if flag:
            if response.json():
                self._capacity_licenses = response.json().get('records',None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_complete_oi_licenses(self):
        """
       GET request to get OI licenses property

        Raises:
            SDKException:

                if response is not success

                if response is empty

        """

        self._OI_LICENSE = self._commcell_object._services['OI_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._OI_LICENSE)

        if flag:
            if response.json():
                self._complete_oi_licenses = response.json().get('records',None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_virtualization_licenses(self):
        """
       GET request to get virtualization licenses property

        Raises:
            SDKException:

                if response is not success

                if response is empty

        """
        self._VIRTUALIZATION_LICENSE = self._commcell_object._services['VIRTUALIZATION_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._VIRTUALIZATION_LICENSE)

        if flag:
            if response.json():
                self._virtualization_licenses = response.json().get('records',None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_user_licenses(self):
        """
       GET request to get user licenses property

        Raises:
            SDKException:

                if response is not success

                if response is empty

        """
        self._USER_LICENSE = self._commcell_object._services['USER_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._USER_LICENSE)

        if flag:
            if response.json():
                self._user_licenses = response.json().get('records',None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_activate_licenses(self):
        """
       GET request to get activate licenses property

        Raises:
            SDKException:

                if response is not success

                if response is empty

        """
        self._ACTIVATE_LICENSE = self._commcell_object._services['ACTIVATE_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._ACTIVATE_LICENSE)

        if flag:
            if response.json():
                self._activate_licenses = response.json().get('records',None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_metallic_licenses(self):
        """
       GET request to get metallic licenses property

        Raises:
            SDKException:

                if response is not success

                if response is empty

        """
        self._METALLIC_LICENSE = self._commcell_object._services['METALLIC_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._METALLIC_LICENSE)

        if flag:
            if response.json():
                self._metallic_licenses = response.json().get('records',None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_other_licenses(self):
        """
       GET request to get other licenses property

        Raises:
            SDKException:

                if response is not success

                if response is empty

        """
        self._OTHER_LICENSE = self._commcell_object._services['OTHER_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._OTHER_LICENSE)

        if flag:
            if response.json():
                self._other_licenses = response.json().get('records',None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_license_details(self):
        """
       GET request to get detailed license information

        Raises:
            SDKException:

                if response is not success

                if response is empty

        """

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
        """Updates metrics object with the latest configuration"""
        self._get_license_details()
        self._get_detailed_licenses()

    @property
    def commcell_id(self):
        """Returns the CommCell Id in decimal value"""
        return self._commcell_id

    @property
    def commcell_id_hex(self):
        """Returns the hexadecimal value of commcell id"""
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
        """Returns the oem_name"""
        return self._oemname

    @property
    def license_mode(self):
        """ Returns the license mode of license"""
        return self._license_mode

    @property
    def registration_code(self):
        """Returns the registration code of CommCell"""
        return self._regcode

    @property
    def serial_number(self):
        """Returns the serial number of CommCell"""
        return self._serialno

    @property
    def expiry_date(self):
        """ Returns the expiry date of License"""
        return self._expiry_date

    @property
    def capacity_licenses(self):
        """Returns dictionary with the capacity licenses"""
        return self._capacity_licenses

    @property
    def complete_oi_licenses(self):
        """Returns dictionary with the complete oi licenses"""
        return self._complete_oi_licenses

    @property
    def virtualization_licenses(self):
        """Returns dictionary with the virtualization licenses"""
        return self._virtualization_licenses

    @property
    def user_licenses(self):
        """Returns dictionary with the user licenses"""
        return self._user_licenses

    @property
    def activate_licenses(self):
        """Returns dictionary with the activate licenses"""
        return self._activate_licenses

    @property
    def metallic_licenses(self):
        """Returns dictionary with the metallic licenses"""
        return self._metallic_licenses

    @property
    def other_licenses(self):
        """Returns dictionary with the other licenses"""
        return self._other_licenses
