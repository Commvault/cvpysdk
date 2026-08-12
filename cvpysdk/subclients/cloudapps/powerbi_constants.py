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

"""Helper file to maintain all the constants for PowerBi subclient.

PowerBiConstants  -   Maintains constants for PowerBi subclient.

"""


class PowerBiConstants:
    """
    Container class for PowerBi subclient-related constants.

    This class is designed to centralize and manage all constant values
    used throughout the PowerBi subclient implementation. By storing constants
    in a dedicated class, it promotes maintainability, consistency, and
    ease of access across the codebase.

    Key Features:
        - Centralized storage for PowerBi subclient constants
        - Improves code readability and maintainability
        - Prevents duplication of constant values

    #ai-gen-doc
    """

    ADD_SUBCLIENT_ENTITY_JSON = {
        "instanceId": None,
        "subclientId": None,
        "clientId": None,
        "applicationId": None
    }