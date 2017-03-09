#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017 SIOS Technology Corp. All rights reserved.
##############################################################################


class ProviderEventsUpdateMessage(object):
    """
    Model class for SIOS iQ's "ProviderEventsUpdateMessage". This model is used to
    represent the message injected into the AMQP exchange. Each event will
    be used in the correlations.

    :param int environment_id: Environment's id for correlation
    :param events: List of event objects
    :type events: CloudProviderEvent.CloudProviderEvent[]
    """
    def __init__(self, environment_id, events):
        self.environment = {
            "id": environment_id,
            "statusCode": "OK",
        }
        self.events = events
