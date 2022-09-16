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


class Certificate:
    """Class for performing certificate related operations"""

    def __init__(self, commcell):
        """
        Initialize the Certificate class object

        Args: 
            commcell: Commcell object
        """

        self.commcell = commcell
        self.url = commcell._services["CERTIFICATES"]

    def _make_request(self, body={}):
        """
        Make a certificate API request

        Args:
            body (dict): Body to pass in post request

        Return: 
            Response of the request

        Example:
            _make_request({})
        """
        success, resp = self.commcell._cvpysdk_object.make_request("POST", self.url, body)
        resp_data = resp.json()
        if resp.status_code != 200:
            raise Exception(f"APIException: Response code {resp.status_code}.\n{resp_data}")
        else:
            return resp_data

    def revoke(self, cert_ids):
        """
        Revoke the certificate by certificate id

        Args:
            cert_ids (List[int]): List of certificate id's

        Return: 
            bool: if request processed successfully

        Example:
            revoke([1, 2, 3])
        """
        data = {
            "operation": 3,
            "certificateInfo": {
                "certificates": [

                ]
            }
        }
        if type(cert_ids) == list:
            for id in cert_ids:
                data["certificateInfo"]["certificates"].append(
                    {"id": int(id)}
                )
        elif type(cert_ids) == int or type(cert_ids) == str:
            data["certificateInfo"]["certificates"].append(
                {"id": int(cert_ids)}
            )
        else:
            raise Exception("cert_ids should be of type list or int")
        resp_data = self._make_request(data)
        return True

    def renew(self, cert_ids):
        """
        Renew the certificate by certificate id

        Args:
            cert_ids (List[int]): List of certificate id's

        Return: 
            bool: if request processed successfully

        Example:
            renew([1, 2, 3])
        """
        data = {
            "operation": 2,
            "certificateInfo": {
                "certificates": [

                ]
            }
        }
        if type(cert_ids) == list:
            for id in cert_ids:
                data["certificateInfo"]["certificates"].append(
                    {"id": int(id)}
                )
        elif type(cert_ids) == int or type(cert_ids) == str:
            data["certificateInfo"]["certificates"].append(
                {"id": int(cert_ids)}
            )
        else:
            raise Exception("cert_ids should be of type list or int")
        resp_data = self._make_request(data)
        return True

    def force_client_authentication(self, operation):
        """
        Enable of disable the lockdown mode

        Args:
            operation (bool): Turn ON/OFF the lockdown mode. 

        Return: 
            bool: if request processed successfully

        Example:
            force_client_authentication(True)
            force_client_authentication(False)
        """
        body = {
            "operation": 0,
            "certificateInfo": {

                "forceClientAuth": operation

            }
        }
        try :
            resp_data = self._make_request(body)
            return True
        except Exception as e:
            raise Exception(str(e))

    def make_temp_certificate(self, client_id):
        """
        Create temporary certificate of client

        Args:
            client_id (int): Client Id to generate certificate.

        Return: 
            str: Temp certificate for the client.

        Example:
            make_temp_certificate(5)
        """
        body = {
            "operation": 4,
            "makeTempCertClientID": client_id
        }
        resp_data = self._make_request(body)
        return resp_data["certificateInfo"]["tempCertificateInfo"]

    def client_certificate_rotation(self, months):
        """
        Modify certificate rotation period.

        Args:
            months (int): Number of months.

        Return: 
            bool: if request processed successfully

        Example:
            client_certificate_rotation(12)
        """
        body = {
            "operation": 0,
            "certificateInfo": {
                "ClientCertificateRotation": int(months)
            }
        }
        try:
            resp_data = self._make_request(body)
            return True
        except Exception as e:
            raise Exception(str(e))

    def ca_certificate_rotation(self, years):
        """
        Modify certificate rotation period.

        Args:
            years (int): Number of years.

        Return: 
            bool: if request processed successfully

        Example:
            ca_certificate_rotation(1)
        """
        body = {
            "operation": 0,
            "certificateInfo": {
                "CACertificateRotation": int(years)
            }
        }
        try:
            resp_data = self._make_request(body)
            return True
        except Exception as e:
            raise Exception(str(e))
