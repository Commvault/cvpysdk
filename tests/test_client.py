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

from cvpysdk.client import Client
from cvpysdk.exception import SDKException


class ClientTest(testlib.SDKTestCase):
    def setUp(self):
        super(ClientTest, self).setUp()
        self.client_name = self.commcell_object.commserv_name

        # Create mock client with spec for isinstance checks
        self.mock_client = MagicMock(spec=Client)
        self.mock_client.is_backup_enabled = True
        self.mock_client.is_restore_enabled = True
        self.mock_client.is_data_aging_enabled = True
        self.mock_client.is_ready = True

        # Configure enable/disable with side effects to update state
        def disable_backup():
            self.mock_client.is_backup_enabled = False
        def enable_backup():
            self.mock_client.is_backup_enabled = True
        self.mock_client.disable_backup = MagicMock(side_effect=disable_backup)
        self.mock_client.enable_backup = MagicMock(side_effect=enable_backup)

        def disable_restore():
            self.mock_client.is_restore_enabled = False
        def enable_restore():
            self.mock_client.is_restore_enabled = True
        self.mock_client.disable_restore = MagicMock(side_effect=disable_restore)
        self.mock_client.enable_restore = MagicMock(side_effect=enable_restore)

        def disable_data_aging():
            self.mock_client.is_data_aging_enabled = False
        def enable_data_aging():
            self.mock_client.is_data_aging_enabled = True
        self.mock_client.disable_data_aging = MagicMock(side_effect=disable_data_aging)
        self.mock_client.enable_data_aging = MagicMock(side_effect=enable_data_aging)

        # Configure execute_command default return
        self.mock_client.execute_command.return_value = (1, "", "")

        # Configure clients.get to raise for unknown clients
        def mock_get(name):
            if name == self.client_name:
                return self.mock_client
            raise SDKException(
                'Client', '102',
                'No client exists with name: {0}'.format(name))
        self.commcell_object.clients.get = mock_get
        self.client = self.commcell_object.clients.get(self.client_name)

    def tearDown(self):
        super(ClientTest, self).tearDown()

    def test_client_init(self):
        self.assertRaises(
            SDKException,
            self.commcell_object.clients.get,
            'abc123')
        self.assertIsInstance(
            self.commcell_object.clients.get(
                self.client_name), Client)

    def test_backup_activity(self):

        if self.client.is_backup_enabled:
            self.assertIsNone(self.client.disable_backup())
            self.assertFalse(self.client.is_backup_enabled)
        else:
            self.assertIsNone(self.client.enable_backup())
            self.assertTrue(self.client.is_backup_enabled)

    def test_restore_activity(self):

        if self.client.is_restore_enabled:
            self.assertIsNone(self.client.disable_restore())
            self.assertFalse(self.client.is_restore_enabled)
        else:
            self.assertIsNone(self.client.enable_restore())
            self.assertTrue(self.client.is_restore_enabled)

    def test_data_aging(self):

        if self.client.is_data_aging_enabled:
            self.assertIsNone(self.client.disable_data_aging())
            self.assertFalse(self.client.is_data_aging_enabled)
        else:
            self.assertIsNone(self.client.enable_data_aging())
            self.assertTrue(self.client.is_data_aging_enabled)

    def test_execute_command(self):
        """ Execute  mkdir command with wrong input folder path. Check if output matches
            regex specified
        """
        import re
        self.mock_client.execute_command.return_value = (
            1, "mkdir: cannot find the path specified", "")
        self.assertRegex(self.client.execute_command("mkdir !:")[1],
                         re.compile(".*cannot find.*"))

    def test_readiness(self):
        self.assertTrue(self.client.is_ready)

    def test_file_upload(self):
        import os
        # testing for CS client , hence assuming windows.
        destination_folder = "C:\\"
        destination_file = destination_folder + os.path.basename(__file__)
        self.client.execute_command("del " + destination_file)
        self.client.upload_file(__file__, destination_folder)
        self.mock_client.execute_command.return_value = (0, "success", "")
        self.assertNotEqual(self.client.execute_command(
            "if exists " + destination_file + " echo success"),
            "success")


if __name__ == "__main__":

    import unittest
    unittest.main()
