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
    event_time = datetime(year = 2017, month = 3, day = 3, hour = 6, minute = 0, tzinfo = timezone('US/Eastern'))

    child_events = [
        CloudProviderEvent(
            description = "Caused by phase of the moon.",
            environment_id = 250,
            event_type = "SDK Event",
            layer = "Compute",
            time = event_time.strftime('%Y-%m-%dT%H:%M:%S%z'),
            vm_uuids = ["421bac04-f3d7-a600-ef5c-b3219e90d1eb"],
        )
    ]

    event_message = ProviderEventsUpdateMessage(
        environment_id = 250,
        events = child_events,
    )

    # Setup the client and send the data!
    client = Client()
    client.connect()
    client.send(event_message)
    client.disconnect()


if __name__ == "__main__":
    main(sys.argv)
