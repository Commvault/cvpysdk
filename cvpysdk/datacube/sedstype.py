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

"""File to store the SEDS Type along with their value.

A Python Dictionary `SEDS_TYPE_DICT` is defined in this file, to store the SEDS Type.

All SEDS Types must be added to this dictionary.

A copy of this dicionary can be imported in all Datacube classes.

"""

from __future__ import absolute_import
from __future__ import unicode_literals

SEDS_TYPE_DICT = {
    0: 'NONE',
    1: 'jdbc',
    2: 'web',
    3: 'exe',
    4: 'csv',
    5: 'file',
    6: 'nas',
    7: 'eloqua',
    8: 'salesforce',
    9: 'ldap',
    10: 'federated',
    11: 'blank',
    12: 'http',
    13: 'camel',
    14: 'facebook',
    15: 'fla',
    16: 'edge',
    17: 'exchange',
    18: 'reviewset',
    19: 'twitter',
    20: 'complianceaudit',
    21: 'fsindex',
    22: 'nfs',
    23: 'cloudoracle',
    24: 'systemdefault',
    25: 'downloadcenteraudit',
    26: 'vm',
    27: 'onedrive',
    28: 'sharepoint',
    29: 'email',
    30: 'dbanalysis',
    31: 'cloudpaas',
    32: 'googledrive',
    33: 'gmail',
    34: 'activedirectory',
    35: 'onedriveindex',
    36: 'multinodefederated',
    37: 'dynamic365',
    38: 'idxlogs',
    39: 'teams',
    40: 'cloudstorage',
    41: 'gmailV2',
    42: 'googledriveV2',
    43: 'asset'
}
