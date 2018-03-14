#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017 SIOS Technology Corp. All rights reserved.
##############################################################################

from SignaliQ.model.CloudVM import CloudVM


class CloudProviderEvent(object):
    """
    Model class for SIOS iQ's "CloudProviderEvent". This model is used to
    represent any event to be injected. A CloudProviderEvent is composed of
    an "environment id", "description", "time the event occurred", and a list
    of the "VM UUIDs" involved in the event.

    The `time` has to be in ISO-8601 format with the timezone. For example,
    `"2017-01-01T22:04:05.678-05:00"`.

    To find the `id` of an environment, log into the SIOS iQ user interface
    and navigate to the "Inventory" dashboard. View the environment's properties
    and the `id` will be available there.

    :param str description: Information about the event.
    :param int environment_id: ID of the environment to correlate to.
    :param str event_type: Type to display in the SIOS iQ UI.
    :param str layer: Either "Compute" or "Storage"
    :param str time: Time of the event.
    :param str[] vm_uuids: List of "UUID"s of the VMs involved in the event.

    :param str category: For anomaly events use "Performance", for
                         availability events use "Reliability".
    :param str internal_type: Type of event.
    :param str name: Display name for the given event.
    :param str source: Value used to filter out sources of events.
    :param str severity: Either "Info", "Warning" or "Critical".
    """
    def __init__(self, description, environment_id,
                 event_type, layer, time,
                 vms = [],
                 vm_uuids = [],
                 category = "Performance",
                 internal_type = "ProviderThirdParty",
                 source = "SDK",
                 severity = "Info"):

        self.assocResourceCollection = {
            "cloudVMs": vms if vms else [CloudVM(uuid = val) for val in vm_uuids]
        }
        self.category = category.capitalize()  # Uppercases only the first letter
        self.cloudEnvironment = {
            "healthState": "OK",
            "id": environment_id,
        }
        self.description = description
        self.impactedResourceCollection = {
            "cloudVMs": [],
        }
        self.internalType = internal_type
        # self.isNoise = False ## Do not specify the isNoise flag
        self.layer = layer.capitalize()  # Uppercases only the first letter
        self.name = event_type
        self.rootCauseResourceCollection = {
            "cloudVMs": [],
        }
        self.severity = severity.capitalize()  # Uppercases only the first letter
        self.source = source
        self.time = time
        self.type = event_type
