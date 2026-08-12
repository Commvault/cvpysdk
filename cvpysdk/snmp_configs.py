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

""" File for managing SNMP Configurations in Commcell """
import base64
from typing import Any
from .exception import SDKException


class SNMPConfigurations:
    """
    Class for managing SNMP (Simple Network Management Protocol) configurations within a Commcell environment.

    This class provides a comprehensive interface for handling SNMP configuration tasks, including adding,
    updating, deleting, and retrieving SNMP configurations. It interacts with the Commcell object to
    maintain and synchronize SNMP settings across the system.

    Key Features:
        - Initialize with a Commcell object for context-aware operations
        - Refresh and synchronize SNMP configuration data
        - Retrieve all SNMP configurations via the `all_configs` property
        - Add new SNMP configurations with specified hostnames and credentials
        - Update existing SNMP configurations, including hostname and credentials changes
        - Delete SNMP configurations by hostname
        - Internal support for configuration updates and retrieval

    Usage:
        Instantiate with a Commcell object and use provided methods to manage SNMP configurations.

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize the SNMPConfigurations class with a Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> snmp_config = SNMPConfigurations(commcell)
            >>> print("SNMPConfigurations object created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._update_response_ = commcell_object._update_response_
        self._SNMP = self._commcell_object._services['SNMP']
        self._SNMP_CONFIG = self._commcell_object._services['SNMP_CONFIG']
        self._configs = None
        self.encrypt_algo_ids = {
            "HMAC_MD5": 1,
            "HMAC_SHA": 2,
            "HMAC128_SHA224": 3,
            "HMAC192_SHA256": 4,
            "HMAC256_SHA384": 5,
            "HMAC384_SHA512": 6
        }
        self.privacy_algo_ids = {
            "None": 0,
            "CBC_DES": 1,
            "CFB128_AES128": 2,
            "CBC_AES128": 3
        }
        self.encrypt_algo_names = {v: k for k, v in self.encrypt_algo_ids.items()}
        self.privacy_algo_names = {v: k for k, v in self.privacy_algo_ids.items()}

    def refresh(self) -> None:
        """Reload all SNMP configuration data associated with the current object.

        This method clears any cached SNMP configuration information, ensuring that subsequent accesses
        retrieve the most up-to-date data.

        Example:
            >>> snmp_configs = SNMPConfigurations(commcell_object)
            >>> snmp_configs.refresh()  # Refresh SNMP configuration cache
            >>> print("SNMP configurations reloaded successfully")

        #ai-gen-doc
        """
        self._configs = None

    def _get_all_configs(self) -> dict:
        """Retrieve all SNMP configurations present in the Commcell.

        Returns:
            dict: A dictionary containing all SNMP configuration details, 
            where each key is the configuration name and the value is its corresponding configuration data.

        Example:
            >>> snmp_configs = snmp_configurations._get_all_configs()
            >>> print(f"Total SNMP configurations: {len(snmp_configs)}")
            >>> for name, config in snmp_configs.items():
            ...     print(f"Config Name: {name}, Details: {config}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._SNMP_CONFIG
        )
        if flag:
            if response and "snmv3InfoList" in response.json():
                return {
                    config["hostName"]: {
                        'privacy_algorithm':  self.privacy_algo_names[config["privacyAlgorithm"]],
                        'authentication_algorithm': self.encrypt_algo_names[config["encryptAlgorithm"]],
                        'id': config["id"],
                        'user_name': config["userAccount"]["userName"],
                    }
                    for config in response.json()["snmv3InfoList"]
                }
            else:
                return {}
        response_string = self._update_response_(response.content)
        raise SDKException('Response', '101', response_string)

    @property
    def all_configs(self) -> dict:
        """Get all SNMP configurations available in the Commcell.

        Returns:
            dict: A dictionary containing all SNMP configuration details, where each key is a configuration name and the value is its corresponding configuration data.

        Example:
            >>> snmp_configs = SNMPConfigurations(commcell_object)
            >>> configs = snmp_configs.all_configs
            >>> print(f"Total SNMP configurations: {len(configs)}")
            >>> for name, config in configs.items():
            ...     print(f"Config Name: {name}, Details: {config}")

        #ai-gen-doc
        """
        if self._configs is None:
            self._configs = self._get_all_configs()
        return self._configs

    def _update_config(self, optype: int, config_hostname: str, username: str, password: str = '', **kwargs: Any) -> None:
        """Update the SNMP configuration in the Commcell.

        This method updates SNMP configuration settings for a specified host in the Commcell.
        The operation type determines whether the configuration is added, deleted, or updated.
        Additional SNMP parameters can be provided as keyword arguments.

        Args:
            optype: Operation type for the SNMP configuration.
                - 1: Add configuration
                - 2: Delete configuration
                - 3: Update configuration
            config_hostname: Hostname of the SNMP configuration to update.
            username: Username for the SNMP configuration.
            password: Password for the SNMP configuration. Defaults to an empty string.
            **kwargs: Optional SNMP configuration parameters, such as:
                - authentication_algorithm: Authentication algorithm (default: 'HMAC_MD5')
                - privacy_algorithm: Privacy algorithm (default: None)
                - privacy_password: Privacy password (default: None)

        Example:
            >>> snmp_configs = SNMPConfigurations()
            >>> snmp_configs._update_config(
            ...     optype=1,
            ...     config_hostname='snmp-server01',
            ...     username='admin',
            ...     password='secret',
            ...     authentication_algorithm='HMAC_SHA',
            ...     privacy_algorithm='AES',
            ...     privacy_password='privpass'
            ... )
            >>> print("SNMP configuration updated successfully.")

        #ai-gen-doc
        """
        payload = {
            "snmv3ConfigOperationType": optype,
            "snmv3Info": {
                "hostName": config_hostname,
                "encryptAlgorithm": self.encrypt_algo_ids[kwargs.get("authentication_algorithm", "HMAC_MD5")],
                "privacyAlgorithm": 0,
                "privacyCredentials": False,
                "userAccount": {
                    "userName": username
                }
            }
        }
        if optype == 3:
            payload["snmv3Info"]["id"] = kwargs.get('id')
        if password:
            payload["snmv3Info"]["userAccount"]["password"] = base64.b64encode(password.encode()).decode()
        if (priv_algo := kwargs.get("privacy_algorithm")) not in ["None", None]:
            payload["snmv3Info"]["privacyCredentials"] = True
            payload["snmv3Info"]["privacyAlgorithm"] = self.privacy_algo_ids[priv_algo]
            if priv_pass := kwargs.get("privacy_password"):
                payload["snmv3Info"]["privacyPassword"] = base64.b64encode(priv_pass.encode()).decode()
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._SNMP_CONFIG, payload
        )
        if flag:
            if response.json():
                self.refresh()
                return
            else:
                raise SDKException('Commcell', '101', f'Failed to update SNMP configuration: {config_hostname}')
        response_string = self._update_response_(response.content)
        raise SDKException('Response', '101', response_string)

    def add(self, config_hostname: str, username: str, password: str, **kwargs: str) -> None:
        """Add a new SNMP configuration to the Commcell.

        This method creates a new SNMP configuration entry with the specified host, username, and password.
        Additional SNMP parameters such as authentication and privacy algorithms can be provided as keyword arguments.

        Args:
            config_hostname: Host name of the SNMP configuration.
            username: Username for the SNMP configuration.
            password: Password for the SNMP configuration.
            **kwargs: Optional keyword arguments for advanced SNMP settings:
                - authentication_algorithm (str): Authentication algorithm (default: 'HMAC_MD5').
                - privacy_algorithm (str): Privacy algorithm (default: None).
                - privacy_password (str): Privacy password for the SNMP configuration.

        Example:
            >>> snmp_configs = SNMPConfigurations()
            >>> snmp_configs.add(
            ...     config_hostname="snmp-server01",
            ...     username="snmpuser",
            ...     password="snmppass",
            ...     authentication_algorithm="HMAC_SHA",
            ...     privacy_algorithm="AES",
            ...     privacy_password="privpass"
            ... )
            >>> print("SNMP configuration added successfully.")

        #ai-gen-doc
        """
        self._update_config(1, config_hostname, username, password, **kwargs)

    def update(self, config_hostname: str, new_config_hostname: str = None, username: str = None, password: str = '', **kwargs: Any) -> None:
        """Update an existing SNMP configuration in the Commcell.

        This method updates the details of an existing SNMP configuration, such as the host name,
        username, password, and optional SNMP security parameters.

        Args:
            config_hostname: The current host name of the SNMP configuration to be updated.
            new_config_hostname: The new host name to assign to the SNMP configuration (optional).
            username: The username to update for the SNMP configuration (optional).
            password: The password to update for the SNMP configuration (optional; defaults to empty string).
            **kwargs: Additional SNMP security parameters. Supported keys include:
                - authentication_algorithm (str): Authentication algorithm (default: 'HMAC_MD5').
                - privacy_algorithm (str): Privacy algorithm (default: None).
                - privacy_password (str): Privacy password (default: None).

        Example:
            >>> snmp_configs = SNMPConfigurations(commcell_object)
            >>> snmp_configs.update(
            ...     config_hostname='old-snmp-host',
            ...     new_config_hostname='new-snmp-host',
            ...     username='snmpuser',
            ...     password='snmppass',
            ...     authentication_algorithm='HMAC_SHA',
            ...     privacy_algorithm='AES',
            ...     privacy_password='privpass'
            ... )
            >>> print("SNMP configuration updated successfully.")

        #ai-gen-doc
        """
        if config_hostname not in self.all_configs:
            raise SDKException('Commcell', '102', 'Configuration {0} does not exist'.format(config_hostname))
        old = self.all_configs[config_hostname]
        self._update_config(
            3,
            new_config_hostname or config_hostname,
            username or old['user_name'],
            password,
            id=old['id'],
            authentication_algorithm=kwargs.get("authentication_algorithm", old['authentication_algorithm']),
            privacy_algorithm=kwargs.get("privacy_algorithm", old['privacy_algorithm']),
            privacy_password=kwargs.get("privacy_password", ''),
        )

    def delete(self, config_hostname: str) -> None:
        """Delete an SNMP configuration from the Commcell.

        Removes the specified SNMP configuration identified by its hostname from the Commcell system.

        Args:
            config_hostname: The hostname of the SNMP configuration to be deleted.

        Example:
            >>> snmp_configs = SNMPConfigurations(commcell_object)
            >>> snmp_configs.delete("snmp-server-01")
            >>> print("SNMP configuration deleted successfully.")

        #ai-gen-doc
        """
        if config_hostname not in self.all_configs:
            raise SDKException('Commcell', '102', 'Configuration {0} does not exist'.format(config_hostname))
        self._update_config(
            2,
            config_hostname,
            self.all_configs[config_hostname]['user_name'],
            authentication_algorithm=self.all_configs[config_hostname]['authentication_algorithm'],
            privacy_algorithm=self.all_configs[config_hostname]['privacy_algorithm'],
        )
