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

"""Main file for performing Metallic Integration steps with existing commcell .

This file has all the classes related to Metallic Integration Operations.

Metallic:      Class for representing all the metallic integration steps

Metallic:

    __init__(commcell_object)       --  initialize the Metallic class
                                            instance for the commcell

    _metallic_commcell_object()     --  returns the metallic commcell object

    metallic_subscribe()            --  linking on metallic side

    _cv_metallic_subscribe()        --  linking on commvault side

    is_metallic_registered()        --  returns boolean value
                                            true - if metallic is subscribed for a user
                                            false - if metallic is not subscribed for a user

    metallic_completed_solutions()        --  returns all the completed solutions on linked company of metalic

    metallic_unsubscribe()          --  unlinking on metallic side

    _cv_metallic_unsubscibe()       --  unlinking on commvault side

    _get_eligible_metallic_commcells()     --  gets the eligible metallic commcells for the logged in user


Metallic instance Attributes:

    **cloudservices_details**       --  returns cloudServices details if metallic service is registered in
                                        onprem/ MSP commcell

    **cloud_hostname**              --  returns cloud commcell hostname

"""

from .exception import SDKException
from .organization import Organization
from .security.user import User


class Metallic(object):
    """Class for representing Metallic related operations."""

    def __init__(self, commcell_object):
        """Intializes object of the Metallic class.

            Args:
                commcell_object (object) -instance of the commcell class

            Returns:
                object - instance of the Metallic class
        """

        self._commcell_object = commcell_object
        self._update_response_ = self._commcell_object._update_response_
        self._metallic_details = None
        self._metallic_web_url = None
        self._metallic_obj = None
        self._cloudservices_details = {}

    def _metallic_commcell_object(self, cloud_webconsole_hostname, cloud_username, cloud_password):
        """Gets the metallic commcell object.

            Args:
                cloud_webconsole_hostname (str) -- hostname of the cloud
                cloud_username (str) -- username of the cloud
                cloud_password (str) -- password of the cloud

            Raises:
                SDKException:

                    if inputs are not valid

                    if failed to create the object

                    if response is empty

                    if response is not success

        """
        if not (isinstance(cloud_webconsole_hostname, str) and
                isinstance(cloud_username, str) and
                isinstance(cloud_password, str)):
            raise SDKException('Metallic', '101')
        from cvpysdk.commcell import Commcell
        metallic_cell = self._get_eligible_metallic_commcells(cloud_username, cloud_webconsole_hostname)
        if (len(metallic_cell)) > 0:
            cloud_webconsole_hostname = metallic_cell[0]
        self._metallic_obj = Commcell(cloud_webconsole_hostname, cloud_username, cloud_password)

    def metallic_subscribe(self, cloud_webconsole_hostname, cloud_username, cloud_password, msp_company_name=None):
        """Adds a new Monitoring Policy to the Commcell.

            Args:
                cloud_webconsole_hostname (str) -- hostname of the cloud
                cloud_username (str) -- username of the cloud
                cloud_password (str) -- password of the cloud
                msp_company_name (str or object) -- name of the company or company object
                    default: None

            Raises:
                SDKException:
                    if metallic is already subscribed

                    if inputs are not valid

                    if failed to subscribe to metallic

                    if response is empty

                    if response is not success


        """
        if not (isinstance(cloud_webconsole_hostname, str) and
                isinstance(cloud_username, str) and
                isinstance(cloud_password, str)):
            raise SDKException('Metallic', '101')
        if msp_company_name and not (isinstance(msp_company_name, str)):
            raise SDKException('Metallic', '101')
        self._metallic_commcell_object(cloud_webconsole_hostname, cloud_username, cloud_password)
        if msp_company_name and not isinstance(msp_company_name, Organization):
            msp_company_name = msp_company_name.lower()
            msp_company_obj = self._commcell_object.organizations.get(msp_company_name)
        request = {
            "thirdpartyAppReq": {
                "opType": 1,
                "clientThirdPartyApps": [
                    {
                        "isCloudApp": False,
                        "appName": self._commcell_object.commserv_guid,
                        "appDisplayName": self._commcell_object.commserv_name,
                        "flags": 0,
                        "isCloudServiceSubscription": True,
                        "appType": 3,
                        "isEnabled": True,
                        "props": {
                            "nameValues": [
                                {
                                    "name": "RedirectUrl",
                                    "value": self._commcell_object.commserv_metadata['commserv_redirect_url']
                                },
                                {
                                    "name": "SP Certificate Data",
                                    "value": self._commcell_object.commserv_metadata['commserv_certificate']
                                },
                                {
                                    "name": "CommcellId",
                                    "value": str(self._commcell_object.commcell_id)
                                },
                                {
                                    "name": "Enable Sso Redirect",
                                    "value": "1"
                                }
                            ]
                        }
                    }
                ]
            }
        }

        if msp_company_name:
            test_dict = {
                'subscriberCompany': {
                    'GUID': self._commcell_object.organizations.all_organizations_props[msp_company_name]['GUID'],
                    'providerDomainName': msp_company_obj.organization_name
                }
            }
            request.update(test_dict)

        flag, response = self._metallic_obj._cvpysdk_object.make_request(
            'POST', self._metallic_obj._services['METALLIC_LINKING'], request)

        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']
                self._metallic_details = {}
                if (error_code == 2 or error_code == 0) and 'cloudServiceDetails' in response.json():
                    self._metallic_details = response.json()['cloudServiceDetails']
                if error_code < 0:
                    error_string = response.json()['errorMessage']
                    raise SDKException(
                        'Metallic',
                        '102',
                        'Failed to create TPA\nError: "{0}"'.format(
                            error_string
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        if msp_company_name:
            self._cv_metallic_subscribe(msp_company_name)
        else:
            self._cv_metallic_subscribe()

    def _cv_metallic_subscribe(self, msp_company_name=None):
        """Subscribing on on-prim or msp side.

            Args:
                msp_company_name (str) -- name of the company or company object
                    default: None

            Raises:
                SDKException:

                    if inputs are not valid

                    if failed to subscribe on on-prim or msp side

                    if response is empty

                    if response is not success


        """
        if msp_company_name and not (isinstance(msp_company_name, str)):
            raise SDKException('Metallic', '101')
        if msp_company_name and not isinstance(msp_company_name, Organization):
            msp_company_obj = self._commcell_object.organizations.get(msp_company_name)
        request = {
            "opType": 3,
            "cloudServiceDetails": self._metallic_details
        }

        if msp_company_name:
            request['subscriberCompany'] = {'providerId': int(msp_company_obj.organization_id)}

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['CV_METALLIC_LINKING'], request)

        if flag:
            if response and response.json():
                error_code = response.json().get('error', {}).get('errorCode')
                if error_code != 0:
                    error_string = response.json()['error']['errorString']
                    raise SDKException(
                        'Metallic',
                        '102',
                        'Failed to update linking details on onprim/msp: "{0}"'.format(
                            error_string
                        )
                    )
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def is_metallic_registered(self):
        """This function says whether metallic is registered for a user or not.

            Args:
                username (str) -- name of the user to which we need to check if metallic is registered

            Returns:
                Boolean --  True if metallic is returned in response
                            False if metallic is not returned in response

            Raises:
                SDKException:

                    if response is empty

                    if response is not success


        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._commcell_object._services['METALLIC_REGISTERED']
        )

        if flag:
            if response.json():
                if 'cloudServices' in response.json():
                    if response.json().get('cloudServices', [])[0].get('cloudService', {}).get('redirectUrl', {}):
                        self._metallic_web_url = \
                            response.json().get('cloudServices', [])[0].get('cloudService', {}).get('redirectUrl', {})
                        self._cloudservices_details = response.json()
                        return True
                return False
            else:
                return False
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def metallic_completed_solutions(self):
        """This function returns the completed solutions for metallic.

            Returns:
                dict of completed solutions

            Raises:
                SDKException:

                    if response is empty

                    if response is not success


        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._commcell_object._services['METALLIC_COMPLETED_SETUPS']
        )

        if flag:
            if response.json() and 'completedSetupsDetails' in response.json():
                completed_solns = response.json()['completedSetupsDetails'][0]['completedSetups']
                return completed_solns
            else:
                raise SDKException('Metallic', '102', 'No metallic solutions are configured')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def metallic_unsubscribe(self):
        """This function is for unsubscribing metallic

            Raises:
                SDKException:

                    if failed to unsubcribe on metallic

                    if response is empty

                    if response is not success


        """
        saml_token_for_user = self._commcell_object.get_saml_token()
        user_obj = User(self._commcell_object, self._commcell_object.commcell_username)
        company_name = user_obj.user_company_name
        if company_name == 'commcell':
            company_name = None
        request = {
            "cloudServiceDetails": {
                "cloudService": {
                    "redirectUrl": self._metallic_web_url if self.is_metallic_registered() else None,
                    "appName": self._commcell_object.commserv_guid
                }
            }
        }

        if company_name:
            test_dict = {
                'subscriberCompany': {
                    'GUID': self._commcell_object.organizations.all_organizations_props[company_name]['GUID'],
                    'providerId': self._commcell_object.organizations.all_organizations[company_name],
                    'providerDomainName': company_name
                }
            }
            request.update(test_dict)

        url1 = self._metallic_web_url + "/api/CloudService/Unsubscribe"
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            method='POST',
            url=url1,
            payload=request,
            headers={'Authtoken': saml_token_for_user,
                     'Accept': 'application/json'}
        )

        if flag:
            if response.json() and 'cloudServiceDetails' in response.json():
                error_code = response.json()['error']['errorCode']
                error_message = response.json()['error']['errorString']
                if not error_code == 0:
                    raise SDKException('Metallic', '102', error_message)
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self._cv_metallic_unsubscribe(user_obj)

    def _cv_metallic_unsubscribe(self, user):
        """This function says whether metallic is registered for a user or not.

            Args:
                user (str or object) -- username or user object who has rights to unsubscribe on on-prim or msp side

            Returns:
                Boolean --  True if metallic is returned in response
                            False if metallic is not returned in response

            Raises:
                SDKException:

                    if failed to unsubscribe on on-prim or msp side

                    if response is empty

                    if response is not success


        """

        if not isinstance(user, User):
            user = self._commcell_object.users.get(self._commcell_object.commcell_username)
        company_name = user.user_company_name
        if company_name == 'commcell':
            company_name = None
        request = {
            "opType": 4,
            "cloudServiceDetails": {
                "cloudService": {
                    "redirectUrl": self._metallic_web_url if self.is_metallic_registered() else None
                }
            }
        }

        if company_name:
            request['subscriberCompany'] = \
                {'providerId': self._commcell_object.organizations.all_organizations[company_name]}

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['CV_METALLIC_LINKING'], request)

        if flag:
            if response.json():
                error_code = response.json().get('error', {}).get('errorCode')
                error_message = response.json().get('error', {}).get('errorString')
                if not error_code == 0:
                    raise SDKException('Metallic', '102', error_message)
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_eligible_metallic_commcells(self, login_name_or_email=None, cloud_webconsole_hostname=None):
        """
        Gets the redirect metallic commcells based on login_name or email provided

        Args:

            login_name_or_email      (str)   -- Login name or email of the user

                default: current logged in user

            cloud_webconsole_hostname (str) -- cloud webconsole hostname

                default: None

        Raises:

            if the response is empty
            if there is no response

        Returns:

            list_of_metallic_commcells   (list)  -- list of metallic commcells

        """

        login_name_or_email = login_name_or_email.lower()
        url1 = r'http://{0}/webconsole/api/CloudService/Routing?username={1}'.format(
            cloud_webconsole_hostname, login_name_or_email)
        flag, response = self._commcell_object._cvpysdk_object.make_request(method='GET', url=url1)
        if flag:
            if response.json() and 'cloudServiceCommcells' in response.json():
                cloud_commcell_list = []
                for ser_comm in response.json()['cloudServiceCommcells']:
                    cloud_commcell_list.append(ser_comm['url'])
                return cloud_commcell_list
            else:
                return []
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def cloud_hostname(self):
        """ Returns cloudhostname"""
        return self._cloud_hostname

    @cloud_hostname.setter
    def cloud_hostname(self, value):
        """ Sets cloud hostname """
        self._cloud_hostname = value

    @property
    def cloudservices_details(self):
        """
        Get cloudServices details if metallic service is registered in onprem/ MSP commcell

        Returns:
             cloudservices_details (dict) --
                {
                'cloudServices':
                    [
                        {
                        'associatedCompany':
                            {
                                'companyAlias': ' ',
                                'GUID': ' '
                            },
                        'cloudService':
                            {
                                'redirectUrl': ' ',
                                'commcellName': ' '
                            }
                        }
                    ]
                }

        """
        if self._cloudservices_details is None:
            self._commserv_metadata = self.is_metallic_registered()

        return self._cloudservices_details
