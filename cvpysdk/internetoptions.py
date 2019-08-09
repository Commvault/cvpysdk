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

"""File for setting internet options
InternetOptions: class for setting Internet options in CommServe

 __init__(Commcell_object)      --  initialise with object of CommCell

__repr__()                      --  returns the string to represent the instance of the
                                            InternetOptions class
set_internet_gateway_client(clientname)
                                --  sets Internet gateway with provided client

set_metrics_internet_gateway()  -- sets metrics server as internet gateway

set_no_gateway()                -- Removes internet gateway

set_http_proxy(servername, port)-- sets HTTP proxy enabled with the provided server name and port

disable_http_proxy()            -- Removes HTTP proxy

set_http_authentication(username, pwd)
                                -- sets authentication to HTTP proxy

disable_http_authentication()   --Removes HTTP authentication

refresh()                       --  refresh the internet options

"""
from __future__ import absolute_import
from __future__ import unicode_literals

from base64 import b64encode

from .exception import SDKException


class InternetOptions(object):
    """Class for setting Internet options in CommServe"""

    def __init__(self, commcell_object):
        self._commcell_object = commcell_object
        self._INTERNET = self._commcell_object._services['INTERNET_PROXY']
        self.refresh()

    def __repr__(self):
        """Representation string for the instance of the UserGroups class."""
        return "InternetOption class instance for Commcell: '{0}' with config '{1}'".format(
            self._commcell_object.commserv_name,
            self._internet_config
        )

    def _get_internet_config(self):
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._INTERNET
        )
        if flag:
            self._internet_config = response.json()
            if self._internet_config and 'config' in self._internet_config:
                self._config = self._internet_config['config']
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def _save_config(self):
        """
        updates the configuration of private Metrics
        this must be called to save the configuration changes made in this object
        Raises:
            SDKException:
                if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._INTERNET, self._internet_config
        )
        if not flag:
            raise SDKException('Response', '101', response.text)

    def set_internet_gateway_client(self,
                                    client_name=None,
                                    cloud_metrics=True,
                                    private_metrics=True
                                    ):
        """
        set internet gateway with the client name provided.
        Args:
            client_name     (str): client to be used as internet gateway
            cloud_metrics  (bool): True to enable gateway for cloud metrics
            private_metrics(bool): True to enable gateway for Private metrics
        Raises:
            SDKException:
                if client doesnt exist in CommServe
        """
        if client_name is None:
            raise SDKException('InternetOptions', '101', 'Client name is required')
        clientid = int(self._commcell_object.clients.get(client_name).client_id)
        self._config['proxyType'] = 2
        self._config['proxyClient']['clientId'] = clientid
        self._config['proxyClient']['clientName'] = client_name
        if cloud_metrics:
            self._config['useInternetGatewayPublic'] = True
        else:
            self._config['useInternetGatewayPublic'] = False
        if private_metrics:
            self._config['useInternetGatewayPrivate'] = True
        else:
            self._config['useInternetGatewayPrivate'] = False
        self._save_config()

    def set_metrics_internet_gateway(self):
        """sets metrics server as internet gateway"""
        self._config['proxyType'] = 3
        self._save_config()

    def set_no_gateway(self):
        """Removes internet gateway"""
        self._config['proxyType'] = 1
        self._save_config()

    def set_http_proxy(self, servername=None, port=None):
        """
        sets HTTP proxy enabled with the provided server name and port
        Args:
            servername (str): hostname or IP of the HTTP proxy server
            port (int): HTTP proxy server port
        Raises:
            SDKException:
                if proxy server name and port are empty
        """
        if servername is None or port is None:
            raise SDKException('Response', '101', 'proxy server name and port cannot be empty')
        self._config['useHttpProxy'] = True
        self._config['proxyServer'] = servername
        self._config['proxyPort'] = int(port)
        self._save_config()

    def disable_http_proxy(self):
        """Removes HTTP proxy"""
        self._config['useHttpProxy'] = False
        self._save_config()

    def set_http_authentication(self, username='', pwd=''):
        """
        sets authentication to HTTP proxy
        Args:
            username: username for proxy server
            pwd: password for proxy server
        """
        self._config['useProxyAuthentication'] = True
        self._config['proxyCredentials']['userName'] = username
        self._config['proxyCredentials']['password'] = b64encode(pwd.encode()).decode()
        self._config['proxyCredentials']['confirmPassword'] = b64encode(pwd.encode()).decode()
        self._save_config()

    def disable_http_authentication(self):
        """Removes HTTP authentication"""
        self._config['useProxyAuthentication'] = False
        self._save_config()

    def refresh(self):
        """Refresh the Internet Options."""
        self._get_internet_config()
