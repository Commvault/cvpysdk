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
from cvpysdk.exception import SDKException
from cvpysdk.instances.vsinstance import VirtualServerInstance


class NullSubclient(VirtualServerInstance):

    def __init__(self, agent_object, instance_name, instance_id=None):
        raise SDKException('Instance', '102',
                           'Instance: "{0}" is not yet supported'.
                           format(instance_name))

