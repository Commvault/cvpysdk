#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Cloud Apps Subclient.

CloudAppsSubclient is the only class defined in this file.

CloudAppsSubclient: Derived class from Subclient Base class, representing a
                        cloud apps subclient, and to perform operations on that subclient

CloudAppsSubclient:
    _get_subclient_content_()   --  gets the content of a cloud apps subclient

    _set_subclient_content_()   --  sets the content of a cloud apps subclient

"""

from ..exception import SDKException
from ..subclient import Subclient


class CloudAppsSubclient(Subclient):
    """Derived class from Subclient Base class, representing a CloudApps subclient,
        and to perform operations on that subclient."""

    def _get_subclient_content_(self, subclient_properties):
        """Gets the appropriate content from the Subclient relevant to the user.

            Args:
                subclient_properties (dict)  --  dictionary contatining the properties of subclient

            Returns:
                list - list of content associated with the subclient
        """
        content = []

        for account in subclient_properties['content']:
            temp_account = account["cloudconnectorContent"]["includeAccounts"]

            content_dict = {
                'SMTPAddress': temp_account["contentName"],
                'display_name': temp_account["contentValue"]
            }

            content.append(content_dict)

        return content

    def _set_subclient_content_(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            Cloud Apps Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []

        try:
            for account in subclient_content:
                temp_content_dict = {
                    "cloudconnectorContent": {
                        "includeAccounts": {
                            "contentValue": account['display_name'],
                            "contentType": 134,
                            "contentName": account['SMTPAddress']
                        }
                    }
                }

                content.append(temp_content_dict)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        return content
