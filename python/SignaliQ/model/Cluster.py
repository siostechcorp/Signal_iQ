#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017-2018 SIOS Technology Corp. All rights reserved.
##############################################################################
import logging
from enum import Enum
__log__ = logging.getLogger(__name__)


class Cluster(object):
    """
    Model for clusters. Typically, the UUID is provided by the environment.

    :param str name: Name for the Cluster.
    :param str uuid: Unique identifier for the Cluster.
    :param str state: State of the Cluster.
    :param ClusterType type: Type of Cluster.
    """
    def __init__(self, name, uuid, state, type):
        if not uuid or not name or not state:
            __log__.error("Must provide the name, state, and uuid!")
            return

        if not isinstance(type, ClusterType):
            raise TypeError('cluster type must be an instance of ClusterType')

        self.name = name
        self.uuid = uuid
        self.state = state

# Enum for cluster type.
class ClusterType(Enum):
    vSphere = "vSphere"
    WSFC = "WSFC"
    LifeKeeper = "LifeKeeper"
