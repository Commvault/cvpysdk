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

"""Main file for performing alert operations.

Alerts and Alert are 2 classes defined in this file.

Alerts: Class for representing all the Alerts

Alert: Class for a single alert selected


Alerts:
    __init__(commcell_object)   --  initialise object of Alerts class associated with
    the specified commcell

    __str__()                   --  returns all the alerts associated with the commcell

    __repr__()                  --  returns the string for the instance of the Alerts class

    __len__()                   --  returns the number of alerts configured on the Commcell

    __getitem__()               --  returns the name of the alert for the given alert Id or the
    details for the given alert name

    _get_alerts()               --  gets all the alerts associated with the commcell specified

    _get_entities()             --  returns the list of associations for an alert

    _get_alert_json()           --  returns the dict/json required to create an alert

    get_alert_sender()          -- returns the mail sender name as set in the Email server

    create_alert(alert_name)    --  returns the instance of Alert class for created alert

    has_alert(alert_name)       --  checks whether the alert exists or not

    get(alert_name)             --  returns the alert class object of the input alert name

    delete(alert_name)          --  removes the alerts from the commcell of the specified alert

    console_alerts()            --  returns the list of all console alerts

    console_alert()             -- returns console alert details for a console alert with given livefeedid

    refresh()                   --   refresh the alerts associated with the commcell

Alerts Attributes
------------------
    **all_alerts**              --  returns the dict of all the alerts associated
    with the commcell and their information such as name, id and category


Alert:
    __init__(commcell_object,
             alert_name,
             alert_id=None)       --  initialise object of alert with the specified commcell name
    and id, and associated to the specified commcell

    __repr__()                    --  return the alert name with description and category,
    the alert is associated with

    _get_alert_id()               --  method to get the alert id, if not specified in __init__

    _get_alert_properties()       --  get the properties of this alert

    _get_alert_category()         --  return the category of the alert

    _modify_alert_properties      --  modifies the alert properties

    alert_name(name)              --  sets the alert name

    alert_severity(severity)      --  sets the alert severity

    notification_types(list)      --  sets the notifications types

    entities(entities_dict)       --  sets the entities/associations

    enable()                      --  enables the alert

    disable()                     --  disables the alert

    enable_notification_type()    --  enables notification type of alert

    disable_notification_type()   --  disables notification type of alert

    refresh()                     --  refresh the properties of the Alert

Alert Attributes
------------------
    **alert_id**                --  returns the id of an alert

    **alert_name**              --  gets the name of an alert

    **alert_type**              --  returns the type of an alert

    **alert_category**          --  returns the category of an alert

    **alert_severity**          --  returns the severity of an alert

    **alert_criteria**          --  returns the criteria of an alert

    **notification_types**      --  returns the notification types of an alert

    **description**             --  returns the description of an alert

    **users_list**              --  returns the list of users associated with the alert

    **user_group_list**         --  returns the list of user groups associated with the alert

    **entities**                --  returns the list of entities associated with an alert

    **email_recipients**        --  returns the list of email recipients associated to the alert
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import xml.etree.ElementTree as ET
from .exception import SDKException


class Alerts(object):
    """Class for getting all the Alerts associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the Alerts class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the Alerts class
        """
        self._commcell_object = commcell_object
        self._ALERTS = commcell_object._services['GET_ALL_ALERTS']
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._alerts = None

        self._notification_types = {
            'email': 1,
            'snmp': 4,
            'event viewer': 8,
            'save to disk': 512,
            'rss feeds': 1024,
            'console alerts': 8192,
            'scom': 32768,
            'workflow': 65536,
            'content indexing': 131072
        }
        self.refresh()

    def __str__(self):
        """Representation string consisting of all alerts of the Commcell.

            Returns:
                str - string of all the alerts for a commcell
        """
        representation_string = "{:^5}\t{:^50}\t{:^80}\t{:^30}\n\n".format(
            'S. No.', 'Alert', 'Description', 'Category'
        )

        for index, alert_name in enumerate(self._alerts):
            alert_description = self._alerts[alert_name]['description']
            alert_category = self._alerts[alert_name]['category']
            sub_str = '{:^5}\t{:50}\t{:80}\t{:30}\n'.format(
                index + 1,
                alert_name,
                alert_description,
                alert_category
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Alerts class."""
        return "Alerts class instance for Commcell"

    def __len__(self):
        """Returns the number of the alerts configured on the Commcell."""
        return len(self.all_alerts)

    def __getitem__(self, value):
        """Returns the name of the alert for the given alert ID or
            the details of the alert for given alert Name.

            Args:
                value   (str / int)     --  Name or ID of the alert

            Returns:
                str     -   name of the alert, if the alert id was given

                dict    -   dict of details of the alert, if alert name was given

            Raises:
                IndexError:
                    no alert exists with the given Name / Id

        """
        value = str(value)

        if value in self.all_alerts:
            return self.all_alerts[value]
        else:
            try:
                return list(filter(lambda x: x[1]['id'] == value, self.all_alerts.items()))[0][0]
            except IndexError:
                raise IndexError('No alert exists with the given Name / Id')

    def _get_alerts(self):
        """Gets all the alerts associated with the commcell

            Returns:
                dict - consists of all alerts of the commcell
                    {
                         "alert1_name": {
                             "id": alert1_id,
                             "category": alert1_category
                         },
                         "alert2_name": {
                             "id": alert2_id,
                             "category": alert2_category
                         }
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._ALERTS)

        if flag:
            if response.json() and 'alertList' in response.json():
                alerts_dict = {}

                for dictionary in response.json()['alertList']:
                    temp_dict = {}

                    temp_name = dictionary['alert']['name'].lower()
                    temp_id = str(dictionary['alert']['id']).lower()
                    temp_description = dictionary['description'].lower()
                    temp_category = dictionary['alertCategory']['name'].lower()

                    temp_dict['id'] = temp_id
                    temp_dict['description'] = temp_description
                    temp_dict['category'] = temp_category

                    alerts_dict[temp_name] = temp_dict

                    del temp_dict

                return alerts_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)


    def _get_entities(self, entities):
        """Returns the list of entities associations for an alert

        Args:
            entities    (dict)  --  dictionary of entities for an alert

        Raise:
            SDKException:
                if entities is not an instance of dictionary

        Returns:
            list  -  a list of associations for an alert

        """
        if not isinstance(entities, dict):
            raise SDKException('Alert', '101')

        # policies not handled as

        entity_dict = {
            "clients": {
                "clientName": "client_name",
                "clientId": "client_id",
                "_type_": 3
            },
            "client_groups": {
                "clientGroupName": "clientgroup_name",
                "clientGroupId": "clientgroup_id",
                "_type_": 28
            },
            "users": {
                "userName": "user_name",
                "userId": "user_id",
                "_type_": 13
            },
            "user_groups": {
                "userGroupName": "user_group_name",
                "userGroupId": "user_group_id",
                "_type_": 15
            },
            "disk_libraries": {
                "libraryName": "library_name",
                "libraryId": "library_id",
                "_type_": 9
            },
            "media_agents": {
                "mediaAgentName": "media_agent_name",
                "mediaAgentId": "media_agent_id",
                "_type_": 11
            },
            "storage_policies": {
                "storagePolicyName": "storage_policy_name",
                "storagePolicyId": "storage_policy_id",
                "_type_": 17
            }
        }

        associations = []

        for entity, values in entities.items():
            if entity == "entity_type_names":
                for value in values:
                    if value == "ALL_CLIENT_GROUPS_ENTITY":
                        entity_type = 27
                    else:
                        entity_type = 2
                    temp_dict = {
                        "entityTypeName": value,
                        "_type_": entity_type
                    }
                    associations.append(temp_dict)
            else:
                entity_obj = getattr(self._commcell_object, entity)

                # this will allows us to loop through even for single item
                values = values.split() if not isinstance(values, list) else values

                for value in values:
                    temp_dict = entity_dict[entity].copy()
                    for name, entity_attr in temp_dict.items():
                        if name != "_type_":
                            try: # to convert the string values to int types
                                temp_dict[name] = int(getattr(entity_obj.get(value), entity_attr))
                            except ValueError:
                                temp_dict[name] = getattr(entity_obj.get(value), entity_attr)
                    associations.append(temp_dict)

        return associations


    def _get_alert_json(self, alert_json):
        """To form the json required to create an alert

        Args:
            alert_json    (dict)  --  a dictionary to create an alert

        Returns:
            dict  -  a constructed dictionary needed to create an alert
        """
        alert_detail = {
            "alertDetail": {
                "alertType": alert_json.get("alert_type"),
                "notifType": [n_type for n_type in alert_json.get("notif_type", [8192])],
                "notifTypeListOperationType": alert_json.get("notifTypeListOperationType", 0),
                "alertSeverity": alert_json.get("alertSeverity", 0),
                "EscnonGalaxyUserList":{
                    "nonGalaxyUserOperationType": alert_json.get("nonGalaxyUserOperationType", 0)
                },
                "locale":{
                    "localeID":alert_json.get("localeID", 0)
                },
                "EscUserList":{
                    "userListOperationType":alert_json.get("userListOperationType", 0)
                },
                "EscUserGroupList":{
                    "userGroupListOperationType": alert_json.get("userGroupListOperationType", 0)
                },
                "alertrule":{
                    "alertName": alert_json.get("alert_name")
                },
                "criteria":{
                    "criteria": alert_json.get("criteria")
                },
                "userList":{
                    "userListOperationType":alert_json.get("userListOperationType", 0),
                    "userList":[{"userName":user} for user in alert_json.get("users", ["admin"])]
                },
                "EntityList":{
                    "associationsOperationType":alert_json.get("associationsOperationType", 0),
                    "associations": self._get_entities(alert_json.get("entities", dict()))
                }
            }
        }

        # Check if paramsList is present or not
        if alert_json.get("paramsList"):
            alert_detail["alertDetail"]["criteria"]["paramsList"] = alert_json.get("paramsList")

        # Check if additonal mail recipents exist
        if alert_json.get("nonGalaxyList"):
            alert_detail["alertDetail"]["nonGalaxyList"] = alert_json.get("nonGalaxyList")

        if alert_json.get("user_groups"):
            alert_detail["alertDetail"]["userGroupList"] = {
                "userGroupListOperationType":alert_json.get("userGroupListOperationType", 0),
                "userGroupList":[
                    {
                        "userGroupName":user_grp
                    } for user_grp in alert_json.get("user_groups")
                ]
            }

        return alert_detail

    def get_alert_sender(self):
        """
            Returns the Alert Sender name
        """
        get_alert = self._services['EMAIL_SERVER']
        flag, response = self._cvpysdk_object.make_request('GET', get_alert)
        if flag:
            if response.json():
                sender = response.json()["senderInfo"]['senderName']
                if not sender:
                    sender = response.json()["senderInfo"]['senderAddress']
                return sender
            else:
                raise SDKException('Alert', '102', "Failed to get sender address")
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)


    def create_alert(self, alert_dict):
        """Creates a new Alert for CommCell

        Args:
            alert_dict    (dict)  --  dictionary required to create an alert

        Returns:
            object  -  instance of the Alert class for this new alert

        Raises:
            SDKException:
                if input argument is not an instance of dict

                if alert with given name already exists

                if failed to create an alert

                if response is not success

                if response is empty
        """
        if not isinstance(alert_dict, dict):
            raise SDKException('Alert', '101')

        # required alert json
        alert_json = self._get_alert_json(alert_dict)
        alert_name = alert_json["alertDetail"]["alertrule"]["alertName"]
        if self.has_alert(alert_name):
            raise SDKException('Alert', '102', 'Alert "{0}" already exists.'.
                               format(alert_name))

        post_alert = self._services['GET_ALL_ALERTS']
        flag, response = self._cvpysdk_object.make_request(
            'POST', post_alert, alert_json)

        if flag:
            if response.json():
                error_dict = response.json()["errorResp"]
                error_code = str(error_dict["errorCode"])

                if error_code == "0":
                    self.refresh()
                    return self.get(alert_name)
                else:
                    error_message = ""

                    if 'errorMessage' in error_dict:
                        error_message = error_dict['errorMessage']

                    if error_message:
                        raise SDKException(
                            'Alert', '102', 'Failed to create Alert\nError: "{}"'.format(
                                error_message
                            )
                        )
                    else:
                        raise SDKException(
                            'Alert', '102', "Failed to create Alert")
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)


    @property
    def all_alerts(self):
        """Returns the dict of all the alerts configured on this commcell

            dict - consists of all alerts of the commcell
                    {
                         "alert1_name": {
                             "id": alert1_id,
                             "category": alert1_category
                         },
                         "alert2_name": {
                             "id": alert2_id,
                             "category": alert2_category
                         }
                    }
        """
        return self._alerts

    def has_alert(self, alert_name):
        """Checks if a alert exists for the commcell with the input alert name.

            Args:
                alert_name (str)  --  name of the alert

            Returns:
                bool - boolean output whether the alert exists for the commcell or not

            Raises:
                SDKException:
                    if type of the alert name argument is not string
        """
        if not isinstance(alert_name, str):
            raise SDKException('Alert', '101')

        return self._alerts and alert_name.lower() in self._alerts

    def get(self, alert_name):
        """Returns a alert object of the specified alert name.

            Args:
                alert_name (str)  --  name of the alert

            Returns:
                object - instance of the Alert class for the given alert name

            Raises:
                SDKException:
                    if type of the alert name argument is not string

                    if no alert exists with the given name
        """
        if not isinstance(alert_name, str):
            raise SDKException('Alert', '101')
        else:
            alert_name = alert_name.lower()

            if self.has_alert(alert_name):
                return Alert(
                    self._commcell_object, alert_name,
                    self._alerts[alert_name]['id'],
                    self._alerts[alert_name]['category']
                )

            raise SDKException('Alert', '102', 'No Alert exists with name: {0}'.format(alert_name))

    def console_alerts(self, page_number=1, page_count=1):
        """Returns the console alerts from page_number to the number of pages asked for page_count

            Args:
                page_number (int)  --  page number to get the alerts from

                page_count  (int)  --  number of pages to get the alerts of

            Raises:
                SDKException:
                    if type of the page number and page count argument is not int

                    if response is empty

                    if response is not success

            Returns:
                str - String representation of console alerts if version is less than SP23
                object - json response object for console alerts if version greater than or equal to SP23
        """
        if not (isinstance(page_number, int) and isinstance(page_count, int)):
            raise SDKException('Alert', '101')

        console_alerts = self._services['GET_ALL_CONSOLE_ALERTS'] % (
            page_number, page_count)

        flag, response = self._cvpysdk_object.make_request('GET', console_alerts)

        if flag:
            if response.json() and 'totalNoOfAlerts' in response.json():
                if self._commcell_object.commserv_version >= 23:
                    return response.json()

                o_str = "Total Console Alerts found: {0}".format(
                    response.json()['totalNoOfAlerts']
                )

                o_str += "\n{:^5}\t{:^50}\t{:^50}\t{:^50}\n\n".format(
                    'S. No.', 'Alert', 'Type', 'Criteria'
                )

                for index, dictionary in enumerate(response.json()['feedsList']):
                    o_str += '{:^5}\t{:50}\t{:^50}\t{:^50}\n'.format(
                        index + 1,
                        dictionary['alertName'],
                        dictionary['alertType'],
                        dictionary['alertcriteria']
                    )

                return o_str
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def console_alert(self, live_feed_id):
        """Returns the console console alert with given live_feed_id

            Args:
                live_feed_id (int)  --  Live feed ID of console alert to fetch

            Raises:
                SDKException:
                    if type of the live_feed_id argument is not int

                    if response is empty

                    if response is not success

            Returns:
                object - Console alert json object for given live_feed_id
        """
        if not (isinstance(live_feed_id, int)):
            raise SDKException('Alert', '101')

        console_alerts = self._services['GET_CONSOLE_ALERT'] % (
            live_feed_id)

        flag, response = self._cvpysdk_object.make_request('GET', console_alerts)

        if flag:
            if response and response.json() and 'description' in response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def delete(self, alert_name):
        """Deletes the alert from the commcell.

            Args:
                alert_name (str)  --  name of the alert

            Raises:
                SDKException:
                    if type of the alert name argument is not string

                    if failed to delete the alert

                    if no alert exists with the given name
        """
        if not isinstance(alert_name, str):
            raise SDKException('Alert', '101')
        alert_name = alert_name.lower()

        if self.has_alert(alert_name):
            alert_id = self._alerts[alert_name]['id']
            alert = self._services['ALERT'] % (alert_id)

            flag, response = self._cvpysdk_object.make_request(
                'DELETE', alert
            )

            if flag:
                if response.json():
                    if 'errorCode' in response.json():
                        if response.json()['errorCode'] == 0:
                            # initialize the alerts again
                            # to refresh with the latest alerts
                            self.refresh()
                        else:
                            raise SDKException('Alert', '102', response.json()['errorMessage'])
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._update_response_(response.text)
                exception_message = 'Failed to delete alert\nError: "{0}"'.format(
                    response_string
                )

                raise SDKException('Alert', '102', exception_message)
        else:
            raise SDKException(
                'Alert', '102', 'No alert exists with name: {0}'.format(alert_name)
            )

    def refresh(self):
        """Refresh the alerts associated with the Commcell."""
        self._alerts = self._get_alerts()


class Alert(object):
    """Class for performing operations for a specific alert."""

    def __init__(self, commcell_object, alert_name, alert_id=None, alert_category=None):
        """Initialise the Alert class instance.

            Args:
                commcell_object (object)  --  instance of the Commcell class

                alert_name      (str)     --  name of the alert

                alert_id        (str)     --  id of the alert
                    default: None

                alert_category  (str)     --  name of the alert category
                    default: None

            Returns:
                object - instance of the ALert class
        """

        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._alerts_obj = Alerts(self._commcell_object)
        self._alert_name = alert_name.lower()
        self._alert_detail = None
        if alert_id:
            self._alert_id = str(alert_id)
        else:
            self._alert_id = self._get_alert_id()

        if alert_category:
            self._alert_category = alert_category
        else:
            self._alert_category = self._get_alert_category()

        self._ALERT = self._services['ALERT'] % (self.alert_id)
        self._all_notification_types = {
            'email': 1,
            'snmp': 4,
            'event viewer': 8,
            'save to disk': 512,
            'rss feeds': 1024,
            'console alerts': 8192,
            'scom': 32768,
            'workflow': 65536,
            'content indexing': 131072
        }

        self._alert_severity = None
        self._alert_type = None
        self._alert_type_id = None
        self._description = None
        self._criteria = []
        self._entities_list = []
        self._users_list = []
        self._user_group_list = []
        self._notification_types = []

        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Alert class instance for Alert: "{0}", Alert Type: "{1}"'
        return representation_string.format(self.alert_name, self._alert_type)

    def _get_alert_id(self):
        """Gets the alert id associated with this alert.

            Returns:
                str - id associated with this alert
        """
        return self._alerts_obj.get(self.alert_name).alert_id

    def _get_alert_category(self):
        """Gets the alert category associated with this alert.

            Returns:
                str - alert category name associated with this alert
        """
        return self._alerts_obj.get(self.alert_name).alert_category

    def _get_alert_properties(self):
        """Gets the alert properties of this alert.

            Returns:
                dict - dictionary consisting of the properties of this alert

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._ALERT)

        if flag:
            if response.json() and 'alertDetail' in response.json().keys():
                self._alert_detail = response.json()['alertDetail']
                if 'alertSeverity' in self._alert_detail:
                    self._alert_severity = self._alert_detail['alertSeverity']

                if 'criteria' in self._alert_detail:
                    criterias = self._alert_detail['criteria']
                    for criteria in criterias:
                        self._criteria.append({
                            'criteria_value': criteria['value'] if 'value' in criteria else None,
                            'criteria_id':
                            str(criteria['criteriaId']) if 'criteriaId' in criteria else None,
                            'esclation_level':
                            criteria['esclationLevel'] if 'esclationLevel' in criteria else None
                        })

                if 'alert' in self._alert_detail:
                    alert = self._alert_detail['alert']

                    if 'description' in alert:
                        self._description = alert['description']

                    if 'alertType' in alert and 'name' in alert['alertType']:
                        self._alert_type = alert['alertType']['name']
                        self._alert_type_id = alert['alertType']['id']

                if 'xmlEntityList' in self._alert_detail:
                    entity_xml = ET.fromstring(self._alert_detail['xmlEntityList'])
                    self._entities_list = []
                    for entity in entity_xml.findall("associations"):
                        if entity.find("flags") is not None:
                            if entity.find("flags").attrib["exclude"] != "1":
                                self._entities_list.append(entity.attrib)
                        else:
                            self._entities_list.append(entity.attrib)

                # to convert the ids to int type
                for entity in self._entities_list:
                    for key, value in entity.items():
                        try:
                            entity[key] = int(value) # to change the ids to type int
                        except ValueError:
                            pass

                if 'regularNotifications' in self._alert_detail:
                    self._notification_types = self._alert_detail["regularNotifications"]

                if 'userList' in self._alert_detail:
                    self._users_list = [user['name'] for user in self._alert_detail['userList']]
                else:
                    self._users_list = []

                if 'userGroupList' in self._alert_detail:
                    self._user_group_list = [grp['name'] for grp in self._alert_detail['userGroupList']]
                else:
                    self._user_group_list = []

                self._email_recipients = []
                if 'nonGalaxyUserList' in self._alert_detail:
                    self._email_recipients = [email['name'] for email in self._alert_detail['nonGalaxyUserList']]

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _modify_alert_properties(self):
        """
        modifies the properties of an alert
        Exception:
            if modification of the alert failed
        """

        request_json = {
            "alertDetail":{
                "alertDetail": {
                    "alertType": self._alert_type_id, # this should not be changed
                    "notifType": self._notification_types,
                    "alertSeverity": self._alert_severity,
                    "alertrule": {
                        "alertName": self._alert_name
                    },
                    "criteria": {
                        "criteria": int(self._criteria[0]['criteria_id'])
                    },
                    "userList": {
                        "userListOperationType": 1,
                        "userList": [{"userName": user} for user in self._users_list]
                    },
                    "userGroupList": {
                        "userGroupListOperationType": 1,
                        "userGroupList": [{"userGroupName": user} for user in self._user_group_list]
                    },
                    "nonGalaxyList": {
                        "nonGalaxyUserList": [{"nonGalaxyUser": email} for email in self._email_recipients]
                    },
                    "EntityList": {
                        "associations": self._entities_list
                    }
                }
            }
        }

        modify_alert = self._services['MODIFY_ALERT'] % (self.alert_id)
        flag, response = self._cvpysdk_object.make_request(
            'POST', modify_alert, request_json
        )

        if flag:
            if response.json():
                error_code = str(response.json()['errorCode'])
                if error_code == '0':
                    self.refresh()
                    return
                else:
                    o_str = 'Failed to update properties of Alert\nError: "{0}"'
                    o_str = o_str.format(response.json()['errorMessage'])
                    raise SDKException('Alert', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)



    @property
    def name(self):
        """Returns the Alert display name """
        return self._alert_detail['alert']['alert']['name']

    @property
    def alert_name(self):
        """Treats the alert name as a read-only attribute."""
        return self._alert_name

    @alert_name.setter
    def alert_name(self, name):
        """Modifies the Alert name"""
        if not isinstance(name, str):
            raise SDKException('Alert', '101')

        self._alert_name = name
        self._modify_alert_properties()

    @property
    def alert_id(self):
        """Treats the alert id as a read-only attribute."""
        return self._alert_id

    @property
    def alert_type(self):
        """Treats the alert type as a read-only attribute."""
        return self._alert_type

    @property
    def alert_category(self):
        """Treats the alert category type id as a read-only attribute. """
        return self._alert_category.title()

    @property
    def alert_severity(self):
        """Treats the alert severity type id as a read-only attribute. """
        return self._alert_severity

    @alert_severity.setter
    def alert_severity(self, severity):
        """Modifies the Alert severity"""
        if not isinstance(severity, int):
            raise SDKException('Alert', '101')

        self._alert_severity = severity
        self._modify_alert_properties()

    @property
    def alert_criteria(self):
        """Treats the alert criteria as a read-only attribute."""
        return "\n".join([criteria["criteria_value"] for criteria in self._criteria])

    @property
    def notification_types(self):
        """Treats the alert notif types as a read-only attribute."""
        notif_types = []
        for notif, notif_id in self._all_notification_types.items():
            if notif_id in self._notification_types:
                notif_types.append((notif_id, notif.title()))
        return notif_types

    @notification_types.setter
    def notification_types(self, notif_types):
        """Treats the alert notif types as a read-only attribute."""
        if not isinstance(notif_types, list):
            raise SDKException('Alert', '102')
        try:
            ntypes = [self._all_notification_types[ntype.lower()] for ntype in notif_types]
        except KeyError as notif_type:
            raise SDKException(
                'Alert',
                '102',
                'No notification type with name {0} exists'.format(notif_type)
            )
        self._notification_types = ntypes
        self._modify_alert_properties()

    @property
    def entities(self):
        """Treats the alert associations as a read-only attribute. """
        return self._entities_list

    @entities.setter
    def entities(self, entity_json):
        """Modifies the Alert entities"""
        if not isinstance(entity_json, dict):
            raise SDKException('Alert', '101')

        self._entities_list = self._alerts_obj._get_entities(entity_json)
        self._modify_alert_properties()

    @property
    def email_recipients(self):
        """returns the email recipients associated to the alert"""
        return self._email_recipients

    @email_recipients.setter
    def email_recipients(self, email_recipients):
        """Modifies the email_recipients for the alert"""
        self._email_recipients.extend(email_recipients)
        self._modify_alert_properties()

    @property
    def description(self):
        """Treats the alert description as a read-only attribute."""
        return self._description

    @description.setter
    def description(self, description):
        """Modifies the Alert description"""
        self._description = description
        self._modify_alert_properties()
    
    @property
    def users_list(self):
        """Treats the users list as a read-only attribute."""
        return self._users_list

    @users_list.setter
    def users_list(self, users_list):
        """Modifies the users list"""
        self._users_list = users_list
        self._modify_alert_properties()
    
    @property
    def user_group_list(self):
        """Treats the user group list as a read-only attribute."""
        return self._user_group_list

    @user_group_list.setter
    def user_group_list(self, user_group_list):
        """Modifies the user group list"""
        self._user_group_list = user_group_list
        self._modify_alert_properties()

    def enable_notification_type(self, alert_notification_type):
        """Enable the notification type.

            Args:
                alert_notification_type (str)  --  alert notification to enable

            Raises:
                SDKException:
                    if type of alert notification argument is not string

                    if failed to enable notification type

                    if response is empty

                    if response is not success

                    if no notification type exists with the name provided
        """
        if not isinstance(alert_notification_type, str):
            raise SDKException('Alert', '101')

        if alert_notification_type.lower() in self._all_notification_types:
            alert_notification_type_id = self._all_notification_types[
                alert_notification_type.lower()]

            enable_request = self._services['ENABLE_ALERT_NOTIFICATION'] % (
                self.alert_id, alert_notification_type_id
            )

            flag, response = self._cvpysdk_object.make_request(
                'POST', enable_request
            )

            if flag:
                if response.json():
                    error_code = str(response.json()['errorCode'])
                    if error_code == '0':
                        return
                    else:
                        raise SDKException('Alert', '102', response.json()['errorMessage'])
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'Alert',
                '102',
                'No notification type with name {0} exists'.format(alert_notification_type)
            )

    def disable_notification_type(self, alert_notification_type):
        """Disable the notification type.

            Args:
                alert_notification_type (str)  --  alert notification to disable

            Raises:
                SDKException:
                    if type of alert notification argument is not string

                    if failed to disable notification type

                    if response is empty

                    if response is not success

                    if no notification type exists with the name provided
        """
        if not isinstance(alert_notification_type, str):
            raise SDKException('Alert', '101')

        if alert_notification_type.lower() in self._all_notification_types:
            alert_notification_type_id = self._all_notification_types[
                alert_notification_type.lower()]

            disable_request = self._services['DISABLE_ALERT_NOTIFICATION'] % (
                self.alert_id, alert_notification_type_id
            )

            flag, response = self._cvpysdk_object.make_request(
                'POST', disable_request
            )

            if flag:
                if response.json():
                    error_code = str(response.json()['errorCode'])
                    if error_code == '0':
                        return
                    else:
                        raise SDKException('Alert', '102', response.json()['errorMessage'])
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'Alert',
                '102',
                'No notification type with name {0} exists'.format(alert_notification_type)
            )

    def enable(self):
        """Enable an alert.

            Raises:
                SDKException:
                    if failed to enable alert

                    if response is empty

                    if response is not success
        """
        enable_request = self._services['ENABLE_ALERT'] % (self.alert_id)

        flag, response = self._cvpysdk_object.make_request('POST', enable_request)

        if flag:
            if response.json():
                error_code = str(response.json()['errorCode'])

                if error_code == "0":
                    return
                else:
                    error_message = ""

                    if 'errorMessage' in response.json():
                        error_message = response.json()['errorMessage']

                    if error_message:
                        raise SDKException(
                            'Alert', '102', 'Failed to enable Alert\nError: "{0}"'.format(
                                error_message
                            )
                        )
                    else:
                        raise SDKException('Alert', '102', "Failed to enable Alert")
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable(self):
        """Disable an alert.

            Raises:
                SDKException:
                    if failed to disable alert

                    if response is empty

                    if response is not success
        """
        disable_request = self._services['DISABLE_ALERT'] % (self.alert_id)

        flag, response = self._cvpysdk_object.make_request(
            'POST', disable_request
        )

        if flag:
            if response.json():
                error_code = str(response.json()['errorCode'])

                if error_code == "0":
                    return
                else:
                    error_message = ""

                    if 'errorMessage' in response.json():
                        error_message = response.json()['errorMessage']

                    if error_message:
                        raise SDKException(
                            'Alert', '102', 'Failed to disable Alert\nError: "{0}"'.format(
                                error_message
                            )
                        )
                    else:
                        raise SDKException('Alert', '102', "Failed to disable Alert")
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the properties of the Alert."""
        self._get_alert_properties()

    def trigger_test_alert(self):
        """
        Method to trigger the test alert

        Raises:
            SDKException:
                if failed to trigger test alert

                if response is empty

                if response is not success
        """
        test_request = self._services['ALERT_TEST'] % (self.alert_id)

        flag, response = self._cvpysdk_object.make_request('POST', test_request)

        if not flag:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        if not response.json():
            raise SDKException('Response', '102')

        error_code = response.json().get('errorCode', -1)

        if error_code != 0:
            error_message = response.json().get('errorMessage', '')

            raise SDKException(
                'Alert', '102', f'Failed to trigger the test Alert. Error: ["{error_message}"]'
            )
