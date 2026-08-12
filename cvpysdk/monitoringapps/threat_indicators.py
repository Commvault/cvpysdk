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

TAServers , TAServer, AnomalyType are the three classes defined in this file

TAServers - class to represent all servers in threat indicators

TAServer  - class to represent single server in threat indicators

AnomalyType - class to represent different types of anomaly

TAServers:

    __init__()                          --  initialise object of the TAServers class

    _get_clients_count()                --  returns total client on threat indicators for this CS

    _get_monitored_vm_count()           --  returns monitored vm count on threat indicators for this CS

    _get_threat_indicators()            --  returns the list of threat indicators client for this CS

    _response_not_success()             --  parses through the exception response, and raises SDKException

    refresh()                           --  refreshes the threat indicators servers for this CS

    has()                               --  Checks whether given server name exists in threat indicators or not

    get()                               --  returns the server class object for given server name

    run_scan()                          --  runs anomaly scan on given server

TAServers Attributes:

    **clients_count**       --  returns the total clients stats from threat indicators from CS

    **monitored_vms**       --  returns the monitored vms stats from threat indicators from CS

TAServer:

    __init__()                          --  initialise object of the TAServer class

    _get_anomalies_stats()              --  returns the anomalies stats for this client

    _get_anomaly_records()              --  returns list containing files anomaly record details of this client

    _response_not_success()             --  parses through the exception response, and raises SDKException

    refresh()                           --  refreshes the server anomalies

    clear_anomaly()                     --  clears the anomalies present for this client

Server Attributes:

    **anomaly_records**             --  returns the list of anomaly records for this client

    **threat_anomaly_stats**        --  returns the dict of threat anomalies stats for this client

    **anomaly_stats**               --  returns the dict of file types/data anomalies stats for this client

    **datasource_id**               --  associated data source id for threat scan / analysis server

    **anomaly_file_count**          --  returns the total anomaly file count for this client


"""
import copy
import datetime
import enum
import time

from ..exception import SDKException
from ..monitoringapps.constants import ThreatConstants, FileTypeConstants, RequestConstants


class AnomalyType(enum.Enum):
    """
    Enumeration class representing different types of anomalies.

    This class is used to define and categorize anomaly types in a structured
    and type-safe manner. It inherits from Python's enum.Enum, allowing for
    clear and consistent usage of anomaly categories throughout the codebase.

    Key Features:
        - Provides a set of predefined anomaly types
        - Ensures type safety and clarity when working with anomalies
        - Facilitates easy comparison and usage in control flow

    #ai-gen-doc
    """
    FILE_ACTIVITY = 16
    FILE_TYPE = 32
    THREAT_ANALYSIS = 64
    FILE_DATA = 128
    EXTENSION_BASED = 512
    DATA_WRITTEN = 4096


class TAServers():
    """
    Represents and manages all servers involved in threat indicator monitoring.

    This class provides an interface for interacting with servers that are part of a threat analysis system.
    It allows users to query server details, monitor virtual machines, retrieve threat indicators, and
    initiate scans for anomalies. The class also supports refreshing server data and checking for the
    existence of specific servers.

    Key Features:
        - Initialization with a communication cell object for server context
        - Error handling for unsuccessful responses
        - Retrieval of client and monitored VM counts
        - Access to threat indicators for servers
        - Check for existence of a server by name
        - Run scans for specified anomaly types within a time range
        - Retrieve server details by name
        - Refresh server data to ensure up-to-date information
        - Properties for monitored VMs and client count

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize a new instance of the TAServers class.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> ta_servers = TAServers(commcell)
            >>> print("TAServers instance created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._threat_indicators = []
        self._servers = []
        self._total_clients = None
        self._monitored_vms = None
        self._API_GET_ALL_INDICATORS = self._services['GET_THREAT_INDICATORS']
        self._API_RUN_SCAN = self._services['RUN_ANOMALY_SCAN']
        self._API_CLIENTS_COUNT = self._services['ANOMALY_CLIENTS_COUNT']
        self._API_MONITORED_VMS = self._services['MONITORED_VM_COUNT']
        self.refresh()

    def _response_not_success(self, response: object) -> None:
        """Raise an exception if the API response status is not 200 (OK).

        This helper function checks the status of the provided response object,
        typically obtained from the `requests` Python package, and raises an
        exception if the response indicates a failure (i.e., status code is not 200).

        Args:
            response: The response object returned from an API request.

        Example:
            >>> response = requests.get('https://api.example.com/data')
            >>> taservers = TAServers()
            >>> taservers._response_not_success(response)
            >>> # If the response status is not 200, an exception will be raised.

        #ai-gen-doc
        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_clients_count(self) -> dict:
        """Retrieve the client count statistics for Threat Indicators on this CommServe.

        Returns:
            dict: A dictionary containing total client statistics, including counts for each client type 
            such as 'fileserver', 'vm', and 'laptop'.

        Raises:
            SDKException: If the method fails to fetch the client count details.

        Example:
            >>> ta_servers = TAServers()
            >>> client_stats = ta_servers._get_clients_count()
            >>> print(client_stats)
            {'fileserver': 10, 'vm': 5, 'laptop': 3}

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._API_CLIENTS_COUNT)
        if flag:
            if response.json():
                return response.json()
            elif bool(response.json()):
                raise SDKException('ThreatIndicators', '110')
        self._response_not_success(response)

    def _get_monitored_vm_count(self) -> dict:
        """Retrieve the monitored virtual machine (VM) count statistics for threat indicators on this CommServe.

        Returns:
            dict: A dictionary containing statistics about the total number of monitored VMs for threat indicators.

        Raises:
            SDKException: If the method fails to fetch the monitored VM details.

        Example:
            >>> ta_servers = TAServers()
            >>> vm_stats = ta_servers._get_monitored_vm_count()
            >>> print(f"Total monitored VMs: {vm_stats.get('total_monitored_vms', 0)}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._API_MONITORED_VMS)
        if flag:
            if response.json():
                return response.json()
            elif bool(response.json()):
                raise SDKException('ThreatIndicators', '111')
        self._response_not_success(response)


    def _get_threat_indicators(self) -> list[dict]:
        """Retrieve the list of threat indicators for this CommServe (CS) server.

        Returns:
            list of dict: A list containing dictionaries with server threat details. Each dictionary
            includes information such as anomaly type, modification count, rename count, VM support,
            reference time, delete and create counts, location, OS information, and client details.

        Example:
            >>> ta_servers = TAServers()
            >>> indicators = ta_servers._get_threat_indicators()
            >>> print(f"Found {len(indicators)} threat indicators")
            >>> if indicators:
            ...     first = indicators[0]
            ...     print(f"First indicator anomaly type: {first['anomalyType']}")
            ...     print(f"Client name: {first['client']['clientName']}")

        Example threat indicator dictionary:
            {
                "anomalyType": 8,
                "modCount": 13705,
                "renameCount": 1,
                "isVMeSupported": True,
                "refTime": 1727519811,
                "deleteCount": 73280,
                "createCount": 19,
                "location": "",
                "osInfo": {
                    "osInfo": {
                        "Type": "Windows",
                        "SubType": "Server",
                        "osId": 210,
                        "OsDisplayInfo": {
                            "ProcessorType": "WinX64",
                            "OSName": "Windows Server 2019 Datacenter"
                        }
                    }
                },
                "client": {
                    "clientId": 9,
                    "clientName": "xx",
                    "displayName": "xx_dn"
                }
            }

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._API_GET_ALL_INDICATORS)
        _threat_indicators = []
        if flag:
            if response.json() and 'anomalyClients' in response.json():
                _threat_indicators = response.json()['anomalyClients']
                for _client in _threat_indicators:
                    if 'client' in _client:
                        _display_name = _client['client'].get('displayName', '')
                        self._servers.append(_display_name.lower())
            elif bool(response.json()):
                raise SDKException('ThreatIndicators', '103')
            return _threat_indicators
        self._response_not_success(response)

    def has(self, name: str) -> bool:
        """Check if the specified server name exists in the threat indicators.

        Args:
            name: The name of the server to check.

        Returns:
            True if the server name exists in the threat indicators, False otherwise.

        Example:
            >>> ta_servers = TAServers()
            >>> exists = ta_servers.has("server01")
            >>> print(f"Server exists: {exists}")
            # Output: Server exists: True

        #ai-gen-doc
        """
        if name.lower() in self._servers:
            return True
        return False

    def run_scan(
            self,
            server_name: str,
            anomaly_types: list,
            index_server_name: str = None,
            storage_pool: str = None,
            from_time: int = None,
            to_time: int = None
        ) -> int:
        """Run an anomaly scan on the specified server.

        This method initiates an anomaly scan for the given server, analyzing the specified anomaly types.
        Optionally, you can specify an index server, storage pool, and a time range for the scan.

        Args:
            server_name: The name of the server to analyze.
            anomaly_types: List of anomaly types to analyze on the client.
            index_server_name: (Optional) Index server name to be used for the scan. Applicable for all OEMs except Metallic.
            storage_pool: (Optional) Storage pool name to be used for the scan. Applicable only for Metallic OEM.
            from_time: (Optional) Epoch timestamp indicating the start time for the scan analysis.
            to_time: (Optional) Epoch timestamp indicating the end time for the scan analysis.

        Returns:
            The job ID (int) of the launched scan job.

        Raises:
            SDKException: If the job fails to start or if input data types are invalid.

        Example:
            >>> ta_servers = TAServers()
            >>> job_id = ta_servers.run_scan(
            ...     server_name="Server01",
            ...     anomaly_types=["ransomware", "suspicious_activity"],
            ...     index_server_name="IndexServerA",
            ...     from_time=1672531200,
            ...     to_time=1672617600
            ... )
            >>> print(f"Anomaly scan job started with ID: {job_id}")

        #ai-gen-doc
        """
        if not isinstance(server_name, str):
            raise SDKException('ThreatIndicators', '101')
        if not isinstance(anomaly_types, list):
            raise SDKException('ThreatIndicators', '101')
        if not self._commcell_object.clients.has_client(server_name):
            raise SDKException('ThreatIndicators', '102', 'Given server is not found in CS')
        if storage_pool and index_server_name:
            raise SDKException('ThreatIndicators', '102', 'Cannot specify both storage_pool and index_server_name input')
        req_json = copy.deepcopy(RequestConstants.RUN_SCAN_JSON)
        req_json['client']['clientId'] = int(self._commcell_object.clients.get(server_name).client_id)
        ta_flag = 0
        for each_anomaly in anomaly_types:
            if each_anomaly.name == AnomalyType.FILE_DATA.name:
                ta_flag = ta_flag + 2
            elif each_anomaly.name == AnomalyType.THREAT_ANALYSIS.name:
                ta_flag = ta_flag + 1
        req_json['threatAnalysisFlags'] = int(ta_flag)
        if not from_time and not to_time:
            to_time = int(time.time())
            req_json['timeRange']['toTime'] = int(to_time)
            to_time = datetime.datetime.fromtimestamp(to_time)
            from_time = to_time - datetime.timedelta(days=7)
            req_json['timeRange']['fromTime'] = int(from_time.timestamp())
        else:
            req_json['timeRange']['toTime'] = to_time
            req_json['timeRange']['fromTime'] = from_time
        if storage_pool:
            req_json.pop('indexServer')
            spool_obj = self._commcell_object.storage_pools.get(storage_pool)
            req_json['backupDetails'][0]['copyId'] = int(spool_obj.copy_id)
            req_json['backupDetails'][0]['storagePoolId'] = int(spool_obj.storage_pool_id)
        else:
            req_json.pop('backupDetails')
            if not index_server_name:
                raise SDKException('ThreatIndicators', '108')
            req_json['indexServer']['clientId'] = int(
                self._commcell_object.index_servers.get(index_server_name).index_server_client_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._API_RUN_SCAN, req_json
        )
        if flag:
            if response.json() and 'jobId' in response.json():
                return response.json()['jobId']
            raise SDKException('ThreatIndicators', '109')
        self._response_not_success(response)

    def get(self, server_name: str) -> 'TAServer':
        """Retrieve a Server object for the specified server name.

        Args:
            server_name: The name of the server (client) to retrieve.

        Returns:
            Server: An instance of the Server class corresponding to the given server name.

        Raises:
            SDKException: If the server cannot be found or if the input is invalid.

        Example:
            >>> ta_servers = TAServers()
            >>> server = ta_servers.get("MyServer01")
            >>> print(f"Retrieved server: {server}")

        #ai-gen-doc
        """
        if not isinstance(server_name, str):
            raise SDKException('ThreatIndicators', '101')
        if not self.has(server_name):
            raise SDKException('ThreatIndicators', '105')
        return TAServer(commcell_object=self._commcell_object, server_name=server_name)

    def refresh(self) -> None:
        """Reload the list of threat indicator servers associated with the CommServe (CS).

        This method refreshes the internal cache of threat indicator servers, ensuring that 
        any changes made on the CommServe are reflected in the TAServers instance.

        Example:
            >>> ta_servers = TAServers(commcell_object)
            >>> ta_servers.refresh()  # Updates the list of threat indicator servers
            >>> print("Threat indicator servers refreshed successfully")

        #ai-gen-doc
        """
        self._servers = []
        self._total_clients = None
        self._monitored_vms = None
        self._threat_indicators = self._get_threat_indicators()
        self._total_clients = self._get_clients_count()
        self._monitored_vms = self._get_monitored_vm_count()

    @property
    def monitored_vms(self) -> dict:
        """Get the monitored virtual machines (VMs) statistics from threat indicators on this CommServe.

        Returns:
            dict: A dictionary containing client statistics for monitored VMs.

        Example:
            >>> ta_servers = TAServers()
            >>> vm_stats = ta_servers.monitored_vms  # Use dot notation for property access
            >>> print(f"Number of monitored VMs: {len(vm_stats)}")
            >>> # Access specific VM stats
            >>> for vm_name, stats in vm_stats.items():
            ...     print(f"VM: {vm_name}, Stats: {stats}")

        #ai-gen-doc
        """
        return self._monitored_vms

    @property
    def clients_count(self) -> dict:
        """Get the client statistics from threat indicators on this CommServe.

        Returns:
            dict: A dictionary containing client statistics as reported by threat indicators.

        Example:
            >>> ta_servers = TAServers()
            >>> stats = ta_servers.clients_count
            >>> print(f"Number of clients: {stats.get('total_clients', 0)}")
            >>> # Access additional statistics as needed from the returned dictionary

        #ai-gen-doc
        """
        return self._total_clients



class TAServer:
    """
    Threat Anomaly Server management class.

    This class provides an interface for interacting with a Threat Anomaly Server,
    enabling retrieval and management of anomaly statistics and records. It allows
    users to refresh server data, clear specific anomaly types, and access various
    properties related to anomaly detection and data sources.

    Key Features:
        - Initialization with commcell object and server name
        - Handling of unsuccessful server responses
        - Retrieval of anomaly statistics and records
        - Refreshing server data to update anomaly information
        - Clearing anomalies by specified types
        - Access to anomaly records, threat anomaly statistics, and general anomaly statistics
        - Access to datasource ID and anomaly file count via properties

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object, server_name: str) -> None:
        """Initialize a new instance of the TAServer class.

        Args:
            commcell_object: An instance of the Commcell class representing the connection to the Commcell environment.
            server_name: The name of the server to be managed by this TAServer instance.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> ta_server = TAServer(commcell, 'MyServer')
            >>> print("TAServer instance created for:", ta_server)

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._server_name = server_name
        self._server_id = self._commcell_object.clients.get(server_name).client_id
        self._anomaly_records = None
        self._threat_anomaly_stats = None
        self._anomaly_stats = None
        self._threat_dsid = None
        self._API_GET_ALL_INDICATORS = self._services['GET_THREAT_INDICATORS']
        self._API_GET_ALL_ANOMALIES = self._services['GET_ALL_CLIENT_ANOMALIES']
        self._API_CLEAR_ANOMALIES = self._services['CLEAR_ANOMALIES']
        self.refresh()

    def _response_not_success(self, response: object) -> None:
        """Raise an exception if the API response status is not 200 (OK).

        This helper function is intended to be used after making an API request using the `requests` package.
        If the response status code is not 200, it raises an appropriate exception to indicate the failure.

        Args:
            response: The response object returned by the `requests` library after making an API call.

        Example:
            >>> response = requests.get('https://api.example.com/data')
            >>> server = TAServer()
            >>> server._response_not_success(response)
            >>> # If the response status is not 200, an exception will be raised

        #ai-gen-doc
        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_anomalies_stats(self) -> dict:
        """Retrieve the anomaly statistics for this client.

        Returns:
            dict: A dictionary containing anomaly statistics related to the client.

        Example:
            >>> stats = ta_server._get_anomalies_stats()
            >>> print(stats)
            >>> # Output might include keys such as 'anomaly_count', 'last_detected', etc.

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._API_GET_ALL_INDICATORS)
        threat_stats = {}
        stats = {}
        if flag:
            if response.json() and 'anomalyClients' in response.json():
                _resp = response.json()['anomalyClients']
                for _client in _resp:
                    if 'client' in _client:
                        if _client['client'].get('displayName', '').lower() == self._server_name.lower():
                            threat_stats[ThreatConstants.FIELD_INFECTED_COUNT] = _client.get(
                                ThreatConstants.FIELD_INFECTED_COUNT, 0)
                            threat_stats[ThreatConstants.FIELD_FINGERPRINT_COUNT] = _client.get(
                                ThreatConstants.FIELD_FINGERPRINT_COUNT, 0)
                            stats[FileTypeConstants.FIELD_CREATE_COUNT] = _client.get(
                                FileTypeConstants.FIELD_CREATE_COUNT, 0)
                            stats[FileTypeConstants.FIELD_DELETE_COUNT] = _client.get(
                                FileTypeConstants.FIELD_DELETE_COUNT, 0)
                            stats[FileTypeConstants.FIELD_MODIFIED_COUNT] = _client.get(
                                FileTypeConstants.FIELD_MODIFIED_COUNT, 0)
                            stats[FileTypeConstants.FIELD_RENAME_COUNT] = _client.get(
                                FileTypeConstants.FIELD_RENAME_COUNT, 0)
                            self._threat_dsid = _client.get('dataSourceId', 0)
            elif bool(response.json()):
                raise SDKException('ThreatIndicators', '103')
            return stats, threat_stats
        self._response_not_success(response)

    def _get_anamoly_records(self) -> list:
        """Retrieve file type anomaly records for this client.

        Returns:
            list: A list containing anomaly records related to file types for the client.

        Example:
            >>> ta_server = TAServer()
            >>> anomaly_records = ta_server._get_anamoly_records()
            >>> print(f"Number of anomaly records: {len(anomaly_records)}")
            >>> # Each record in the list represents a file type anomaly

        #ai-gen-doc
        """
        api = self._API_GET_ALL_ANOMALIES % (0, self._server_id)  # filter=0 to fetch all anomalies types
        flag, response = self._cvpysdk_object.make_request('GET', api)
        if flag:
            if response.json() and 'clientInfo' in response.json():
                _resp = response.json()['clientInfo'][0]
                if 'anomalyRecordList' in _resp:
                    return _resp['anomalyRecordList']
                else:
                    # for fingerprint analysis, record list will be empty
                    return []
            raise SDKException('ThreatIndicators', '104')
        self._response_not_success(response)

    def refresh(self) -> None:
        """Reload the anomaly details associated with this TAServer instance.

        This method refreshes the internal state to ensure that the latest anomaly information
        for the server is available. Use this method when you suspect that the anomaly data
        may have changed and you want to update the server's details.

        Example:
            >>> server = TAServer()
            >>> server.refresh()  # Updates the anomaly details for this server
            >>> print("Anomaly details refreshed successfully")
        #ai-gen-doc
        """
        self._threat_dsid = 0
        self._anomaly_records = self._get_anamoly_records()
        self._anomaly_stats, self._threat_anomaly_stats = self._get_anomalies_stats()

    def clear_anomaly(self, anomaly_types: list) -> None:
        """Clear specified anomalies for this server.

        Args:
            anomaly_types: List of anomalies to clear. Each item should correspond to an anomaly type 
                as defined in the AnomalyType class.

        Raises:
            SDKException: If clearing the anomaly fails or if the input is not valid.

        Example:
            >>> server = TAServer()
            >>> server.clear_anomaly([AnomalyType.CPU_SPIKE, AnomalyType.MEMORY_LEAK])
            >>> print("Selected anomalies cleared successfully.")

        #ai-gen-doc
        """
        if not isinstance(anomaly_types, list):
            raise SDKException('ThreatIndicators', '101')
        anomalies_to_clear = []
        for each_anomaly in anomaly_types:
            anomalies_to_clear.append(each_anomaly.name)
        _req_json = copy.deepcopy(RequestConstants.CLEAR_ANOMALY_JSON)
        _req_json['clients'][0]['clientId'] = int(self._server_id)
        _req_json['clients'][0]['displayName'] = self._server_name
        _req_json['anomalyTypes'] = anomalies_to_clear
        if AnomalyType.FILE_DATA.name in anomalies_to_clear or AnomalyType.THREAT_ANALYSIS.name in anomalies_to_clear:
            _req_json['clients'][0]['dataSourceId'] = self.datasource_id
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._API_CLEAR_ANOMALIES, _req_json
        )
        if flag:
            if response.json() and 'error' in response.json():
                response = response.json()['error']
                if 'errorCode' in response and response['errorCode'] != 0:
                    raise SDKException(
                        'ThreatIndicators',
                        '106')
                elif 'errorCode' not in response:
                    raise SDKException(
                        'ThreatIndicators',
                        '102',
                        f'Something went wrong during clear anomaly - {response.json()}')
                self.refresh()
                return
        self._response_not_success(response)

    @property
    def anomaly_records(self) -> list:
        """Get the list of anomaly records for this client.

        Returns:
            list: A list containing anomaly records associated with this client.

        Example:
            >>> ta_server = TAServer()
            >>> records = ta_server.anomaly_records  # Access anomaly records using the property
            >>> print(f"Number of anomaly records: {len(records)}")
            >>> # Iterate through the records
            >>> for record in records:
            >>>     print(record)

        #ai-gen-doc
        """
        return self._anomaly_records

    @property
    def threat_anomaly_stats(self) -> dict:
        """Get the threat anomaly statistics for this client.

        Returns:
            dict: A dictionary containing threat anomaly statistics specific to this client.

        Example:
            >>> ta_server = TAServer()
            >>> stats = ta_server.threat_anomaly_stats
            >>> print(stats)
            >>> # Output will be a dictionary with threat anomaly statistics for the client

        #ai-gen-doc
        """
        return self._threat_anomaly_stats

    @property
    def anomaly_stats(self) -> dict:
        """Get the file type or data anomaly statistics for this client.

        Returns:
            dict: A dictionary containing file or data anomaly statistics for the client.

        Example:
            >>> ta_server = TAServer()
            >>> stats = ta_server.anomaly_stats
            >>> print(f"Anomaly stats: {stats}")

        #ai-gen-doc
        """
        return self._anomaly_stats

    @property
    def datasource_id(self) -> int:
        """Get the threat datasource ID associated with this server.

        Returns:
            The datasource ID as an integer.

        Example:
            >>> server = TAServer()
            >>> ds_id = server.datasource_id  # Use dot notation for property access
            >>> print(f"Datasource ID: {ds_id}")

        #ai-gen-doc
        """
        return int(self._threat_dsid)

    @property
    def anomaly_file_count(self) -> int:
        """Get the total number of anomaly files detected for this server.

        Returns:
            The total count of anomaly files as an integer.

        Example:
            >>> server = TAServer()
            >>> count = server.anomaly_file_count  # Use dot notation for property
            >>> print(f"Anomaly file count: {count}")

        #ai-gen-doc
        """
        _total_files = 0
        _total_files = _total_files + sum(self._anomaly_stats.values())
        _total_files = _total_files + sum(self._threat_anomaly_stats.values())
        return _total_files
