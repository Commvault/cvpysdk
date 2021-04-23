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

"""Helper file to maintain all the constants for Activate Apps

ActivateEntityConstants         -       Maintains constants for Regex custom entity

TagConstants                    -       Maintains constants for Tags

"""
import copy


class ActivateEntityConstants:
    """Class to maintain all the Activate entity related constants"""

    REQUEST_JSON = {
        "regularExpression": "",
        "flags": 0,
        "enabled": True,
        "entityName": "",
        "entityXML": {
            "keywords": "",
            "isSystemDefinedEntity": False
        }
    }


class TagConstants:
    """class to maintain all the Tags related constants"""

    TAG_SET_ADD_REQUEST_JSON = {
        "entityType": 9504,
        "operationType": 1,
        "fromSite": 4,
        "container": {
            "containerType": 9504,
            "containerName": "",
            "comment": ""
        }
    }

    TAG_SET_MODIFY_REQUEST_JSON = copy.deepcopy(TAG_SET_ADD_REQUEST_JSON)
    TAG_SET_MODIFY_REQUEST_JSON['operationType'] = 3

    TAG_SET_DELETE_REQUEST_JSON = {
        "entityType": 9504,
        "containers": [
            {
                "containerType": 9504,
                "containerId": 0
            }
        ]
    }

    TAG_ADD_REQUEST_JSON = {
        "container": {
            "containerId": 0
        },
        "tags": [
            {
                "name": ""
            }
        ]
    }

    TAG_MODIFY_REQUEST_JSON = copy.deepcopy(TAG_ADD_REQUEST_JSON)
    TAG_MODIFY_REQUEST_JSON['tags'][0]['tagId'] = 0

    VIEW_PERMISSION = {
        "permissionId": 31,
        "_type_": 122,
        "permissionName": "View"
    }
    ADD_PERMISSION = {
        "permissionId": 34,
        "_type_": 122,
        "permissionName": "Add/Append"
    }

    TAG_SET_SHARE_REQUEST_JSON = {
        "entityAssociated": {
            "entity": [
                {
                    "tagId": 0,
                    "_type_": 9504
                }
            ]
        },
        "securityAssociations": {
            "associationsOperationType": 1,
            "associations": [
                {
                    "userOrGroup": [
                        {

                        }
                    ],
                    "properties": {
                        "permissions": [
                            VIEW_PERMISSION
                        ]
                    }
                }

            ]
        }
    }
