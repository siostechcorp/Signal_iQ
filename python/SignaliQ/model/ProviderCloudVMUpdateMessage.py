#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017-2018 SIOS Technology Corp. All rights reserved.
##############################################################################

class ProviderCloudVMUpdateMessage(object):
    """
    Model class for SIOS iQ's "ProviderCloudVMUpdateMessage". This model is used to
    represent the message injected into the AMQP exchange. VM info will
    be used to augment SIOS iQ event information.

    :param int environment_id: Environment's id for correlation
    :param vms: List of vm objects
    :type vms: CloudVM[]
    """
    def __init__(self, environment_id, vms = []):
        self.environment = {
            "id": environment_id,
            "statusCode": "OK",
        }
        self.cloudVMs = vms
