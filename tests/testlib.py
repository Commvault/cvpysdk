#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Shared unit test utilities."""
import json
import os
import time

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from cvpysdk import commcell
from time import sleep
from datetime import datetime, timedelta

import logging
logging.basicConfig(
    filename='unit_test.log',
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s")


class SDKTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('input.json', 'r') as data_file:
            cls.data = json.load(data_file)

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.test_json()
        self.commcell_object = commcell.Commcell(**self.data['commcell'])

    def tearDown(self):
        self.commcell_object.logout()

    def test_json(self):
        self.assertIsInstance(self.data, dict)
        self.assertIsInstance(self.data['commcell'], dict)
        self.assertIn('webconsole_hostname', self.data['commcell'].keys())
        self.assertIn('commcell_username', self.data['commcell'].keys())
        self.assertIn('commcell_password', self.data['commcell'].keys())
        self.assertNotIn("", self.data['commcell'].values())


if __name__ == "__main__":
    import unittest
    unittest.main()
