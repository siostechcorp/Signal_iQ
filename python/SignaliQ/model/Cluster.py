#!/usr/bin/env python
###############################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017 SIOS Technology Corp. All rights reserved.
##############################################################################


class Cluster(object):
    """
    Model for a "Cluster", that is a set of objects that need to be
    protected through availability setting.

    :param str description: Information about the event.
    :param int environment_id: ID of the environment to correlate to.
    :param str name: Display name for the given event.
    """
    def __init__(self,
                 description,
                 environment_id,
                 healthState,
                 id,
                 name,
                 state,
                 ):
        self.description = description
        self.cloudEnvironment = {
            "healthState": "OK",
            "id": environment_id,
        }
        self.healthState = healthState
        self.id = id
        self.name = name
        self.state = state
