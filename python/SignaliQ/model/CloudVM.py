#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017 SIOS Technology Corp. All rights reserved.
##############################################################################
import logging
__log__ = logging.getLogger(__name__)


class CloudVM(object):
    """
    Model for virtual machines. Typically, the UUID is provided by
    the environment.

    :param str uuid: Unique identifier for the VM.
    """
    def __init__(self, uuid = "", network_interfaces = []):
        if not uuid and not network_interfaces:
            __log__.error(
                "Must provide either the uuid and/or the network interfaces!"
            )
            return

        self.networkInterfaces = network_interfaces
        self.uuid = uuid
