# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing identity management operations

IdentityManagementApps and IdentityManagementApp are the classes defined in this file

IdentityManagementApps: Class for representing all the identity management apps in the commcell

IdentityManagementApp: Class for representing a single identity management app in the commcell

IdentityManagementApps
======================

    __init__(commcell_object)   --  initialise object of identity management apps
    class of the commcell

    __str__()                   --  returns all the apps identity management apps
    in the commcell

    __repr__()                  --  returns the string for the instance of the
    identity management apps

    _get_apps()                 --  gets all the identity management appsin the commcell

    get_local_identity_app     --  gets the local identity app of the commcell

    get_commcell_identity_apps --  gets the list of commcell identity apps of the commcell

    delete_identity_app         --  deletes the specified local identity app

    configure_local_identity_app    --  sets up the local identity app for the specified commcell

    configure_commcell_app      --  creates a commcell identity app for the specified commcell

    refresh()                   --  refresh the apps in the commcell


IdentityManagementApp
======================
    __init__()                  --  initialize instance of the IdentityManagementApp instance

    __repr__()                  -- return the appname name, the instance it is associated with

    _get_app_key()              -- gets the app key

    _get_app_details            --  gets the details of the identity management app

    refresh()                   -- refresh the details of the app
"""

import time

from past.builtins import basestring

from .exception import SDKException


class IdentityManagementApps(object):
    """Class for representing third party apps in the commcell"""

    def __init__(self, commcell_object):
        """Initialize object of third party apps class.

            Args:
                commcell_object    (object)    --  instance of the Commcell class

            Returns:
                object - instance of ThirdPartyApps class
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._update_response_ = commcell_object._update_response_
        self._APPS = commcell_object._services['IDENTITY_APPS']
        self._apps = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all identity management apps of the Commcell.

            Returns:
                str -   string of all the identity management apps in a commcell
        """
        representation_string = "{:^5}\t{:^50}\n\n".format('S. No.', 'App')

        for index, app in enumerate(self._apps):
            sub_str = '{:^5}\t{:30}\n'.format(index + 1, app)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the IdentityManagementApps class."""
        return "IdentityManagementApps class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def __len__(self):
        """Returns the number of the app added to the Commcell."""
        return len(self.all_apps)

    def _get_apps(self):
        """Gets list of all third party apps.

            Returns:
                dict - consisits of all thrid party apps in the commcell
                        {
                            "app1_name": app1_props
                            "app2_name": app2_props
                        }

            Raises:
                SDKException:
                        if response is not success
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._APPS
        )

        if flag:
            apps = {}

            if response.json() and 'clientThirdPartyApps' in response.json():
                response_value = response.json()['clientThirdPartyApps']

                for app in response_value:
                    apps[app['appName']] = {
                        'appKey': app['appKey'],
                        'appType': app['appType']
                    }
                return apps
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get(self, app_name):
        """Returns a identitymanagementapp object of the specified app name

            Args:
                app_name    (str)   --  name of the app

            Returns:
                object  -   instance of IdentityManagementApp class for the given app name

            Raises:
                SDKException:
                    if type of the app name argument is not string
        """
        if not isinstance(app_name, basestring):
            raise SDKException('IdentityManagement', '101')
        else:
            return IdentityManagementApp(
                self._commcell_object,
                app_name,
                self._apps[app_name]['appKey']
            )

    @property
    def get_local_identity_app(self):
        """Returns the local identity app details for IDP commcell

            Returns:
                object    -   object of IdentityManangementApp class
        """
        app_list = self._apps
        if app_list:
            for app in app_list.keys():
                if app_list[app]['appType'] is 4:
                    return self.get(app)

    @property
    def get_commcell_identity_apps(self):
        """Returns a list of commcell apps for the local commcell

            Returns:
                list    -   List containing commcell apps in the SP commcell

                    [
                        app1_obj,
                        app2_obj
                    ]
        """
        app_list = self._apps
        commcell_apps = []
        if app_list:
            for app in app_list.keys():
                if app_list[app]['appType'] is 3:
                    commcell_apps.append(self.get(app))
            if commcell_apps:
                return commcell_apps

    @property
    def all_apps(self):
        """Returns the dictionary consisting of all the ID apps added to the Commcell.

            dict - consists of all the apps configured on the commcell

                {
                    "app1_name": app1_id,

                    "app2_name": app2_id
                }

        """
        return self._apps

    def delete_identity_app(self, app):
        """Deletes the specified local identity app

            Args:
                app     (object)      -- object containing app details

            Returns:
                bool    -   True if operation succeeds

            Raises:
                SDKException:
                    if passed app not found

                    if failure in response
        """
        draft_json = app._get_app_details()

        if draft_json:
            req_json = {
                'opType': 2,
                'clientThirdPartyApps': [
                    draft_json
                ]
            }
        else:
            raise SDKException('IdentityManagement', '102')

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._APPS, req_json
        )
        if flag:
            if response.json() and 'error' in response.json():
                if response.json()['error']['errorCode'] is 0:
                    self.refresh()
                else:
                    raise SDKException(
                        'Response',
                        '101',
                        response.json()['error']['warningMessage']
                    )
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def configure_local_identity_app(self, user_list=None):
        """Creates a local identity app by associating speccified users

            Args:
                user_list      (list)     --  list of objects to be associated
                                              with identity server

            Returns:
                object  -   returns object of IdentityManagementApp class

            Raises:
                SDKException:
                    if failed to configure identity app
        """
        third_party_json = {
            'opType': 1,
            'clientThirdPartyApps': [
                {
                    'appType': 4,
                    'isEnabled': True,
                    'assocTree': [
                        {
                            'userId': user_obj.user_id,
                            '_type_': 13
                        } for user_obj in user_list
                    ]
                }
            ]
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._APPS, third_party_json
        )

        if flag:
            if response.json() and 'error' in response.json():
                if response.json()['error']['errorCode'] is 0:
                    self.refresh()
                    return self.get_local_identity_app
                else:
                    raise SDKException(
                        'IdentityManagement',
                        '103',
                        ' - error {0}'.format(response.json()['error']['errorString'])
                    )
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('', '101', response_string)

    def configure_commcell_app(self,
                               IDP_props,
                               app_name,
                               user_assoc_list=None,
                               user_mappings=None):
        """Creates a commcell app by associating speccified users

            Args:
                IDP_props      (dict)     --  dict containing properties of the IDP's identity app

                app_name       (str)      --  GUID for the app

                user_assoclist (list)     --  list of users for association

                user_mappings  (dict)     --  dict containing mapping of IDP user to local user

            Returns:
                object  -   returns object of IdentityManagementApp class

            Raises:
                SDKException:
                    if failed to configure identity app
        """
        third_party_json = {
            'opType': 1,
            'clientThirdPartyApps': [
                {
                    'appName': app_name,
                    'appDisplayName': 'Auto_IDP_Commcell_app_{0}'.format(time.time()),
                    'appDescription': 'Auto created app',
                    'flags': 0,
                    'appType': 3,
                    'isEnabled': True,
                    'UserMappings': {
                        'opType': 2,
                        'userslist': [
                            {
                                'userfromToken': spuser,
                                "localuser": {
                                    "userId": user_mappings[spuser].user_id
                                }
                            } for spuser in user_mappings
                        ]
                    },
                    'props': {
                        'nameValues': IDP_props
                    },
                    'assocTree': [
                        {
                            'userId': user_obj.user_id,
                            '_type_': 13
                        } for user_obj in user_assoc_list
                    ]
                }
            ]
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._APPS, third_party_json
        )

        if flag:
            if response.json() and 'error' in response.json():
                if response.json()['error']['errorCode'] is 0:
                    self.refresh()
                    return self.get_commcell_identity_apps
                else:
                    raise SDKException(
                        'IdentityManagement',
                        '103',
                        ' - error {0}'.format(response.json()['error']['errorString'])
                    )
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('', '101', response_string)

    def refresh(self):
        """Refresh the apps associated with the Commcell."""
        self._apps = self._get_apps()


class IdentityManagementApp(object):
    """Class for performing operations on a specific identity management app"""

    def __init__(self, commcell_object, app_name, app_key=None):
        """Initialize the app class

            Args:
                commcell_object     (object)    --  instance of the commcell class

                app_name            (str)       --  name of the app

                app_key             (str)       --  key of the app
                    default: None

            Returns:
                object - instance of the IdentityManagementApp class
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._update_response_ = commcell_object._update_response_

        self._app_name = app_name
        self._app_description = None
        self._flags = None
        self._app_type = None
        self._app_type_dict = {
            1: 'Regular',
            2: 'SAML',
            3: 'CommCell',
            4: 'Local Identity',
            5: 'OpenId Connect'
        }
        self._is_enabled = None
        self._app_displayname = None

        if app_key:
            self._app_key = app_key
        else:
            self._app_key = self._get_app_key()

        self._APPS = commcell_object._services['IDENTITY_APPS']

        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'IdentityManagementApp class instance for app: \
                                "{0}", of Commcell: "{1}"'

        return representation_string.format(
            self._app_name, self._commcell_object.commserv_name
        )

    def _get_app_key(self):
        """Gets the key of app associated to this object

            Returns:
                str - key associated with this app
        """
        apps = IdentityManagementApps(self._commcell_object)
        return apps.get(self.app_name).app_key

    def _get_app_details(self):
        """Returns a dict containing the details of a third party app.

            Returns:
                dict    -   details of the identity app app

            Raises:
                SDKException:
                        if response is not success
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._APPS
        )

        if flag:
            if response.json() and 'clientThirdPartyApps' in response.json():
                response_value = response.json()['clientThirdPartyApps']
                for app in response_value:
                    if app['appKey'] == self._app_key:
                        if 'appDescription' in app:
                            self._app_description = app['appDescription']

                        if 'flags' in app:
                            self._flags = app['flags']

                        if 'appType' in app:
                            self._app_type = self._app_type_dict[app['appType']]

                        if 'isEnabled' in app:
                            self._is_enabled = app['isEnabled']

                        return app
            else:
                raise SDKException('IdentityManagement', '101')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the properties of the app."""
        self._properties = self._get_app_details()

    @property
    def app_name(self):
        """Treats the app name as a read-only attribute."""
        return self._app_name

    @property
    def app_key(self):
        """Treats the app key as a read-only attribute."""
        return self._app_key

    @property
    def app_description(self):
        """Treats the app description as a read-only attribute."""
        return self._app_description

    @property
    def app_type(self):
        """Treats the app type as a read-only attribute."""
        return self._app_type

    @property
    def is_enabled(self):
        """Treats the enabled peroperty as a read-only attribute."""
        return self._is_enabled

    @property
    def flags(self):
        """Treats the app flags as a read-only attribute."""
        return self._flags
