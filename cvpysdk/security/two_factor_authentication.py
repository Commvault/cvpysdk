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

"""Helper file to manage two factor authentication settings on this commcell

TwoFactorAuthentication is the only class defined in this file

TwoFactorAuthentication:

    __init__()      --      Initializes TwoFactorAuthentication class object.

    refresh()       --      fetches the current tfa settings.

    _get_tfa_info() --      Excutes get api on the server to fetch tfa info.

    _process_response()   --  Process the response json

    disable_tfa()   --      Disables tfa at commcell or organizaton level

    enable_tfa()    --      Enables tfa at commcell or organization level

TwoFactorAuthentication Instance Attributes
===========================================

    **is_tfa_enabled**      --      returns tfa status True or False

    **tfa_enabled_user_groups** --  returns user groups on which tfa is enabled.
                                    only if user group level tfa is enabled
"""

from typing import Union, Optional, List, Dict, Any

from ..exception import SDKException


class TwoFactorAuthentication:
    """Class for managing the security associations roles on the commcell

    Attributes:
        _commcell (Commcell): Commcell class object.
        _tfa_status (bool): Two factor authentication status.
        _tfa_enabled_user_groups (list): User groups on which tfa is enabled.
        _org_id (int): Organization ID.
        _cvpysdk_object (object): CVPySDK object.
        _services (dict): Dictionary of services.
        _update_response_ (method): Method to update response.

    Usage:
        >>> from commvault import Commcell
        >>> commcell = Commcell('hostname', 'user', 'password')
        >>> tfa = TwoFactorAuthentication(commcell)
    """

    def __init__(self, commcell_object: object, organization_id: Optional[Union[int, str]] = None) -> None:
        """
        Initializes TwoFactorAuthentication class object

        Args:
            commcell_object (object): commcell class object.
            organization_id (Union[int, str], optional): id of the organization on which two factor authentication
                                        operations to be performed. Defaults to None.

        Raises:
            SDKException:
                if invalid args are sent.

        Usage:
            >>> tfa = TwoFactorAuthentication(commcell_object)
            >>> tfa = TwoFactorAuthentication(commcell_object, organization_id=123)
        """
        self._commcell = commcell_object
        self._tfa_status = None
        self._tfa_enabled_user_groups = None
        self._org_id = None
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        if organization_id:
            if isinstance(organization_id, (int, str)):
                self._org_id = organization_id
            else:
                raise SDKException('Security', '101')
        self.refresh()

    def refresh(self) -> None:
        """
        Refresh the properties of two factor authentication

        Returns:
            None

        Usage:
            >>> tfa.refresh()
        """
        self._get_tfa_info()

    def _get_tfa_info(self) -> None:
        """
        Executes api on the server and fetches commcell/organization two factor authentication info.

        Returns:
            None

        Raises:
            SDKException:
                if failed to fetch details
                if response is emmpty
                if response is not success

        Usage:
            >>> tfa._get_tfa_info()
        """
        url = self._services['TFA']

        if self._org_id:
            url = self._services['ORG_TFA'] % self._org_id

        flag, response = self._cvpysdk_object.make_request(
            'GET', url
        )

        if flag:
            if response.json() and 'twoFactorAuthenticationInfo' in response.json():
                info = response.json().get('twoFactorAuthenticationInfo')

                if 'error' in response.json() and 'errorCode' in response.json().get('error'):
                    if response.json().get('error').get('errorCode') != 0:
                        error_msg = response.json().get('error').get('errorCode').get('errorString')
                        raise SDKException('Security',
                                           '102',
                                           'Failed to get the tfa info. \nError {0}'.format(error_msg))

                if 'mode' in info:
                    if info.get('mode') == 0:
                        self._tfa_status, self._tfa_enabled_user_groups = False, []
                    if info.get('mode') in (1, 2):
                        self._tfa_status, self._tfa_enabled_user_groups = True, info.get('userGroups', [])
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _process_response(self, flag: int, response: Any) -> None:
        """
        Processes the flag and response json

        Args:
            flag     (int):   status of api execution
            response (byte): data received from server

        Raises:
            SDKException:
                if failed to get required info

        Usage:
            >>> tfa._process_response(flag, response)
        """
        if flag:
            if response.json():
                response_json = {}
                if 'response' in response.json():
                    response_json = response.json()['response'][0]
                if 'error' in response.json():
                    response_json = response.json().get('error')
                if response_json.get('errorCode') != 0:
                    error_msg = response_json.get('errorString')
                    raise SDKException('Security',
                                       '102',
                                       'Failed to get the two factor authentication info.'
                                       ' \nError {0}'.format(error_msg))
                self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable_tfa(self, otp: str = None) -> None:
        """
         Disables two factor authentication at commcell/organization level
        Args:
            otp (str): otp for two-factor authentication operation.
         Returns:
             None

        Raises:
            SDKException:
                if failed to disable tfa.

        Usage:
            >>> tfa.disable_tfa()
        """
        url = self._services['TFA_DISABLE']
        if self._org_id:
            url = self._services['ORG_TFA_DISABLE'] % self._org_id
        headers = None
        if otp:
            headers = self._commcell._headers.copy()
            headers["otp"] = otp

        flag, response = self._cvpysdk_object.make_request(
            'PUT', url, headers=headers
        )
        self._process_response(flag=flag, response=response)

    def enable_tfa(self, user_groups: Optional[list] = None, usernameless: bool = False, passwordless: bool = False,
                   otp: str = None) -> None:
        """
        Enables two factor authentication at commcell/organization level.

        Args:
            user_groups  (list, optional):  user group names on which two factor authentication needs to be enabled. Defaults to None.
            usernameless (bool, optional):  allow usernameless login if True. Defaults to False.
            passwordless (bool, optional):  allow passwordless login if True. Defaults to False.
            otp (str): otp for two-factor authentication operation.

        Returns:
            None

        Raises:
            SDKException:
                if failed to enable tfa.

        Usage:
            >>> tfa.enable_tfa()
            >>> tfa.enable_tfa(user_groups=['group1', 'group2'])
            >>> tfa.enable_tfa(usernameless=True, passwordless=True)
        """
        url = self._services['TFA_ENABLE']

        if self._org_id:
            url = self._services['ORG_TFA_ENABLE'] % self._org_id

        user_groups_list = []
        if user_groups:
            if isinstance(user_groups, list):
                for group in user_groups:
                    group_obj = self._commcell.user_groups.get(user_group_name=group)
                    user_groups_list.append({"userGroupName": group_obj.name})
            else:
                raise SDKException('Security', '101')

        payload = {
            "twoFactorAuthenticationInfo": {
                "mode": 2 if user_groups_list else 1,
                "userGroups": user_groups_list,
                'webAuthn': {
                    'allowPasswordlessLogin': passwordless,
                    'allowUsernamelessLogin': usernameless
                }
            }
        }

        if not self._org_id:
            payload = {
                "commCellInfo": {
                    "generalInfo": payload
                }
            }

        headers = None
        if otp:
            headers = self._commcell._headers.copy()
            headers["otp"] = otp

        flag, response = self._cvpysdk_object.make_request(
            'PUT', url, payload, headers=headers
        )
        self._process_response(flag=flag, response=response)

    @property
    def is_tfa_enabled(self) -> bool:
        """Returns status of two factor authentication(True/False)

        Returns:
            bool: True if tfa is enabled, False otherwise.

        Usage:
            >>> tfa.is_tfa_enabled
        """
        return self._tfa_status

    @property
    def tfa_enabled_user_groups(self) -> list:
        """
        Returns list of user group names for which two factor authentication is enabled
            eg:-
            [
                {
                "userGroupId": 1,
                "userGroupName": "dummy"
                }
            ]

        Returns:
            list: List of user group names.

        Usage:
            >>> tfa.tfa_enabled_user_groups
        """
        return self._tfa_enabled_user_groups
