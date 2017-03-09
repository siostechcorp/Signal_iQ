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

from SignaliQ.client import Client
from SignaliQ.model.CloudProviderEvent import CloudProviderEvent
from SignaliQ.model.ProviderEventsUpdateMessage import ProviderEventsUpdateMessage

__log__ = logging.getLogger(__name__)


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client()


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


if __name__ == "__main__":
    unittest.main()
