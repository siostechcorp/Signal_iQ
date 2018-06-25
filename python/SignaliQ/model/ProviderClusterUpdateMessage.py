#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017-2018 SIOS Technology Corp. All rights reserved.
##############################################################################

class ProviderClusterUpdateMessage(object):
    """
    Model class for SIOS iQ's "ProviderClusterUpdateMessage". This model is used to
    represent the message injected into the AMQP exchange. Cluster and VM info will
    be used to augment event information.

    :param int environment_id: Environment's id for correlation
    :param clusters: List of cluster objects
    :param vms: List of vm objects
    :type clusters: Cluster[]
    :type vms: CloudVM[]
    """
    def __init__(self, environment_id, clusters = [], vms = []):
        self.environment = {
            "id": environment_id,
            "statusCode": "OK",
        }
        self.clusters = clusters
        self.cloudVMs = vms
