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

"""File for configuring and monitoring live sync on the Google Cloud subclient.

GCPLiveSync is the only class defined in this file.
GCPLiveSync: Class for configuring and monitoring Google Cloud subclient live sync

GCPLiveSync:

    configure_live_sync()               -- To configure live sync for Google Cloud
                                            Platform instances

"""

from .vsa_live_sync import VsaLiveSync
from ....exception import SDKException


class GCPLiveSync(VsaLiveSync):
    """Class for configuring and monitoring Google Cloud Platform live sync operations"""
    # TODO: Implement methods for Google Cloud Live Sync in next Form
    pass