"""
Unit tests for client-server functionality
"""

import logging
import threading
import unittest

import clientserver
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestClientServer(unittest.TestCase):
    """The test"""
    _server = clientserver.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = clientserver.Client()  # create new client for each test

    def test_srv_get_existing_entry(self):  #schaut ob Hans da ist
        """Test GET for existing entry"""
        msg = self.client.call("GET Hans")
        self.assertEqual(msg, "Hans: 1234")
    def test_srv_get_existing_entry1(self):  #schaut ob Sabine da ist
        """Test GET for existing entry"""
        msg = self.client.call("GET Sabine")
        self.assertEqual(msg, "Sabine: 151617")

    def test_srv_get_non_existing_entry(self):  #schaut wa spassiert wen User not found
        """Test GET for non-existing entry"""
        msg = self.client.call("GET Unknown")
        self.assertEqual(msg, "Name not in telephonebook")

    def test_srv_invalid_command(self):
        """Test invalid command"""
        msg = self.client.call("INVALID")
        self.assertEqual(msg, "Command not found")

    def test_srv_get_all(self):
        """Test GETALL"""
        msg = self.client.call("GETALL")
        self.assertEqual(msg, "Hans: 1234\nPeter: 5678\nPaul: 91011\nMax: 121314\nSabine: 151617\n")

    # def test_srv_get_all_empty(self):         #setzt das Telefonbuch auf leer - Testreihenfolge nicht immer konstant - deswegen nicht mitausführen stört die anderen Tests
    #     """Test GETALL with 0 entries"""
    #     clientserver.telephonebook = {}
    #     msg = self.client.call("GETALL")
    #     self.assertEqual(msg, "Telephonebook is empty")

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate


if name == 'main':
    unittest.main()