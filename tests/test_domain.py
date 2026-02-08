#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import testlib


try:
    import unittest2 as unittest
except ImportError:
    import unittest

from unittest.mock import MagicMock

from cvpysdk.exception import SDKException


class DomainTest(testlib.SDKTestCase):
    def setUp(self):
        super(DomainTest, self).setUp()
        self.client_name = self.commcell_object.commserv_name
        self.client = MagicMock()

        # Track domain state for mock operations
        self._mock_domains = {}

        def mock_get(name):
            if name in self._mock_domains:
                return self._mock_domains[name]
            raise SDKException(
                'Domain', '102',
                "Domain {0} doesn't exists on this commcell.".format(name))

        def mock_add(name, netbios, user, password, proxy_list):
            self._mock_domains[name] = {
                "shortName": {"domainName": name}
            }

        def mock_delete(name):
            if name in self._mock_domains:
                del self._mock_domains[name]
            else:
                raise SDKException(
                    'Domain', '102',
                    'No domain exists with name: {0}'.format(name))

        self.commcell_object.domains.get = mock_get
        self.commcell_object.domains.add = mock_add
        self.commcell_object.domains.delete = mock_delete

    def tearDown(self):
        super(DomainTest, self).tearDown()

    def test_add_domian(self):

        self.assertRaises(
            SDKException,
            self.commcell_object.domains.get,
            'abc123')
        self.commcell_object.domains.add(
            "automation_pyunittest",
            "automation", "automation\\administrator",
            self.data['password1'] ,
            ["magic_test"]
            )
        self.assertEqual(
            u"automation_pyunittest",
            self.commcell_object.domains.get("automation_pyunittest")["shortName"]["domainName"]
            )
        self.commcell_object.domains.delete("automation_pyunittest")
        self.assertRaises(
            SDKException,
            self.commcell_object.domains.get,
            'automation_pyunittest')


if __name__ == "__main__":

    import unittest
    unittest.main()
