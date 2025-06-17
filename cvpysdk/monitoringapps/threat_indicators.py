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
    """Enum class for Anomaly type"""
    FILE_ACTIVITY = 16
    FILE_TYPE = 32
    THREAT_ANALYSIS = 64
    FILE_DATA = 128
    EXTENSION_BASED = 512
    DATA_WRITTEN = 4096


class TAServers():
    """class to represent all servers in threat indicators"""

    def __init__(self, commcell_object):
        """Initializes an instance of the TAServers class.

            Args:

                commcell_object     (object)    --  instance of the commcell class

            Returns:

                object  -   instance of the Servers class

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

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_clients_count(self):
        """returns the client count details for Threat inidcators on this CS

            Args:

                None

            Returns:

                dict  - Containing total client stats [stats for client type = fileserver,vm,laptop]

            Raises:

                SDKException:

                    if failed to fetch details
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._API_CLIENTS_COUNT)
        if flag:
            if response.json():
                return response.json()
            elif bool(response.json()):
                raise SDKException('ThreatIndicators', '110')
        self._response_not_success(response)

    def _get_monitored_vm_count(self):
        """returns the monitored vm count stats for Threat inidcators on this CS

            Args:

                None

            Returns:

                dict  - Containing total monitored vm stats

            Raises:

                SDKException:

                    if failed to fetch details
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._API_MONITORED_VMS)
        if flag:
            if response.json():
                return response.json()
            elif bool(response.json()):
                raise SDKException('ThreatIndicators', '111')
        self._response_not_success(response)


    def _get_threat_indicators(self):
        """returns the list of threat indicators for this CS

            Args:

                None

            Returns:

                list(dict)      - server threat details

                        Eg:-

                                {
                                  "anomalyType": 8,
                                  "modCount": 13705,
                                  "renameCount": 1,
                                  "isVMeSupported": true,
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

    def has(self, name):
        """Checks whether given server name exists in threat indicators or not

            Args:

                name        (str)       --  Name of the server

            Returns:

                bool    --  True if server name exists in threat indicators

        """
        if name.lower() in self._servers:
            return True
        return False

    def run_scan(
            self,
            server_name,
            anomaly_types,
            index_server_name=None,
            storage_pool=None,
            from_time=None,
            to_time=None):
        """runs anomaly scan on given server name

            Args:

                server_name     (str)           --  Server name to analyze

                anomaly_types    (list)         --  list of anomaly to analyze on client

                index_server_name   (str)       --  Index server name to be used for scan

                storage_pool        (str)       --  Storage pool name to be used for scan

                from_time           (int)       --  epoch timestamp from when scan will analyze in backup

                to_time             (int)       --  epoch timestamp to which scan will analyze in backup

            Returns:

                int --  job id of scan job launched

            Raises:

                SDKException:

                    if failed to start job

                    if input data type is not valid

        """
        if not isinstance(server_name, str):
            raise SDKException('ThreatIndicators', '101')
        if not isinstance(anomaly_types, list):
            raise SDKException('ThreatIndicators', '101')
        if not self._commcell_object.clients.has_client(server_name):
            raise SDKException('ThreatIndicators', '102', 'Given server is not found in CS')
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

        if int(self._commcell_object.commserv_oem_id) == 119:
            if not storage_pool:
                raise SDKException('ThreatIndicators', '107')
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

    def get(self, server_name):
        """returns Server class object for given server name

                Args:

                    server_name        (str)       --  client name

                Returns:

                    obj --  Instance of Server class

                Raises:

                    SDKException:

                            if failed to find given server

                            if input is not valid

        """
        if not isinstance(server_name, str):
            raise SDKException('ThreatIndicators', '101')
        if not self.has(server_name):
            raise SDKException('ThreatIndicators', '105')
        return TAServer(commcell_object=self._commcell_object, server_name=server_name)

    def refresh(self):
        """Refresh the threat indicator servers associated with CS"""
        self._servers = []
        self._total_clients = None
        self._monitored_vms = None
        self._threat_indicators = self._get_threat_indicators()
        self._total_clients = self._get_clients_count()
        self._monitored_vms = self._get_monitored_vm_count()

    @property
    def monitored_vms(self):
        """returns the monitored vms stats from threat indicators on this CS

            Returns:

                dict --  client stats

        """
        return self._monitored_vms

    @property
    def clients_count(self):
        """returns the client stats from threat indicators on this CS

            Returns:

                dict --  client stats

        """
        return self._total_clients



class TAServer:

    def __init__(self, commcell_object, server_name):
        """Initializes an instance of the TAServer class.

            Args:

                commcell_object     (object)    --  instance of the commcell class

                server_name         (str)       --  Name of the server


            Returns:

                object  -   instance of the Server class

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

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_anomalies_stats(self):
        """returns the anomalies stats for this client"""
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

    def _get_anamoly_records(self):
        """returns file type anomaly records for this client"""
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

    def refresh(self):
        """Refresh the anomalies details associated with this server"""
        self._threat_dsid = 0
        self._anomaly_records = self._get_anamoly_records()
        self._anomaly_stats, self._threat_anomaly_stats = self._get_anomalies_stats()

    def clear_anomaly(self, anomaly_types):
        """clears the anomalies for this server

            Args:

                anomaly_types       (list)      --  list of anomalies to clear (Refer to AnomalyType class)

            Returns:

                None

            Raises:

                SDKException:

                    if failed to clear anomaly

                    if input is not valid

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
    def anomaly_records(self):
        """returns the anomaly records list

            Returns:

                list --  anomaly records for this client

        """
        return self._anomaly_records

    @property
    def threat_anomaly_stats(self):
        """returns the threat anomaly stats

            Returns:

                dict --  threat anomaly stats for this client

        """
        return self._threat_anomaly_stats

    @property
    def anomaly_stats(self):
        """returns the file type/data anomaly stats

            Returns:

                dict --  file/data anomaly stats for this client

        """
        return self._anomaly_stats

    @property
    def datasource_id(self):
        """returns the threat datasource_id associated with this server

            Returns:

                int --  datasource id

        """
        return int(self._threat_dsid)

    @property
    def anomaly_file_count(self):
        """returns the total anomalies file count for this server

            Returns:

                int --  anomaly file count

        """
        _total_files = 0
        _total_files = _total_files + sum(self._anomaly_stats.values())
        _total_files = _total_files + sum(self._threat_anomaly_stats.values())
        return _total_files
