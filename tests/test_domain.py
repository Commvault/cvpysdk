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

from cvpysdk.client import Client
from cvpysdk.exception import SDKException


class DomainTest(testlib.SDKTestCase):
    def setUp(self):
        super(DomainTest, self).setUp()
        self.client_name = self.commcell_object.commserv_name
        self.client = self.commcell_object.clients.get(self.client_name)

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
