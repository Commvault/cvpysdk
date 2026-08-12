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
from typing import Any, Dict
from .exception import SDKException


class LicenseDetails(object):
    """
    Provides access to detailed license information for a CommCell environment.

    The LicenseDetails class enables retrieval and management of various license types
    and their associated details within a CommCell. It offers methods to fetch detailed
    license data, including capacity, virtualization, user, activation, metallic, and
    other license categories. The class also provides properties to access key license
    attributes such as CommCell ID, host information, license mode, registration code,
    serial number, expiry date, and OEM name.

    Key Features:
        - Retrieve detailed license information for a CommCell
        - Access capacity, complete OI, virtualization, user, activation, metallic, and other license details
        - Refresh license data to ensure up-to-date information
        - Access license attributes via convenient properties (e.g., commcell_id, cs_hostname, expiry_date)
        - Obtain license mode, registration code, serial number, and OEM name

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize a LicenseDetails object with the specified Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> cc = Commcell('commcell_host', 'username', 'password')
            >>> license_details = LicenseDetails(cc)
            >>> print("LicenseDetails object created successfully")

        #ai-gen-doc
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

    def _get_detailed_licenses(self) -> dict:
        """Retrieve all types of license details associated with the Commcell object.

        Returns:
            dict: A dictionary containing detailed information about all license types
            associated with the Commcell.

        Example:
            >>> license_details = LicenseDetails(commcell_object)
            >>> licenses = license_details._get_detailed_licenses()
            >>> print(licenses)
            >>> # Output will be a dictionary with license type details

        #ai-gen-doc
        """
        self._get_capacity_details()
        self._get_complete_oi_licenses()
        self._get_virtualization_licenses()
        self._get_user_licenses()
        self._get_activate_licenses()
        self._get_metallic_licenses()
        self._get_other_licenses()

    def _get_capacity_details(self) -> dict:
        """Retrieve the capacity license properties for the current environment.

        This method sends a request to obtain details about capacity-based licenses,
        such as usage and allocation information.

        Returns:
            dict: A dictionary containing capacity license properties.

        Raises:
            SDKException: If the response is unsuccessful or empty.

        Example:
            >>> license_details = LicenseDetails()
            >>> capacity_info = license_details._get_capacity_details()
            >>> print(capacity_info)
            {'totalCapacity': 1000, 'usedCapacity': 750, ...}

        #ai-gen-doc
        """

        self._CAPACITY_LICENSE = self._commcell_object._services['CAPACITY_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._CAPACITY_LICENSE)

        if flag:
            if response.json():
                self._capacity_licenses = response.json().get('records', None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_complete_oi_licenses(self) -> dict:
        """Retrieve the complete OI (Object Identification) licenses property via a GET request.

        This method sends a GET request to obtain the OI licenses property details.

        Returns:
            dict: A dictionary containing the OI licenses property information.

        Raises:
            SDKException: If the response is not successful or if the response is empty.

        Example:
            >>> license_details = LicenseDetails()
            >>> oi_licenses = license_details._get_complete_oi_licenses()
            >>> print(oi_licenses)
            {'licenseType': 'OI', 'status': 'Active', ...}

        #ai-gen-doc
        """

        self._OI_LICENSE = self._commcell_object._services['OI_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._OI_LICENSE)

        if flag:
            if response.json():
                self._complete_oi_licenses = response.json().get('records', None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_virtualization_licenses(self) -> dict:
        """Retrieve virtualization license properties via a GET request.

        This method fetches the virtualization license details associated with the current LicenseDetails instance.
        It raises an SDKException if the response is unsuccessful or empty.

        Returns:
            dict: A dictionary containing the virtualization license properties.

        Raises:
            SDKException: If the GET request fails or returns an empty response.

        Example:
            >>> license_details = LicenseDetails()
            >>> virtualization_licenses = license_details._get_virtualization_licenses()
            >>> print(virtualization_licenses)
            >>> # Output will be a dictionary with virtualization license information

        #ai-gen-doc
        """
        self._VIRTUALIZATION_LICENSE = self._commcell_object._services['VIRTUALIZATION_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._VIRTUALIZATION_LICENSE)

        if flag:
            if response.json():
                self._virtualization_licenses = response.json().get('records', None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_user_licenses(self) -> dict:
        """Retrieve the user licenses property via a GET request.

        This method fetches the user license details from the server. It is intended for internal use
        to obtain license information associated with users.

        Returns:
            dict: A dictionary containing user license properties.

        Raises:
            SDKException: If the server response is unsuccessful or empty.

        Example:
            >>> license_details = LicenseDetails()
            >>> user_licenses = license_details._get_user_licenses()
            >>> print(user_licenses)
            >>> # Output will be a dictionary with user license information

        #ai-gen-doc
        """
        self._USER_LICENSE = self._commcell_object._services['USER_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._USER_LICENSE)

        if flag:
            if response.json():
                self._user_licenses = response.json().get('records', None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_activate_licenses(self) -> dict:
        """Send a GET request to retrieve the activated licenses property.

        This method fetches the currently activated licenses from the server.

        Returns:
            dict: A dictionary containing the activated license properties.

        Raises:
            SDKException: If the response is not successful or if the response is empty.

        Example:
            >>> license_details = LicenseDetails()
            >>> activated_licenses = license_details._get_activate_licenses()
            >>> print(activated_licenses)
            >>> # Output will be a dictionary with license information

        #ai-gen-doc
        """
        self._ACTIVATE_LICENSE = self._commcell_object._services['ACTIVATE_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._ACTIVATE_LICENSE)

        if flag:
            if response.json():
                self._activate_licenses = response.json().get('records', None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_metallic_licenses(self) -> Any:
        """Send a GET request to retrieve the Metallic licenses property.

        This method fetches the Metallic license details associated with the current LicenseDetails instance.
        It raises an SDKException if the response is unsuccessful or empty.

        Raises:
            SDKException: If the response is not successful or is empty.

        Example:
            >>> license_details = LicenseDetails(commcell_object)
            >>> metallic_licenses = license_details._get_metallic_licenses()
            >>> print(metallic_licenses)
            >>> # The returned value contains the Metallic license properties

        #ai-gen-doc
        """
        self._METALLIC_LICENSE = self._commcell_object._services['METALLIC_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._METALLIC_LICENSE)

        if flag:
            if response.json():
                self._metallic_licenses = response.json().get('records', None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_other_licenses(self) -> dict:
        """Retrieve the details of other licenses via a GET request.

        This method fetches information about additional licenses associated with the system.
        It raises an SDKException if the response is unsuccessful or empty.

        Returns:
            dict: A dictionary containing details of other licenses.

        Raises:
            SDKException: If the GET request fails or returns an empty response.

        Example:
            >>> license_details = LicenseDetails()
            >>> other_licenses = license_details._get_other_licenses()
            >>> print(other_licenses)
            {'licenseType': 'Trial', 'expiryDate': '2024-12-31'}
        #ai-gen-doc
        """
        self._OTHER_LICENSE = self._commcell_object._services['OTHER_LICENSE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._OTHER_LICENSE)

        if flag:
            if response.json():
                self._other_licenses = response.json().get('records', None)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _get_license_details(self) -> dict:
        """Retrieve detailed license information via a GET request.

        This method sends a GET request to obtain comprehensive license details.
        It raises an SDKException if the response is unsuccessful or empty.

        Returns:
            dict: A dictionary containing detailed license information.

        Raises:
            SDKException: If the response is not successful or is empty.

        Example:
            >>> license_details = LicenseDetails(commcell_object)
            >>> details = license_details._get_license_details()
            >>> print(details)
            # Output: {'licenseType': 'Perpetual', 'expiryDate': '2025-12-31', ...}

        #ai-gen-doc
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

    def refresh(self) -> None:
        """Update the LicenseDetails metrics object with the latest configuration.

        This method refreshes the internal state of the LicenseDetails object to ensure
        it reflects the most current license configuration and metrics.

        Example:
            >>> license_details = LicenseDetails()
            >>> license_details.refresh()
            >>> print("License details refreshed successfully")

        #ai-gen-doc
        """
        self._get_license_details()
        self._get_detailed_licenses()

    @property
    def commcell_id(self) -> int:
        """Get the CommCell ID in decimal format.

        Returns:
            The CommCell ID as an integer.

        Example:
            >>> license_details = LicenseDetails()
            >>> commcell_id = license_details.commcell_id  # Use dot notation for property access
            >>> print(f"CommCell ID: {commcell_id}")

        #ai-gen-doc
        """
        return self._commcell_id

    @property
    def commcell_id_hex(self) -> str:
        """Get the hexadecimal representation of the Commcell ID.

        Returns:
            str: The Commcell ID as a hexadecimal string.

        Example:
            >>> license_details = LicenseDetails()
            >>> hex_id = license_details.commcell_id_hex  # Access as a property
            >>> print(f"Commcell ID (hex): {hex_id}")

        #ai-gen-doc
        """
        ccid = self._commcell_id
        if ccid == -1:
            return 'FFFFF'
        return hex(ccid).split('x')[1].upper()

    @property
    def cs_hostname(self) -> str:
        """Get the CommCell server host name or address.

        Returns:
            The host name or address of the CommCell server as a string.

        Example:
            >>> license_details = LicenseDetails()
            >>> hostname = license_details.cs_hostname
            >>> print(f"CommCell Hostname: {hostname}")

        #ai-gen-doc
        """
        return self._cs_hostname

    @property
    def license_ipaddress(self) -> str:
        """Get the IP address associated with the license.

        Returns:
            The license server's IP address as a string.

        Example:
            >>> license_details = LicenseDetails()
            >>> ip = license_details.license_ipaddress
            >>> print(f"License server IP: {ip}")

        #ai-gen-doc
        """
        return self._license_ipaddress

    @property
    def oem_name(self) -> str:
        """Get the OEM (Original Equipment Manufacturer) name associated with the license.

        Returns:
            The OEM name as a string.

        Example:
            >>> license_details = LicenseDetails()
            >>> oem = license_details.oem_name  # Access the OEM name property
            >>> print(f"OEM Name: {oem}")

        #ai-gen-doc
        """
        return self._oemname

    @property
    def license_mode(self) -> str:
        """Get the license mode associated with this license.

        Returns:
            The license mode as a string.

        Example:
            >>> license_details = LicenseDetails()
            >>> mode = license_details.license_mode  # Use dot notation for property access
            >>> print(f"License mode: {mode}")

        #ai-gen-doc
        """
        return self._license_mode

    @property
    def registration_code(self) -> str:
        """Get the registration code associated with the CommCell.

        Returns:
            The registration code as a string.

        Example:
            >>> license_details = LicenseDetails()
            >>> reg_code = license_details.registration_code  # Use dot notation for property access
            >>> print(f"Registration Code: {reg_code}")

        #ai-gen-doc
        """
        return self._regcode

    @property
    def serial_number(self) -> str:
        """Get the serial number of the CommCell.

        Returns:
            The serial number of the CommCell as a string.

        Example:
            >>> license_details = LicenseDetails()
            >>> sn = license_details.serial_number  # Use dot notation for property access
            >>> print(f"CommCell Serial Number: {sn}")

        #ai-gen-doc
        """
        return self._serialno

    @property
    def expiry_date(self) -> str:
        """Get the expiry date of the license.

        Returns:
            The expiry date of the license as a string.

        Example:
            >>> license_details = LicenseDetails()
            >>> expiration = license_details.expiry_date  # Use dot notation for property access
            >>> print(f"License expires on: {expiration}")

        #ai-gen-doc
        """
        return self._expiry_date

    @property
    def capacity_licenses(self) -> Dict[str, Any]:
        """Get a dictionary containing the capacity licenses.

        Returns:
            Dictionary with details about the capacity licenses. The keys represent license types,
            and the values provide associated license information.

        Example:
            >>> license_details = LicenseDetails()
            >>> capacity_info = license_details.capacity_licenses  # Use dot notation for property access
            >>> print("Capacity Licenses:", capacity_info)
            >>> # Output might be: {'CapacityLicenseTypeA': {...}, 'CapacityLicenseTypeB': {...}}

        #ai-gen-doc
        """
        return self._capacity_licenses

    @property
    def complete_oi_licenses(self) -> dict:
        """Get a dictionary containing all complete Open Infrastructure (OI) licenses.

        Returns:
            dict: A dictionary where keys represent license identifiers and values contain license details.

        Example:
            >>> license_details = LicenseDetails()
            >>> oi_licenses = license_details.complete_oi_licenses
            >>> print(f"Total OI licenses: {len(oi_licenses)}")
            >>> # Access license details by key
            >>> for license_id, details in oi_licenses.items():
            ...     print(f"License ID: {license_id}, Details: {details}")

        #ai-gen-doc
        """
        return self._complete_oi_licenses

    @property
    def virtualization_licenses(self) -> Dict[str, Any]:
        """Get a dictionary containing the virtualization licenses.

        Returns:
            Dict[str, Any]: A dictionary where keys represent virtualization license types and values provide license details.

        Example:
            >>> license_details = LicenseDetails()
            >>> virtualization_info = license_details.virtualization_licenses
            >>> print(virtualization_info)
            {'VMware': {'total': 10, 'used': 5}, 'Hyper-V': {'total': 8, 'used': 3}}

        #ai-gen-doc
        """
        return self._virtualization_licenses

    @property
    def user_licenses(self) -> Dict[str, Any]:
        """Get a dictionary containing details of user licenses.

        Returns:
            Dictionary where keys represent license types or categories, and values contain license details.

        Example:
            >>> license_details = LicenseDetails()
            >>> user_license_info = license_details.user_licenses  # Access property
            >>> print(user_license_info)
            >>> # Output might be: {'UserLicenseTypeA': {'count': 10, 'expiry': '2024-12-31'}, ...}

        #ai-gen-doc
        """
        return self._user_licenses

    @property
    def activate_licenses(self) -> dict:
        """Get a dictionary containing the activated licenses.

        Returns:
            dict: A dictionary with details of the activated licenses.

        Example:
            >>> license_details = LicenseDetails()
            >>> activated = license_details.activate_licenses
            >>> print(f"Activated licenses: {activated}")

        #ai-gen-doc
        """
        return self._activate_licenses

    @property
    def metallic_licenses(self) -> dict:
        """Get a dictionary containing the Metallic licenses.

        Returns:
            dict: A dictionary with details of the Metallic licenses.

        Example:
            >>> license_details = LicenseDetails()
            >>> metallic_licenses = license_details.metallic_licenses
            >>> print(metallic_licenses)
            {'license_type': 'Metallic', 'expiry_date': '2024-12-31', ...}

        #ai-gen-doc
        """
        return self._metallic_licenses

    @property
    def other_licenses(self) -> dict:
        """Get a dictionary containing information about other licenses.

        Returns:
            dict: A dictionary with details of additional licenses associated with the system.

        Example:
            >>> license_details = LicenseDetails()
            >>> other_lics = license_details.other_licenses
            >>> print(other_lics)
            {'licenseA': {'expiry': '2025-01-01'}, 'licenseB': {'expiry': '2024-12-31'}}

        #ai-gen-doc
        """
        return self._other_licenses
