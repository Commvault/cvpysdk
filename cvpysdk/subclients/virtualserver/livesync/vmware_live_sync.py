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

"""File for configuring and monitoring live sync on the VMW subclient.

VMWareLiveSync is the only class defined in this file.

VMWareLiveSync: Class for configuring and monitoring VMWare subclient live sync

"""

from .vsa_live_sync import VsaLiveSync


class VMWareLiveSync(VsaLiveSync):
    """Class for configuring and monitoring VMWare live sync operations"""
    pass
