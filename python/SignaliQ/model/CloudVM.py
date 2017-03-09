#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017 SIOS Technology Corp. All rights reserved.
##############################################################################


class CloudVM(object):
    """
    Model for virtual machines. Typically, the UUID is provided by the environment.

    :param str uuid: Unique identifier for the VM.
    """
    def __init__(self, uuid):
        self.uuid = uuid
