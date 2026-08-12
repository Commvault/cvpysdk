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

"""Main file for performing threat/file type analysis on clients/laptops

Resources and Resource are 2 classes defined in this file

Resources class is derived from TAServers class
Resource class is derived from TAServer class


Resources: Class for representing all the servers in threat detection page
Resource: Class for representing a single server in threat detection page

Resources:
    __init__() --  initializes the Resources class object

Resource:
    __init__() --  initializes the Resource class object
    run_scan() -- Run anomaly scan on the Threat Anomaly Server
    disable_data_aging() -- Disable data aging for the Threat Anomaly Server
    enable_data_aging() -- Enable data aging for the Threat Anomaly Server



"""
from ..monitoringapps.threat_indicators import TAServers, TAServer

class Resources(TAServers):
    """
    Represents and manages all the servers involved in threat detection.
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize a new instance of the Resources class.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.
        """
        super().__init__(commcell_object)
        self._commcell_object = commcell_object


class Resource(TAServer):
    """
    Represents and manages a single server involved in threat detection.
    """

    def __init__(self, commcell_object: object, server_name: str) -> None:
        """
        Initialize a new instance of the Resource class.
        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.
            server_name: Name of the server involved in threat detection.

        """
        super().__init__(commcell_object, server_name)

    def run_scan(self,anomaly_types: list,
        index_server_name: str = None,
        storage_pool: str = None,
        from_time: int = None,
        to_time: int = None):

        """Run anomaly scan on the Threat Anomaly Server
        Args:
            anomaly_types (list): List of anomaly types to scan for.
            index_server_name (str, optional): Name of the index server to use for the scan. Defaults to None.
            storage_pool (str, optional): Name of the storage pool to use for the scan. Defaults to None.
            from_time (int, optional): Start time for the scan in epoch format. Defaults to None.
            to_time (int, optional): End time for the scan in epoch format. Defaults to None.

        Returns:
            The job ID (int) of the launched scan job.

        Raises:
            SDKException: If the job fails to start or if input data types are invalid.
        ."""
        return self._commcell_object.threat_indicators.run_scan(
            self._server_name,
            anomaly_types,
            index_server_name,
            storage_pool,
            from_time,
            to_time
        )

    def disable_data_aging(self):
        """Disable data aging for the Threat Anomaly Server."""
        self._commcell_object.clients.get(self._server_name).disable_data_aging()

    def enable_data_aging(self):
        """Enable data aging for the Threat Anomaly Server."""
        self._commcell_object.clients.get(self._server_name).enable_data_aging()