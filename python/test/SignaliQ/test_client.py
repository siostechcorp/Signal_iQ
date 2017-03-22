#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017 SIOS Technology Corp. All rights reserved.
##############################################################################

import amqp
import arrow
import logging
import json
import unittest
try:
    from imp import reload
except ImportError as e:
    from importlib import reload

from SignaliQ import client
from SignaliQ.model.CloudProviderEvent import CloudProviderEvent
from SignaliQ.model.ProviderEventsUpdateMessage import ProviderEventsUpdateMessage

__log__ = logging.getLogger(__name__)


class TestClient(unittest.TestCase):

    def setUp(self):
        # Mockout the config function so do not have to read from disk
        def mock_build_config_from_file(self):
            return {
                "connection": {
                    "host": "hostname",
                },
                "credentials": {
                    "password": "my_password",
                    "user": "admin",
                },
                "logging": {
                    "date_format": "%m-%d-%Y %I:%M:%S.%f",
                    "level": "INFO",
                },
            }

        client.Client._build_config_from_file = mock_build_config_from_file
        self.client = client.Client()

    def test_build_message_body(self):
        sample_data = json.dumps({"a": 1, "b": 2})
        result = self.client._build_message_body(sample_data)
        self.assertIsInstance(result, amqp.Message)


    def test_serialize_models(self):
        events = [
            CloudProviderEvent(
                description = "Caused by phase of the moon.",
                environment_id = 253,
                layer = "storage",
                event_type = "Here",
                time = arrow.get("2017-01-02T03:04:05").to("US/Eastern").isoformat(),
                vm_uuids = ["42205c48-3065-9a39-a25b-f290f31bc0fc"],
            )
        ]
        event_message = ProviderEventsUpdateMessage(
            environment_id = 123,
            events = events,
        )

        result_serialize = self.client._serialize_models(event_message)
        self.assertIsInstance(result_serialize, dict)

        result_dumps = json.dumps(
            event_message,
            default = self.client._serialize_models
        )
        self.assertIsInstance(result_dumps, str)


class TestClientConstructor(unittest.TestCase):

    def setUp(self):
        reload(client)


    def test_build_config_from_file__not_exists(self):
        my_client = client.Client
        my_client._current_dir = "/current_dir/"

        with self.assertRaises(SystemExit) as exp:
            my_client()

        self.assertEqual(exp.exception.code, 1)


    __mock_config__ = {
        "connection": {
            "host": "hostname",
        },
        "credentials": {
            "password": "my_password",
            "user": "admin",
        },
        "logging": {
            "date_format": "%m-%d-%Y %I:%M:%S.%f",
            "level": "INFO",
        },
    }

    __mock_config_ini__ = (
        "[connection] \n"
        "host = no_such_host \n"
        "[credentials] \n"
        "password = change_this_value \n"
        "user = admin \n"
        "[logging] \n"
        "date_format = %m-%d-%Y %I:%M:%S.%f \n"
        "level = INFO \n"
    )


if __name__ == "__main__":
    unittest.main()
