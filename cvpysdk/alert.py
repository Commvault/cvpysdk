#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See License.txt in the project root for
# license information.
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
    _get_alert()                --  gets all the alerts associated with the commcell specified
    has_alert(alert_name)       --  checks whether the alert exists or not
    get(alert_name)             --  returns the alert class object of the input alert name
    delete(alert_name)          --  removes the alerts from the commcell of the specified alert
    console_alerts()            --  returns the list of all console alerts

Alert:
    __init__(commcell_object,
             alert_name,
             alert_id=None)     --  initialise object of alert with the specified commcell name
                                        and id, and associated to the specified commcell
    __repr__()                  --  return the alert name with description and category,
                                        the alert is associated with
    _get_alert_id()             --  method to get the alert id, if not specified in __init__
    _get_alert_properties()     --  get the properties of this alert
    _get_alert_category()       --  return the category of the alert
    enable()                    --  enables the alert
    disable()                   --  disables the alert
    enable_notification_type    --  enables notification type of alert
    disable_notification_type   --  disables notification type of alert

"""

from exception import SDKException


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
        self._ALERTS = self._commcell_object._services.GET_ALL_ALERTS
        self._alerts = self._get_alerts()

    def __str__(self):
        """Representation string consisting of all alerts of the Commcell.

            Returns:
                str - string of all the alerts for a commcell
        """
        representation_string = "{:^5}\t{:^50}\t{:^50}\t{:^30}\n\n".format(
            'S. No.', 'Alert', 'Description', 'Category')

        for index, alert_name in enumerate(self._alerts):
            alert_description = self._alerts[alert_name]['description']
            alert_category = self._alerts[alert_name]['category']
            sub_str = '{:^5}\t{:50}\t{:^50}\t{:^30}\n'.format(
                index + 1,
                alert_name,
                alert_description,
                alert_category
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Alerts class."""
        return "Alerts class instance for Commcell: '{0}'".format(
            self._commcell_object._headers['Host']
        )

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
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._ALERTS)

        if flag:
            if response.json():
                alerts_dict = {}
                alert_dict = {}

                for dictionary in response.json()['alertList']:
                    temp_name = str(dictionary['alert']['name']).lower()
                    temp_id = str(dictionary['alert']['id']).lower()
                    temp_description = str(dictionary['description']).lower()
                    temp_category = str(dictionary['alertCategory']['name']).lower()

                    alert_dict['id'] = temp_id
                    alert_dict['description'] = temp_description
                    alert_dict['category'] = temp_category
                    alerts_dict[temp_name] = alert_dict

                return alerts_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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
            raise SDKException('Alert', '103')

        return self._alerts and str(alert_name).lower() in self._alerts

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
            raise SDKException('Alert', '103')
        else:
            alert_name = str(alert_name).lower()

            if self.has_alert(alert_name):
                return Alert(self._commcell_object, alert_name,
                             self._alerts[alert_name]['id'],
                             self._alerts[alert_name]['category'])

            raise SDKException('Alert',
                               '104',
                               'No Alert exists with name: {0}'.format(alert_name))

    def console_alerts(self, page_number=1, page_count=1):
        """Prints the console alerts from page_number to the number of pages asked for page_count

            Args:
                page_number (int)  --  page number to get the alerts from
                page_count  (int)  --  number of pages to get the alerts of

            Raises:
                SDKException:
                    if type of the page number and page count argument is not int
                    if response is empty
                    if response is not success
        """
        if not (isinstance(page_number, int) and isinstance(page_count, int)):
            raise SDKException('Alert', '103')

        console_alerts = self._commcell_object._services.GET_ALL_CONSOLE_ALERTS % (
            page_number, page_count)

        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', console_alerts)

        if flag:
            if response.json() and 'totalNoOfAlerts' in response.json():
                print "Total Console Alerts found: {0}".format(response.json()['totalNoOfAlerts'])

                o_str = "{:^5}\t{:^50}\t{:^50}\t{:^50}\n\n".format(
                    'S. No.', 'Alert', 'Type', 'Criteria')

                for index, dictionary in enumerate(response.json()['feedsList']):
                    o_str += '{:^5}\t{:50}\t{:^50}\t{:^50}\n'.format(
                        index + 1,
                        dictionary['alertName'],
                        dictionary['alertType'],
                        dictionary['alertcriteria']
                    )

                print o_str
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def delete(self, alert_name):
        """Deletes the alert from the commcell.

            Args:
                alert_name (str)  --  name of the alert

            Returns:
                None

            Raises:
                SDKException:
                    if type of the alert name argument is not string
                    if failed to delete the alert
                    if no alert exists with the given name
        """
        if not isinstance(alert_name, str):
            raise SDKException('Alert', '103')
        else:
            alert_name = str(alert_name).lower()

            if self.has_alert(alert_name):
                alert_id = self._alerts[alert_name]
                alert = self._commcell_object._services.ALERT % (alert_id)

                flag, response = self._commcell_object._cvpysdk_object.make_request('DELETE',
                                                                                    alert)

                if flag:
                    if response.json():
                        if 'errorCode' in response.json():
                            if response.json()['errorCode'] == 0:
                                o_str = 'Alert: "{0}" deleted successfully'
                                print o_str.format(alert_name)
                                self._alerts = self._get_alerts()
                            else:
                                print response.json()['errorMessage']
                    else:
                        raise SDKException('Response', '102')
                else:
                    exception_message = 'Failed to delete the Alert: {0}'.format(alert_name)
                    response_string = self._commcell_object._update_response_(response.text)
                    exception_message += "\n" + response_string

                    raise SDKException('Alert', '104', exception_message)
            else:
                raise SDKException('Alert',
                                   '104',
                                   'No alert exists with name: {0}'.format(alert_name))


class Alert(object):
    """Class for performing operations for a specific alert."""

    def __init__(self, commcell_object, alert_name, alert_id=None, alert_category=None):
        """Initialise the Alert class instance.

            Args:
                commcell_object (object)  --  instance of the Commcell class
                alert_name (str)          --  name of the alert
                alert_id (str)            --  id of the alert
                    default: None
                alert_category (str)      --  name of the alert category
                    default: None

            Returns:
                object - instance of the ALert class
        """
        self._commcell_object = commcell_object
        self._alert_name = str(alert_name).lower()

        if alert_id:
            self._alert_id = str(alert_id)
        else:
            self._alert_id = self._get_alert_id()

        if alert_category:
            self._alert_category = str(alert_category)
        else:
            self._alert_category = self._get_alert_category()

        self._ALERT = self._commcell_object._services.ALERT % (self.alert_id)
        self.properties = self._get_alert_properties()
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

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Alert class instance for Alert: "{0}", Notification Type: "{1}"'
        return representation_string.format(self.alert_name, self.alert_category)

    def _get_alert_id(self):
        """Gets the alert id associated with this alert.

            Returns:
                str - id associated with this alert
        """
        alerts = Alerts(self._commcell_object)
        return alerts.get(self.alert_name).alert_id

    def _get_alert_category(self):
        """Gets the alert category associated with this alert.

            Returns:
                str - alert category name associated with this alert
        """
        alerts = Alerts(self._commcell_object)
        return alerts.get(self.alert_name).alert_category

    def _get_alert_properties(self):
        """Gets the alert properties of this alert.

            Returns:
                dict - dictionary consisting of the properties of this alert

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._ALERT)

        if flag:
            if response.json() and 'alertDetail' in response.json().keys():
                return response.json()['alertDetail']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def alert_id(self):
        """Treats the alert id as a read-only attribute."""
        return self._alert_id

    @property
    def alert_category(self):
        """Treats the alert category type id as a read-only attribute. """
        return self._alert_category

    @property
    def alert_name(self):
        """Treats the alert name as a read-only attribute."""
        return self._alert_name

    def enable_notification_type(self, alert_notification_type):
        """Enable the notification type.

            Args:
                alert_notification_type (str)  --  alert notification to enable

            Returns:
                None

            Raises:
                SDKException:
                    if type of alert notification argument is not string
                    if response is empty
                    if response is not success
                    if no notification type exists with the name provided
        """
        if not isinstance(alert_notification_type, str):
            raise SDKException('Alert', '103')

        if alert_notification_type.lower() in self._all_notification_types:
            alert_notification_type_id = self._all_notification_types[
                alert_notification_type.lower()]

            enable_request = self._commcell_object._services.ENABLE_ALERT_NOTIFICATION % (
                self.alert_id, alert_notification_type_id
            )

            flag, response = self._commcell_object._cvpysdk_object.make_request('POST',
                                                                                enable_request)

            if flag:
                if response.json():
                    error_code = str(response.json()['errorCode'])
                    if error_code is '0':
                        print "Notification Type enabled successfully"
                    else:
                        print str(response.json()['errorMessage'])
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'Alert',
                '104',
                'No notification type with name {0} exists'.format(alert_notification_type))

    def disable_notification_type(self, alert_notification_type):
        """Disable the notification type.

            Args:
                alert_notification_type (str)  --  alert notification to disable

            Returns:
                None

            Raises:
                SDKException:
                    if type of alert notification argument is not string
                    if response is empty
                    if response is not success
                    if no notification type exists with the name provided
        """
        if not isinstance(alert_notification_type, str):
            raise SDKException('Alert', '103')

        if alert_notification_type.lower() in self._all_notification_types:
            alert_notification_type_id = self._all_notification_types[
                alert_notification_type.lower()]

            disable_request = self._commcell_object._services.ENABLE_ALERT_NOTIFICATION % (
                self.alert_id, alert_notification_type_id
            )

            flag, response = self._commcell_object._cvpysdk_object.make_request('POST',
                                                                                disable_request)

            if flag:
                if response.json():
                    error_code = str(response.json()['errorCode'])
                    if error_code is '0':
                        print "Notification Type disabled successfully"
                    else:
                        print str(response.json()['errorMessage'])
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'Alert',
                '104',
                'No notification type with name {0} exists'.format(alert_notification_type))

    def enable(self):
        """Enable an alert.

            Returns:
                None

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        enable_request = self._commcell_object._services.ENABLE_ALERT % (self.alert_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', enable_request)

        if flag:
            if response.json():
                print str(response.json()['errorMessage'])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable(self):
        """Disable an alert.

            Returns:
                None

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        disable_request = self._commcell_object._services.DISABLE_ALERT % (self.alert_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request('POST',
                                                                            disable_request)

        if flag:
            if response.json():
                print str(response.json()['errorMessage'])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
