#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017 SIOS Technology Corp. All rights reserved.
##############################################################################
"""
This is an example of how to use the SDK to send events into SIOS iQ.
"""

import logging
from datetime import datetime
from pytz import timezone
from os.path import dirname, realpath
import sys

curr_path = dirname(realpath(__file__))
sys.path.insert(0, '{}/../../'.format(curr_path))

from SignaliQ.client import Client
from SignaliQ.model.CloudProviderEvent import CloudProviderEvent
from SignaliQ.model.CloudVM import CloudVM
from SignaliQ.model.NetworkInterface import NetworkInterface
from SignaliQ.model.ProviderEventsUpdateMessage import ProviderEventsUpdateMessage

__log__ = logging.getLogger(__name__)


def main(args):
    ##
    # IMPORTANT REQUIREMENTS FOR EVENTS
    # - The event's `environment_id` must match the ProviderEventsUpdateMessage's `environment_id`
    # - The VM must be within the given environment
    # - Event time has to be in ISO-8601 format with the timezone.
    ##

    ##
    # REQUIREMENTS FOR CORRELATING THIRD PARTY EVENTS
    # - Parent event must be in progress.
    # - Time of child events must be during the parent's duration time
    # - The child event's layer must match the parent's layer
    ##

    ##
    # Valid Time Formats:
    # - 2017-03-03T06:00:00.000Z       (time assumed to be in UTC)
    # - 2017-03-03T06:00:00.000        (time assumed to be in UTC)
    # - 2017-03-03T06:00:00.000-05:00  (timezone specified)
    # - 2017-03-03T06:00:00-05:00      (timezone specified)
    ##
    event_time = datetime(
        year = 2017, month = 11, day = 1, hour = 3, minute = 15, tzinfo = timezone('US/Eastern')
    ).strftime('%Y-%m-%dT%H:%M:%S%z')
    environment_id = 500  # name: Env 6.5 QA

    vms = [
        CloudVM(
            network_interfaces = [
                NetworkInterface(hw_address = "00:50:56:93:7a:b9"),
                NetworkInterface(hw_address = "00:50:56:9b:06:1c"),
            ],
        ),
        CloudVM(
            uuid = "421321c6-2d7a-0b73-942e-e539bda95775"
        ),
        CloudVM(
            network_interfaces = [
                NetworkInterface(hw_address = "00:50:56:9b:7c:a8"),
                NetworkInterface(hw_address = "00:50:56:9b:2f:a0"),
            ],
        ),
    ]

    child_events = [
        CloudProviderEvent(
            description = "Caused by phase of the moon.",
            environment_id = environment_id,
            event_type = "SDK Event",
            layer = "Compute",
            source = "Example.py",
            time = event_time,
            vms = vms,
        )
    ]

    event_message = ProviderEventsUpdateMessage(
        environment_id = environment_id,
        events = child_events,
    )

    # Setup the client and send the data!
    client = Client()

    __log__.info(
        "Creating event with time {} and env id of {}".format(event_time, environment_id)
    )

    client.connect()
    client.send(event_message)
    client.disconnect()


if __name__ == "__main__":
    main(sys.argv)
