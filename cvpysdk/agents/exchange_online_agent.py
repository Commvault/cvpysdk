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

"""Module for doing operations on an Exchange Online Agent.

This module has operations that are applicable at the Agent level for Exchange Online (Exchange Mailbox).

ExchangeOnlineAgent:
    __init__()                          --  initialize object of Agent with the specified agent name
                                            and id, and associated to the specified client

    set_graph_support_for_exchange()    --  enable or disable Graph support for the Exchange client

"""

from __future__ import unicode_literals

from typing import Any, Optional

from ..agent import Agent
from ..exception import SDKException


class ExchangeOnlineAgent(Agent):
    """Specialized agent class for managing Exchange Online (Exchange Mailbox) operations.

    This class extends the Agent base class to provide functionality specific
    to Exchange Online agent management, including Graph support configuration.
    """

    def __init__(self, client_object: Any, agent_name: str, agent_id: Optional[str] = None) -> None:
        """Initialize an ExchangeOnlineAgent instance for a specific client and agent.

        Args:
            client_object: Instance of the Client class representing the target client.
            agent_name: Name of the agent (e.g., "Exchange Mailbox").
            agent_id: Optional string specifying the agent's unique identifier.

        Example:
            >>> client = Client(...)
            >>> agent = ExchangeOnlineAgent(client, "Exchange Mailbox", agent_id="137")
        """
        super(ExchangeOnlineAgent, self).__init__(client_object, agent_name, agent_id)

    def set_graph_support_for_exchange(self, use_graph: bool) -> None:
        """Enable or disable Graph support for an Exchange client.

        This method updates the Exchange agent's one-pass properties to toggle Graph usage
        by calling the Agent update API.

        Args:
            use_graph: Set to True to enable Graph support, False to disable it.

        Raises:
            SDKException: If the response is empty or if the API request fails.

        Example:
            >>> agent = ExchangeOnlineAgent(...)
            >>> agent.set_graph_support_for_exchange(True)
            >>> agent.set_graph_support_for_exchange(False)
        """
        request_json = {
            "association": {
                "entity": [{
                    "clientId": int(self._client_object.client_id),
                    "applicationId": int(self.agent_id)
                }]
            },
            "agentProperties": {
                "onePassProperties": {
                    "onePassProp": {
                        "useGraph": bool(use_graph)
                    }
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._AGENT, request_json)

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0].get('errorCode', 0)

                if error_code == 0:
                    self.refresh()
                    return

                error_string = response.json()['response'][0].get('errorString', 'Unknown error')
                raise SDKException(
                    'Agent', '102', 'Failed to update Graph support for Exchange\nError: "{0}"'.format(error_string)
                )

            raise SDKException('Response', '102')

        raise SDKException('Response', '101', self._update_response_(response.text))
