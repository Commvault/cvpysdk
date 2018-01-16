# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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
    25: 'downloadcenteraudit'
}
