#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017 SIOS Technology Corp. All rights reserved.
##############################################################################
"""
This script will spray events for various environments and VMs.
"""

import logging
import sys
from datetime import datetime, timedelta
from pytz import timezone
from os.path import dirname, realpath

curr_path = dirname(realpath(__file__))
sys.path.insert(0, '{}/../../'.format(curr_path))

from SignaliQ.client import Client
from SignaliQ.model.CloudProviderEvent import CloudProviderEvent
from SignaliQ.model.CloudVM import CloudVM
from SignaliQ.model.NetworkInterface import NetworkInterface
from SignaliQ.model.ProviderEventsUpdateMessage import ProviderEventsUpdateMessage

__log__ = logging.getLogger(__name__)


def main(args):
    # Setup the client and send the data!
    client = Client()
    client.connect()

    id_interf = {
        500: [
            "00:50:56:9b:3a:9b",
            "00:50:56:9b:51:f2",
            "00:50:56:9b:6f:09",
        ],
        505: [
            "00:50:56:93:7a:b9",
        ],
    }

    id_list = [id_interf for xx in range(5)]

    event_time = (
        datetime
        .now()
        .replace(tzinfo = timezone('US/Eastern'))
    )

    for idx in id_list:
        for env_id, hws in id_interf.items():

            event_time += timedelta(minutes = 5)

            __log__.info(
                "Creating event with time {} and env id of {}".format(
                    event_time.strftime('%Y-%m-%dT%H:%M:%S%z'), env_id,
                )
            )

            events = [
                CloudProviderEvent(
                    description = "Caused by a bad mood",
                    environment_id = env_id,
                    layer = "Storage",
                    severity = "Critical",
                    time = event_time.strftime('%Y-%m-%dT%H:%M:%S%z'),
                    event_type = "SDK Event",
                    vms = [
                        CloudVM(network_interfaces = [NetworkInterface(hw_address = hw)]) for hw in hws
                    ],
                )
            ]

            event_message = ProviderEventsUpdateMessage(
                environment_id = env_id,
                events = events,
            )

            client.send(event_message)

    # DONE
    client.disconnect()


if __name__ == "__main__":
    main(sys.argv)
