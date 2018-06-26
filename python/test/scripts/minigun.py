#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017-2018 SIOS Technology Corp. All rights reserved.
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
from SignaliQ.model.ProviderEventsUpdateMessage import ProviderEventsUpdateMessage

__log__ = logging.getLogger(__name__)


def main(args):
    # Setup the client and send the data!
    client = Client()
    client.connect()

    id_uuids = {
        252: [
            "4220f3d7-53f4-13c4-9917-8ccd13dcd741",
            "4213314a-b4fe-839c-2396-a08b12e25913",
            "4220a81d-4228-b5f4-3f1e-bf976db50f85",
            "42131eb6-827d-0c33-661c-ef64cb273b28",
            "4220e75e-14b1-c93f-41e9-9d1fd07144ed",
            "42138816-5c3e-ef95-9c19-46c9fa7f21cd",
            "42206db2-4df2-91de-bc66-cbf340285ff0",
            "42130bef-a2ed-c840-c7f3-ad76dc6c49e6",
            "4220634b-541d-5d25-9f78-0beca0ab69ed",
        ],
        253: [
            "42115faf-27f2-58ac-390c-cc812b7f57d4",
            "4211025b-1d52-6a69-be62-ff54453f1df3",
            "4211c152-b452-52c3-2f81-b66b136bca5c",
            "42110065-c258-79ef-76a8-48e6cfad4fe6",
            "4211d091-e5e3-eb0f-0bf1-d9f33118c082",
        ],
        254: [
            "4220660c-b4bc-e791-4a8b-66a26b4deec3",
            "4220f56d-814a-5ff7-748f-d86c06b9c14a",
            "42207d24-4fca-81ac-aac1-aa4345c06180",
            "42205c48-3065-9a39-a25b-f290f31bc0fc",
            "420b7a83-6668-76f3-d5b8-aa0795d9c033",
            "420bf73e-aab5-043b-f616-35973af20948",
            "420b0dea-83e4-bab7-a287-e8a84a553cac",
            "42202fd8-b5cd-3f32-1d79-2c925579072a",
            "420bcea4-b6e0-1a7c-5c47-e1be30bb2b5b",
            "420bc56b-8124-b33e-f30c-a84ea6e36246",
            "4220ddaf-e2ef-e38d-a017-f47c2563c2cf",
            "420b1a5f-71e1-3ed7-304b-6413e5f836be",
            "420b53bb-08ab-d790-a4a1-6acbc251f682",
            "42209223-89b9-30c8-e009-572d39b136f7",
            "420bd42a-7090-5ec4-68e5-3b7c9d4181cf",
            "420b3280-04df-f00d-c044-344421b774df",
            "4220f252-5732-df84-ec9e-0cacf48070af",
        ],
    }

    id_list = [id_uuids for xx in range(5)]

    event_time = (
        datetime
        .now()
        .replace(tzinfo = timezone('US/Eastern'))
        .strftime('%Y-%m-%dT%H:%M:%S%z')
    )

    for idx in id_list:
        for env_id, uuids in id_uuids.items():
            event_time += timedelta(minutes = 5)
            events = [
                CloudProviderEvent(
                    description = "Caused by a bad mood",
                    environment_id = env_id,
                    layer = "Storage",
                    severity = "Critical",
                    time = event_time,
                    event_type = "SDK Event",
                    vm_uuids = uuids,
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
