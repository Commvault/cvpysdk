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

"""Helper file to manage security associations on this commcell

SecurityAssociation is the only class defined in this file

SecurityAssociation:
    __init__()                  --  initializes security class object

    __str__()                   --  returns all the users associated with the commcell

    __repr__()                  --  returns the string for the instance of the User class

    _security_association_json()--  generates security association blob with all
                                    user-entity-role association

    fetch_security_association()--  fetches security associations from entity

    _get_security_roles()       --  gets the list of all the security roles applicable
                                        on this commcell

    _add_security_association() --  adds the security association with client or clientgroup

    has_role()                  --  checks if specified role exists on commcell


"""

from ..exception import SDKException


class SecurityAssociation(object):
    """Class for managing the security associations roles on the commcell"""

    def __init__(self, commcell_object, class_object):
        """Initializes the security associations object

            Args:
                commcell_object     (object)     --     instance of the Commcell class

                class_object         (object)     --    instance of the class on which we want to
                                                            manage security operations
                                                        default: commcell object will be used
        """
        self._commcell_object = commcell_object
        if not class_object:
            class_object = self._commcell_object

        from ..commcell import Commcell
        if isinstance(class_object, Commcell):
            self._entity_list = {
                "entity": [{
                    "commCellId": class_object.commcell_id,
                    "_type_": 1
                }]
            }

        from ..client import Client
        if isinstance(class_object, Client):
            self._entity_list = {
                "entity": [{
                    "clientId": int(class_object.client_id),
                    "_type_": 3
                }]
            }

        from ..storage_pool import StoragePool
        if isinstance(class_object, StoragePool):
            self._entity_list = {
                "entity": [{
                    "storagePolicyId": int(class_object.storage_pool_id),
                    "_type_": 17
                }]
            }
            
        from ..plan import Plan
        if isinstance(class_object, Plan):
            self._entity_list = {
                "entity": [{
                    "planId": int(class_object.plan_id),
                    "_type_": 158
                }]
            }

        from ..workflow import WorkFlow
        if isinstance(class_object, WorkFlow):
            self._entity_list = {
                "entity": [{
                    "workflowId": int(class_object.workflow_id),
                    "_type_": 83,
                    "entityType": 83
                }]
            }

        self._roles = self._get_security_roles()

    def __str__(self):
        """Representation string consisting of all available security roles on this commcell.

            Returns:
                str - string of all the available security roles on this commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Roles')

        for index, role in enumerate(self._roles):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, role)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Security class."""
        return "Security class instance for Commcell"

    @staticmethod
    def _security_association_json(entity_dictionary):
        """handles three way associations (role-user-entities)

            Args:
                entity_dictionary   --      combination of entity_type, entity names
                                            and role
                e.g.: entity_dict={
                                'assoc1':
                                    {
                                        'entity_type':['entity_name'],
                                        'entity_type':['entity_name', 'entity_name'],
                                        'role': ['role1']
                                    },
                                'assoc2':
                                    {
                                        'mediaAgentName': ['networktestcs', 'standbycs'],
                                        'clientName': ['Linux1'],
                                        'role': ['New1']
                                        }
                                    }
                entity_type         --      key for the entity present in dictionary
                                            on which user will have access

                entity_name         --      Value of the key

                role                --      role will remain role in dictionary
                e.g.: {"clientName":"Linux1"}
                entity_type:    clientName, mediaAgentName, libraryName, userName,
                                userGroupName, storagePolicyName, clientGroupName,
                                schedulePolicyName, locationName, providerDomainName,
                                alertName, workflowName, policyName, roleName

                entity_name:    client name for entity_type 'clientName'
                                Media agent name for entitytype 'mediaAgentName'
                                similar for other entity_typees

                request_type        --      decides whether to ADD, DELETE or
                                            OVERWRITE user security association.

        """
        complete_association = []
        for entity_value in entity_dictionary.values():
            for each_entity_key in entity_value:
                for element in entity_value[each_entity_key]:
                    if each_entity_key != "role":
                        if each_entity_key == "_type_":
                            association_blob = {
                                "entities": {
                                    "entity": [{
                                        each_entity_key: element,
                                        "flags": {
                                            "includeAll": True
                                        }
                                    }]
                                },
                                "properties": {
                                    "role": {
                                        "roleName": entity_value['role'][0]
                                    }
                                }
                            }
                        else:
                            association_blob = {
                                "entities": {
                                    "entity": [{
                                        each_entity_key: element
                                    }]
                                },
                                "properties": {
                                    "role": {
                                        "roleName": entity_value['role'][0]
                                    }
                                }
                            }
                        complete_association.append(association_blob)
        return complete_association

    @staticmethod
    def fetch_security_association(security_dict):
        """Fetches security associations from entity
        Args:
            security_dict    (dict)   --  security association properties of entity

        Returns:
            formatted security association dictionary with custom permissions marked as invalid
        """
        security_list = []
        count = 0
        associations = {}
        entity_permissions = {}
        for every_association in security_dict:
            if 'entity' in every_association['entities']:
                entities = every_association['entities']['entity']
                for entity in entities:
                    for each_key in entity:
                        if 'Name' in each_key:
                            if 'externalGroupName' in each_key:
                                associations = entity[each_key]
                            #if 'providerDomainName' in each_key:
                                # No need to explicitely  check for provider key
                                if associations:
                                    ext_group = "{0}\\{1}".format(entity['providerDomainName'],
                                                                  associations)
                                    associations = {}
                                else:
                                    ext_group = entity[each_key]
                                security_list.append(each_key)
                                security_list.append(ext_group.lower())
                                break
                            elif 'displayName' in each_key:
                                security_list.append('clientName')
                                security_list.append(entity['clientName'].lower())
                                break
                            else:
                                security_list.append(each_key)
                                security_list.append(entity[each_key].lower())
                                break
                        elif 'flags' in each_key:
                            security_list.append(entity['_type_'])
                            security_list.append(entity['flags'])

                    if 'role' in every_association['properties']:
                        role_list = every_association['properties']['role']
                        for entity in role_list:
                            if 'Name' in entity:
                                security_list.append(role_list[entity].lower())
                    if 'categoryPermission' in every_association['properties']:
                        categories = every_association['properties'][
                            'categoryPermission']['categoriesPermissionList']
                        for key in categories:
                            categories = key
                            for permission in categories:
                                if 'Name' in permission:
                                    security_list.append(categories[permission] + str('-invalid'))
                                    #Not supporting custom permissions as of now.
                    entity_permissions.setdefault(count, security_list)
                    security_list = []
                    count += 1
        return entity_permissions


    def _get_security_roles(self):
        """Returns the list of available roles on this commcell"""
        GET_SECURITY_ROLES = self._commcell_object._services['GET_SECURITY_ROLES']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', GET_SECURITY_ROLES
        )

        if flag:
            if response.json() and 'roleProperties' in response.json():
                role_props = response.json()['roleProperties']

                roles = {}

                for role in role_props:
                    if 'role' in role:
                        role_name = role['role']['roleName'].lower()
                        role_id = role['role']['roleId']
                        roles[role_name] = role_id

                return roles
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _add_security_association(self, association_list, user= True, request_type = None, externalGroup = False):
        """
        Adds the security association on the specified class object

        Supported Types : Client, Storage Pool class objects.

        Args:
            associations_list   (list)  --  list of users to be associated
                Example:
                    associations_list = [
                        {
                            'user_name': user1,
                            'role_name': role1
                        },
                        {
                            'user_name': user2,
                            'role_name': role2
                        }
                    ]
 
            user (bool)             --    True or False. set user = False, If associations_list made up of user groups
            request_type (str)      --    eg : 'OVERWRITE' or 'UPDATE' or 'DELETE', Default will be OVERWRITE operation
            externalGroup (bool)    --    True or False, set externalGroup = True. If Security associations is to be done on External User Groups

        Raises:
            SDKException:
                if association is not of dict type
                if role doesnot exists on Commcell
                if request fails
        """

        update_operator_request_type = {
            "OVERWRITE": 1,
            "UPDATE": 2,
            "DELETE": 3
        }

        if request_type:
            request_type = request_type.upper()

        security_association_list = []
        for association in association_list:
            if not isinstance(association, dict):
                raise SDKException('Security', '101')

            if not self.has_role(association['role_name']):
                raise SDKException(
                    'Security', '102', 'Role {0} doesn\'t exist'.format(association['role_name'])
                )

            user_or_group = {}
            if user:
                user_or_group = {'userName': association['user_name']}
            elif externalGroup:
                user_or_group = {'externalGroupName': association['user_name']}
            else:
                user_or_group = {'userGroupName': association['user_name']}  

            temp = {
                "userOrGroup": [
                    user_or_group
                ],
                "properties": {
                    "role": {
                        "_type_": 120,
                        "roleId": self._roles[association['role_name'].lower()],
                        'roleName': association['role_name']
                    }
                }
            }
            security_association_list.append(temp)

        request_json = {
            "entityAssociated": self._entity_list,
            "securityAssociations": {
                "associationsOperationType": update_operator_request_type.get(request_type, 1),
                "associations": security_association_list,
                "ownerAssociations": {
                    "ownersOperationType": 1
                }
            }
        }

        ADD_SECURITY_ASSOCIATION = self._commcell_object._services['SECURITY_ASSOCIATION']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', ADD_SECURITY_ASSOCIATION, request_json
        )

        if flag:
            if response.json() and 'response' in response.json():
                response_json = response.json()['response'][0]

                error_code = response_json['errorCode']

                if error_code != 0:
                    error_message = response_json['errorString']
                    raise SDKException(
                        'Security',
                        '102',
                        'Failed to add associations. \nError: {0}'.format(error_message)
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def has_role(self, role_name):
        """Checks if role with specified name exists

            Args:
                role_name     (str)     --     name of the role to be verified

            Returns:
                (bool)     -  True if role with specified name exists
        """
        if not isinstance(role_name, str):
            raise SDKException('Security', '101')

        return self._roles and role_name.lower() in self._roles

