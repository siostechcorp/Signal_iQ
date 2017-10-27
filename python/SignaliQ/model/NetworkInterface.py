#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017 SIOS Technology Corp. All rights reserved.
##############################################################################
import logging
__log__ = logging.getLogger(__name__)


class NetworkInterface(object):
    """
    Model for virtual network interface (vNIC). Each interface
    can have any combination of IP Addresses or MAC Addresses.  The
    model must have either a MAC address OR 1 or more IP Address.

    :param str hw_address:  The MAC address of the hardware/virtual
                             network interface.
    :param str[] addresses: List of (IP) addresses configured on the
                             network interface.
    """
    def __init__(self, hw_address = "", addresses = []):
        if not hw_address and not addresses:
            __log__.error(
                "Network Interface invalid! Specify either MAC or IP addresses!"
            )
            return

        self.hwAddress = hw_address.replace("-", ":")
        self.networkAddresses = [{"address": ip} for ip in addresses]
