#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017-2018 SIOS Technology Corp. All rights reserved.
##############################################################################
import logging
__log__ = logging.getLogger(__name__)


class Cluster(object):
    """
    Model for clusters. Typically, the UUID is provided by the environment.

    :param str uuid: Unique identifier for the Cluster.
    """
    def __init__(self, uuid = ""):
        if not uuid:
            __log__.error("Must provide the uuid!")
            return

        self.uuid = uuid
