#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017-2018 SIOS Technology Corp. All rights reserved.
##############################################################################
import logging
__log__ = logging.getLogger(__name__)


class CloudVM(object):
    """
    Model for virtual machines. Typically, the UUID is provided by
    the environment.

    :param str uuid: Unique identifier for the VM.
    :param network_interfaces: Network interfaces for the VM.
    :param clusters (optional): Clusters for the VM.
    :type network_interfaces: NetworkInterface[]
    :type clusters: Cluster[]
    """
    def __init__(self, uuid = "", network_interfaces = [], clusters = []):
        if not uuid and not network_interfaces:
            __log__.error(
                "Must provide either the uuid and/or the network interfaces!"
            )
            return

        self.uuid = uuid
        self.networkInterfaces = network_interfaces
        self.clusters = clusters
