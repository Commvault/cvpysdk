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

"""Main file for performing identity management operations

IdentityManagementApps, IdentityManagementApp and SamlApp are the classes defined in this file

IdentityManagementApps: Class for representing all the identity management apps in the commcell

IdentityManagementApp: Class for representing a single identity management app in the commcell

SamlApp: class for representing a single saml app in commcell

IdentityManagementApps
======================

    __init__(commcell_object)       --  initialise object of identity management apps
    class of the commcell

    __str__()                       --  returns all the apps identity management apps
    in the commcell

    __repr__()                      --  returns the string for the instance of the
    identity management apps

    _get_apps()                     --  gets all the identity management appsin the commcell

    get_local_identity_app          --  gets the local identity app of the commcell

    get_commcell_identity_apps      --  gets the list of commcell identity apps of the commcell

    delete_identity_app()           --  deletes the specified local identity app

    delete_saml_app()               --  deletes the specified saml app

    get_saml_apps()                 --  get the list of all the saml apps in the commcell

    get_saml()                      --  returns instance of SamlApp class

    configure_saml_app()            --  creates a saml app

    configure_local_identity_app()  --  sets up the local identity app for the specified commcell

    configure_commcell_app()        --  creates a commcell identity app for the specified commcell

    configure_openid_app()          --  creates a OpenID app for the specified commcell

    refresh()                       --  refresh the apps in the commcell


IdentityManagementApp
======================
    __init__()                  --  initialize instance of the IdentityManagementApp instance

    __repr__()                  -- return the appname name, the instance it is associated with

    properties                  -- holds the updated properties of app

    get_app_props()             -- returns a dict containing the properties of a third party app
                                   (via qoperation)

    refresh()                   -- refresh the details of the app


SamlApp
======================
    __init__()                   --  initialize instance of the SamlApp instance

    __repr__()                   -- return the appname name, the instance it is associated with

    _get_saml_details()          -- gets details of saml app

    modify_saml_app()            --  modifies saml app

    refresh()                    -- refresh the details of the saml app

    saml_app_details()           --  gets saml app details in dict

    get_saml_user_redirect_url() -- gets redirect url of saml user

    set_auto_redirect_to_idp()   -- Enable/Disable auto redirect to IDP


SamlApp instance Attributes
============================

    **is_saml_app_enabled**         --  returns True if saml app is enabled, False otherwise

    **is_auto_create_user**         --  returns True if auto create user flag is enabled, False otherwise

    **saml_app_default_user_groups** -  returns list of dict of default usergroups of saml app

    **saml_app_nameid_attribute**   --  returns value of NameId attribute of saml app

    **saml_app_attribute_mappings** --  returns attribute mappings of saml app

    **saml_app_identity_provider_metadata** -   returns IDP metadata of saml app

    **saml_app_service_provider_metadata**  -   returns SP metadata of saml app

    **saml_app_associations**       --  returns saml app associations

    **is_company_saml_app**         -- returns True if saml app is created for a company, False otherwise
"""

import xml.etree.ElementTree as ET
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
        self._ADD_SAML = commcell_object._services['ADD_OR_GET_SAML']
        self._SAML = commcell_object._services['EDIT_SAML']
        self._LOCAL_APP = commcell_object._services['LOCAL_APP']
        self._V4_IDENTITY_SERVERS = commcell_object._services['V4_IDENTITY_SERVERS']
        self._apps = None
        self._local_app = None
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
        return "IdentityManagementApps class instance for Commcell"

    def __len__(self):
        """Returns the number of the app added to the Commcell."""
        return len(self.all_apps)

    def _get_apps(self, hard=False):
        """Gets list of all third party apps.

            Returns:
                dict - consisits of all thrid party apps in the commcell
                        {
                            'app1_name': {
                                'appKey': app1_key,
                                'appType': app1_type,
                                'appDescription': 'app1_description',
                                'flags': 'app1_flags',
                                'isEnabled': 'app1_isEnabled'
                            },
                            'app2_name': {
                                'appKey': app2_key,
                                'appType': app2_type,
                                'appDescription': 'app1_description',
                                'flags': 'app1_flags',
                                'isEnabled': 'app1_isEnabled'
                            }
                        }

            Raises:
                SDKException:
                        if response is not success
        """
        if hard:
            self._cvpysdk_object.make_request(
                'GET', self._APPS + '?hardRefresh=true'
            )
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._APPS
        )

        if flag:
            apps = {}

            if response.json() and 'clientThirdPartyApps' in response.json():
                response_value = response.json()['clientThirdPartyApps']

                for app in response_value:
                    apps[app['appName'].lower()] = {
                        'appKey': app['appKey'],
                        'appType': app['appType'],
                        'appDescription': app['appDescription'],
                        'flags': app['flags'],
                        'isEnabled': app['isEnabled']
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
        if not isinstance(app_name, str):
            raise SDKException('IdentityManagement', '101')
        else:
            app_name = app_name.lower()
            if self.has_identity_app(app_name):
                return IdentityManagementApp(
                    self._commcell_object,
                    app_name,
                    self._apps[app_name]
                )

            raise SDKException('IdentityManagement', '102')

    def get_saml_apps(self):
        """Returns a list of all SAML apps in the commcell

            Returns:
                list    -   List containing dicts for all SAML apps

                    [
                        {
                            'id': 1097,
                            'name': 'c1',
                            'type': 'SAML',
                            'samlType': 'ADFS',
                            'company': {'id': 384, 'name': 'c1'},
                            'configured': True
                        },
                        ...
                    ]

            Raises:
                SDKException:
                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._V4_IDENTITY_SERVERS
        )

        if flag:
            saml_apps = []
            if response.json() and 'identityServers' in response.json():
                identity_servers = response.json()['identityServers']

                for server in identity_servers:
                    if server.get('type') == 'SAML':
                        saml_apps.append(server)

            return saml_apps
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_saml(self, app_name):
        """Returns a SamlApp object of the specified app name

            Args:
                app_name    (str)   --  name of the saml app

            Returns:
                object  -   instance of SamlApp class for the given app name

            Raises:
                SDKException:
                    if type of the app name argument is not string
        """
        if not isinstance(app_name, str):
            raise SDKException('IdentityManagement', '101')
        else:
            app_name = app_name.lower()
            if self.has_identity_app(app_name):
                return SamlApp(
                    self._commcell_object,
                    app_name
                )

            raise SDKException('IdentityManagement', '102')

    @property
    def get_local_identity_app(self):
        """Returns the local identity app details for IDP commcell

            Returns:
                object    -   object of IdentityManangementApp class
        """
        if self._local_app is None:
            flag, response = self._cvpysdk_object.make_request('GET', self._LOCAL_APP)
            if flag:
                if response.json() and 'clientThirdPartyApps' in response.json():
                    local_apps = response.json()['clientThirdPartyApps']
                    if local_apps:
                        local_app = local_apps[0]
                        self._local_app = IdentityManagementApp(
                            self._commcell_object,
                            local_app['appName'],
                            local_app
                        )
                if self._local_app is None:
                    raise SDKException('IdentityManagement', '102', 'No local identity app found')
            else:
                response_string = self._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

        return self._local_app

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
        commcell_apps = []
        if self._apps:
            for app in self._apps:
                if self._apps[app]['appType'] == 3:
                    commcell_apps.append(self.get(app))
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

    def delete_identity_app(self, app_name):
        """Deletes the specified local identity app

            Args:
                app_name     (str)      -- name of the app to be deleted

            Returns:
                bool    -   True if operation succeeds

            Raises:
                SDKException:
                    if passed app not found

                    if failure in response
        """
        draft_json = self._apps.get(app_name)

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
                if response.json()['error']['errorCode'] == 0:
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

    def delete_saml_app(self, app_name):
        """Deletes the specified saml app
            Args:
                app_name       (string) name of the saml app

            Raises :
                SDK Exception :
                    if failure in response
                    if invalid response
        """
        flag, response = self._cvpysdk_object.make_request(
            'DELETE', self._SAML % app_name
        )
        if flag:
            if response.json() and 'errorCode' in response.json():
                if response.json()['errorCode'] == 0:
                    self.refresh()
                else:
                    raise SDKException(
                        'IdentityManagement',
                        '104',
                        ' - error {0}'.format(response.json()['errorMessage'])
                    )
            else:
                raise SDKException('Response', '500' + 'Invalid Response Returned')

        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def configure_saml_app(self, app_name, desc, idp_metadata, sp_metadata, associations):
        """Creates a saml app

            Args:
                app_name        (string)    saml app name

                desc            (string)    saml app description

                idp_metadata   (dict)  idp_metadata = {
                                            'entityId' : '',
                                            'redirectUrl' : '',
                                            'logoutUrl' : '',
                                            'certificateData': '',
                                            'SAMLProtocolVersion' : "urn:oasis:names:tc:SAML:2.0:metadata"
                                        }
                sp_metadata      (dict)  dict of serviceProviderEndpoint, autoGenerateSPMetaData, jksFileContents
                                        sp_metadata = {
                                            "serviceProviderEndpoint": "https://test.mydomain:443/webconsole",
                                            "autoGenerateSPMetaData": true,
                                            "jksFileContents":[]
                                        }
                associations    (dict)  dict of email suffixes, companies, domains and usergroups
                                        associations = {
                                            'emails' = ['a.com', b.com'],
                                            'companies' = [],
                                            'domains' = [],
                                            'usergroups'= []
                                        }

            Returns:
                object - returns object of SamlApp class

            Raises:
                SDKException:   if failure in response
                                if invalid response
        """
        req_body = {
            "name": app_name,
            "description": desc,
            "identityProviderMetaData": idp_metadata,
            "serviceProviderMetaData": sp_metadata,
            "associations": associations
        }
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_SAML, req_body
        )

        if flag:
            if response.json() and 'errorCode' in response.json():
                if response.json()['errorCode'] == 0:
                    self.refresh()
                    return SamlApp(
                        self._commcell_object,
                        app_name
                    )
                else:
                    raise SDKException(
                        'IdentityManagement',
                        '103',
                        ' - error {0}'.format(response.json()['errorMessage'])
                    )
            else:
                raise SDKException('Response', '500' + 'Invalid Response Returned')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def configure_local_identity_app(self, user_list=None, optype=1):
        """Creates a local identity app by associating speccified users

            Args:
                user_list      (list)     --  list of names of users to be associated
                                              with identity server
                optype         (int)      --  operation type, 1 is 'create', 3 is 'overwrite'

            Returns:
                object  -   returns object of IdentityManagementApp class

            Raises:
                SDKException:
                    if failed to configure identity app
        """
        if user_list is None:
            user_list = []
        if str(user_list).lower() == 'all':
            users_list = [{'_type_': 12}]
        else:
            users_list = [
                {'userId': self._commcell_object.users.all_users[user_name], '_type_': 13}
                for user_name in user_list
            ]

        third_party_json = {
            'opType': optype,
            'clientThirdPartyApps': [
                {
                    'appType': 4,
                    'appName': self.get_local_identity_app.app_name,
                    'assocTree': users_list
                }
            ]
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._APPS, third_party_json
        )

        if flag:
            if response.json() and 'error' in response.json():
                if response.json()['error']['errorCode'] == 0:
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
                               idp_props,
                               app_name,
                               app_display_name,
                               app_description='',
                               user_assoc_list=None,
                               user_mappings=None):
        """Creates a commcell app by associating speccified users

            Args:
                idp_props      (list)     --  dict containing properties of the IDP's identity app

                    [
                        {
                            "name": "SP Certificate Data",
                            "value: "certificate1_str"
                        },
                        {
                            "name": "JKS Private Key",
                            "value: "key1_str"
                        },
                        {
                            "name": "CommcellId",
                            "value": "id1"
                        },
                        {
                            "name": "RedirectUrl",
                            "value": "url1"
                        }
                    ]

                app_name       (str)      --  GUID for the app

                app_display_name (str)    --  display name for the app

                app_description  (str)    --  description for the app

                user_assoc_list (list)    --  list of users for association

                user_mappings  (dict)     --  dict containing mapping of IDP user to local user

                    {
                        "idp1_user":  "sp1_user",

                        "idp2_user":  "sp2_user"
                    }

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
                    'appDisplayName': app_display_name,
                    'appDescription': app_description,
                    'flags': 0,
                    'appType': 3,
                    'isEnabled': True,
                    'UserMappings': {
                        'opType': 2,
                        'userslist': [
                            {
                                'userfromToken': spuser,
                                "localuser": {
                                    "userId": self._commcell_object.users.all_users[
                                        user_mappings[spuser]
                                    ]
                                }
                            } for spuser in user_mappings
                        ]
                    },
                    'props': {
                        'nameValues': idp_props
                    },
                    'assocTree': [
                        {
                            'userId': self._commcell_object.users.all_users[user_name],
                            '_type_': 13
                        } for user_name in user_assoc_list
                    ]
                }
            ]
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._APPS, third_party_json
        )

        if flag:
            if response.json() and 'error' in response.json():
                if response.json()['error']['errorCode'] == 0:
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

    def configure_openid_app(self, appname, props, user_to_be_added):
        """
        Adding OpenID app

        Args:
            appname (str)           :       Name of the app to be created

            props      (list)       :  dict containing properties of the IDP's identity app

                    [
                        {
                                "name": "clientId",
                                "value": "13445"
                            },
                            {
                                "name": "clientSecret",
                                "value": "ABC13567"
                            },
                            {
                                "name": "endPointUrl",
                                "value": "https://test.okta.com/.well-known/openid-configuration"
                            },
                            {
                                "name": "webConsoleUrls",
                                "values": [
                                    https://mydomain:443/webconsole
                                ]
                            }
                    ]

            user_to_be_added   (list) :   list of users for association

        Raises:
            SDKException:
                if failed to configure identity app

        """
        third_party_json = {
                "opType": 1,
                "clientThirdPartyApps": [
                    {
                        "appDescription": "",
                        "appDisplayName": appname,
                        "appName": appname,
                        "flags": 0,
                        "appType": 5,
                        "isEnabled": True,
                        "props": {
                            "nameValues": props
                        },
                        "assocTree": [
                            {
                                "_type_": 13,
                                "userName": user_name
                            } for user_name in user_to_be_added
                        ]
                    }
                ]

        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._APPS, third_party_json
        )

        if flag:
            if response.json() and 'error' in response.json():
                if response.json()['error']['errorCode'] == 0:
                    self.refresh()
                else:
                    raise SDKException(
                        'IdentityManagement',
                        '103',
                        ' - error {0}'.format(response.json()['error']['errorString'])
                    )
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('IdentityManagement', '103', response_string)

    def has_identity_app(self, app_name):
        """Checks if an identity app exits in the commcell

            Args:
                app_name    (str)   --  name of the identity app

            Returns:
                bool    -   boolean output whether the app exists in the commcell or not

            Raises:
                SDKException:
                    if type of the app name argument is not string
        """
        if not isinstance(app_name, str):
            raise SDKException('IdentityManagement', '102')

        return self._apps and app_name.lower() in self._apps

    def refresh(self, hard=False):
        """Refresh the apps associated with the Commcell.
        
            Args:
                hard    (bool)  --  perform a hard refresh of the cache
                
        """
        self._apps = self._get_apps(hard)
        self._local_app = None


class IdentityManagementApp(object):
    """Class for performing operations on a specific identity management app"""

    def __init__(self, commcell_object, app_name, app_dict=None):
        """Initialize the app class

            Args:
                commcell_object     (object)    --  instance of the commcell class

                app_name            (str)       --  name of the app

                app_dict            (dict)     -- dict containing the properties of the app. default: None

            Returns:
                object - instance of the IdentityManagementApp class
        """
        self._properties = app_dict
        self._commcell_object = commcell_object

        self._app_name = app_name
        self._app_type_dict = {
            1: 'Regular',
            2: 'SAML',
            3: 'CommCell',
            4: 'Local Identity',
            5: 'OpenId Connect'
        }
        self._app_displayname = None

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'IdentityManagementApp class instance for app: \
                                "{0}", of Commcell: "{1}"'

        return representation_string.format(
            self._app_name, self._commcell_object.commserv_name
        )

    def get_app_props(self):
        """Returns a dict containing the properties of a third party app.

            Returns:
                dict    -   properties of the identity app

            Raises:
                SDKException:
                    if response is not success
        """
        req_xml = """<App_GetClientThirdPartyAppPropReq propLevel='30'>
                        <appKeys val='{0}'/>
                    </App_GetClientThirdPartyAppPropReq>""".format(self.app_key)
        response = self._commcell_object._qoperation_execute(req_xml)
        if 'clientThirdPartyApps' in response:
            return response['clientThirdPartyApps'][0]['props']['nameValues']
        else:
            raise SDKException('IdentityManagement', '102')

    def refresh(self):
        """Refresh the properties of the app."""
        apps = self._commcell_object.identity_management
        apps.refresh()
        if self.app_type == 'Local Identity':
            self._properties = apps.get_local_identity_app.properties
        else:
            self._properties = apps.get(self.app_name).properties

    @property
    def properties(self):
        """Returns the properties of the app."""
        if self._properties is None:
            self.refresh()
        return self._properties

    @property
    def app_name(self):
        """Treats the app name as a read-only attribute."""
        return self._app_name

    @property
    def app_key(self):
        """Treats the app key as a read-only attribute."""
        return self.properties.get('appKey')

    @property
    def app_description(self):
        """Treats the app description as a read-only attribute."""
        return self.properties.get('appDescription')

    @property
    def app_type(self):
        """Treats the app type as a read-only attribute."""
        return self._app_type_dict.get(
            int(self.properties.get('appType', -1)), 
            'unknown app type'
        )

    @property
    def is_enabled(self):
        """Treats the enabled property as a read-only attribute."""
        return self.properties.get('isEnabled')

    @property
    def flags(self):
        """Treats the app flags as a read-only attribute."""
        return self.properties.get('flags')


class SamlApp(object):
    """Class for performing operations on a specific saml app"""

    def __init__(self, commcell, appname, properties=None):
        """Initialise SamlApp class
            Args:
                commcell            (object)        instance of commcell class

                appname             (string)        saml app name

                properties          (dict)          dict containing properties of saml app. Default: None

            Returns:
                object - instance of the SamlApp class
        """

        self._commcell = commcell
        self._cvpysdk_object = commcell._cvpysdk_object
        self._update_response_ = commcell._update_response_
        self._appname = appname
        self._properties = None
        self._SAML = commcell._services['EDIT_SAML']
        self._redirecturl = commcell._services['REDIRECT_LIST']
        self._APPS = commcell._services['IDENTITY_APPS']
        self._SAML_PROP = commcell._services['GET_SAML_PROP']

        if properties:
            self._properties = properties
        else:
            self.refresh()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'SamlApp class instance for app: \
                                "{0}", of Commcell: "{1}"'

        return representation_string.format(
            self._appname, self._commcell.commserv_name
        )

    def refresh(self):
        """Refresh the saml app properties"""
        self._properties = self._get_saml_app_details()

    def _get_saml_app_details(self):
        """gets the properties of a saml app
        Returns:
                        prop        (dict)      properties of a saml app

        Raises:
                SDK Exception:
                    if saml app is not found
                    if request is not successful
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._SAML % self._appname
        )
        if flag:
            if response.json() and 'name' in response.json():
                if response.json()['name'] == self._appname:
                    return response.json()
                else:
                    raise SDKException(
                        'IdentityManagement',
                        '102',
                        ' - error {0}'.format(response.json()['errorMessage'])
                    )
            else:
                raise SDKException('Response', '500' + 'Invalid Response Returned')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_all_saml_app_prop(self) -> dict:
        """Returns a dict containing the properties of SAML app.

            Returns:
                dict    -   properties of the saml app

            Raises:
                SDKException:
                    if response is not success
        """
        req_url = self._APPS+ '?appName=%s' % self._appname
        flag, response = self._cvpysdk_object.make_request('GET', req_url)
        if flag:
            if response.json() and 'clientThirdPartyApps' in response.json():
                return response.json()['clientThirdPartyApps'][0]
            else:
                raise SDKException(
                    'IdentityManagement',
                    '102',
                    ' - error {0}'.format(response.text)
                )
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)


    def modify_saml_app(self, req_body):
        """Modifies a saml app
            Args:
                req_body  (json)       saml app properties in json format

            Raises:
                SDKException:
                    if failed to modify saml app
                    if request is not successful

        """
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._SAML % self._appname, req_body
        )
        if flag:
            if response.json() and 'errorCode' in response.json():
                if response.json()['errorCode'] == 0:
                    self.refresh()
                else:
                    raise SDKException(
                        'IdentityManagement',
                        '105',
                        ' - error {0}'.format(response.json()['errorMessage'])
                    )
            else:
                raise SDKException('Response', '500' + 'Invalid Response Returned')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def set_auto_redirect_to_idp(self, enable:bool=True) -> None:
        """Enable/Disable auto redirection to IDP

        Args:
            enable (bool)   :   True to enable, False to disable

        Raises:
            SDKException:
                if request is not successful
        """
        # preserve the state of other flags
        flags = self.get_all_saml_app_prop()['flags']
        if enable:
            flags |= 1
        else:
            flags &= ~1

        req_json = {
                        "opType": 3,
                        "clientThirdPartyApps": [
                            {
                                "flags": flags,
                                "appType": 2,
                                "appKey": self._properties['appKey']
                            }
                        ]
                    }
        flag, response = self._cvpysdk_object.make_request('PUT', self._APPS, req_json)
        if flag:
            if response.json():
                error_code = response.json().get('errorCode', 0)
                if error_code != 0:
                    raise SDKException(
                        'Response', '101',
                        self._update_response_(response.text)
                    )
                return
            raise SDKException('Response', '102')
        raise SDKException(
            'Response', '101', self._update_response_(response.text))

    def get_saml_user_redirect_url(self, user_email):
        """Get Redirect Url of SAML User
        Args:
            user_email         (str)        user email

        Returns :
                redirect url of user, None if redirect url is not found for the user
        Raises:
                SDKException:
                    if failed to get redirect url
                    if request is not successful
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._redirecturl % user_email
        )
        if flag:
            if response.json():
                if 'AvailableRedirects' in response.json():
                    if len(response.json()['AvailableRedirects']) > 0:
                        return response.json()['AvailableRedirects'][0].get('redirectUrl')
                    else:
                        return None
                else:
                    raise SDKException(
                        'IdentityManagement',
                        '106',
                        ' - error {0}'.format(response.json()['error'])
                    )
            else:
                raise SDKException('Response', '500' + 'Invalid Response Returned')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def saml_app_description(self):
        """Treats the saml_app_description as a read-only attribute."""
        return self._properties.get('description')

    @property
    def is_saml_app_enabled(self):
        """Treats the is_saml_app_enabled as a read-only attribute."""
        return self._properties.get('enabled')

    @property
    def is_auto_create_user(self):
        """Treats the is_auto_create_user as a read-only attribute."""
        return self._properties.get('autoCreateUser')

    @property
    def saml_app_default_user_groups(self):
        """Treats the saml_app_default_user_groups as a read-only attribute."""
        return self._properties.get('userGroups')

    @property
    def saml_app_nameid_attribute(self):
        """Treats the saml_app_nameid_attribute as a read-only attribute."""
        return self._properties.get('nameIDAttribute')

    @property
    def saml_app_attribute_mappings(self):
        """Treats the saml_app_attribute_mappings as a read-only attribute."""
        return self._properties.get('attributeMappings')

    @property
    def saml_app_identity_provider_metadata(self):
        """Treats the saml_app_identity_provider_metadata as a read-only attribute."""
        return self._properties.get('identityProviderMetaData')

    @property
    def saml_app_service_provider_metadata(self):
        """Treats the saml_app_service_provider_metadata as a read-only attribute."""
        return self._properties.get('serviceProviderMetaData')

    @property
    def saml_app_associations(self):
        """Treats the saml_app_associations as a read-only attribute."""
        return self._properties.get('associations')

    @property
    def is_company_saml_app(self):
        """Treats the is_company_saml_app as a read-only attribute.
            Returns
                    True if saml app is created for a company, False otherwise
        """
        if self._properties.get('createdForCompany'):
            return True
        else:
            return False
