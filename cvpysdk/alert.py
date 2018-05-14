# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
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

    __len__()                   --  returns the number of alerts configured on the Commcell

    __getitem__()               --  returns the name of the alert for the given alert Id or the
    details for the given alert name

    _get_alert()                --  gets all the alerts associated with the commcell specified

    all_alerts()                --  returns the dict of all the alerts associated
    with the commcell

    has_alert(alert_name)       --  checks whether the alert exists or not

    get(alert_name)             --  returns the alert class object of the input alert name

    delete(alert_name)          --  removes the alerts from the commcell of the specified alert

    console_alerts()            --  returns the list of all console alerts

    refresh()                   --   refresh the alerts associated with the commcell


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

    enable()                      --  enables the alert

    disable()                     --  disables the alert

    enable_notification_type()    --  enables notification type of alert

    disable_notification_type()   --  disables notification type of alert

    refresh()                     --  refresh the properties of the Alert

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from past.builtins import basestring

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
        self._ALERTS = self._commcell_object._services['GET_ALL_ALERTS']

        self._alerts = None
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
        return "Alerts class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

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
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._ALERTS)

        if flag:
            if response.json() and 'alertList' in response.json():
                alerts_dict = {}

                for dictionary in response.json()['alertList']:
                    alert_dict = {}

                    temp_name = dictionary['alert']['name'].lower()
                    temp_id = str(dictionary['alert']['id']).lower()
                    temp_description = dictionary['description'].lower()
                    temp_category = dictionary['alertCategory']['name'].lower()

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
        if not isinstance(alert_name, basestring):
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
        if not isinstance(alert_name, basestring):
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
        """
        if not (isinstance(page_number, int) and isinstance(page_count, int)):
            raise SDKException('Alert', '101')

        console_alerts = self._commcell_object._services['GET_ALL_CONSOLE_ALERTS'] % (
            page_number, page_count)

        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', console_alerts)

        if flag:
            if response.json() and 'totalNoOfAlerts' in response.json():
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
            response_string = self._commcell_object._update_response_(response.text)
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
        if not isinstance(alert_name, basestring):
            raise SDKException('Alert', '101')
        else:
            alert_name = alert_name.lower()

            if self.has_alert(alert_name):
                alert_id = self._alerts[alert_name]['id']
                alert = self._commcell_object._services['ALERT'] % (alert_id)

                flag, response = self._commcell_object._cvpysdk_object.make_request(
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
                    response_string = self._commcell_object._update_response_(response.text)
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
        self._alert_name = alert_name.lower()

        if alert_id:
            self._alert_id = str(alert_id)
        else:
            self._alert_id = self._get_alert_id()

        if alert_category:
            self._alert_category = alert_category
        else:
            self._alert_category = self._get_alert_category()

        self._ALERT = self._commcell_object._services['ALERT'] % (self.alert_id)
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

        self._criteria = {}
        self._description = None
        self._alert_type = None

        self.refresh()

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
                alert_detail = response.json()['alertDetail']

                if 'criteria' in alert_detail:
                    criteria = alert_detail['criteria'][0]

                    criteria_value = None
                    criteria_id = None
                    escalation_level = None

                    if 'value' in criteria:
                        criteria_value = criteria['value']

                    if 'criteriaId' in criteria:
                        criteria_id = str(criteria['criteriaId'])

                    if 'esclationLevel' in criteria:
                        escalation_level = criteria['esclationLevel']

                    self._criteria = {
                        'criteria_value': criteria_value,
                        'criteria_id': criteria_id,
                        'esclation_level': escalation_level
                    }

                if 'alert' in alert_detail:
                    alert = alert_detail['alert']

                    if 'description' in alert:
                        self._description = alert['description']

                    if 'alertType' in alert and 'name' in alert['alertType']:
                        self._alert_type = alert['alertType']['name']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def alert_name(self):
        """Treats the alert name as a read-only attribute."""
        return self._alert_name

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
        return self._alert_category

    @property
    def description(self):
        """Treats the alert description as a read-only attribute."""
        return self._description

    @property
    def criteria(self):
        """Treats the alert criteria as a read-only attribute."""
        return self._criteria

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
        if not isinstance(alert_notification_type, basestring):
            raise SDKException('Alert', '101')

        if alert_notification_type.lower() in self._all_notification_types:
            alert_notification_type_id = self._all_notification_types[
                alert_notification_type.lower()]

            enable_request = self._commcell_object._services['ENABLE_ALERT_NOTIFICATION'] % (
                self.alert_id, alert_notification_type_id
            )

            flag, response = self._commcell_object._cvpysdk_object.make_request(
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
                response_string = self._commcell_object._update_response_(response.text)
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
        if not isinstance(alert_notification_type, basestring):
            raise SDKException('Alert', '101')

        if alert_notification_type.lower() in self._all_notification_types:
            alert_notification_type_id = self._all_notification_types[
                alert_notification_type.lower()]

            disable_request = self._commcell_object._services['DISABLE_ALERT_NOTIFICATION'] % (
                self.alert_id, alert_notification_type_id
            )

            flag, response = self._commcell_object._cvpysdk_object.make_request(
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
                response_string = self._commcell_object._update_response_(response.text)
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
        enable_request = self._commcell_object._services['ENABLE_ALERT'] % (self.alert_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', enable_request)

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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable(self):
        """Disable an alert.

            Raises:
                SDKException:
                    if failed to disable alert

                    if response is empty

                    if response is not success
        """
        disable_request = self._commcell_object._services['DISABLE_ALERT'] % (self.alert_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the properties of the Alert."""
        self._get_alert_properties()
