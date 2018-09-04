#!/usr/bin/env python
################################################################################
# vim: tabstop=4:shiftwidth=4:expandtab:
# Copyright (c) 2017-2018 SIOS Technology Corp. All rights reserved.
################################################################################
"""
This is the generic client library for use with SIOS iQ's Event Correlation API.
You can use this library to send events into SIOS iQ from external sources.
"""

import amqp
# handle python 2 and 3
try:
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser
import json
import logging
from functools import partial
import os.path as path
import ssl
import sys

from SignaliQ.model.ProviderEventsUpdateMessage import ProviderEventsUpdateMessage
from SignaliQ.model.ProviderCloudVMUpdateMessage import ProviderCloudVMUpdateMessage

__log__ = logging.getLogger(__name__)


class Client(object):
    """
    Connector to the AMQP server on a SIOS iQ instance.

    :param dict config: Override the default configuration.
    """
    def __init__(self, config = None):
        self._channel = None
        self._connection = None
        self._current_dir = None
        self._params = None

        self._config = config if config else self._build_config_from_file()

        # Setup logging
        log_config = self._config.get("logging", {})
        logging.basicConfig(
            level = log_config.get("level", "INFO"),
            datefmt = log_config.get("date_format", "%m-%d-%Y %I:%M:%S.%f"),
        )

    ###
    # PUBLIC
    ###
    def connect(self):
        """
        Connects to the given AMQP instance, defined in `self._config`.

        :returns Bool: True if connection and channel is established successfully.
        """
        params = self._build_connection_params()

        self._connection = amqp.Connection(**params)

        # handle older and newer versions of amqp
        try:
            self._connection.connect()
        except: # NOQA
            pass

        self._channel = self._connection.channel()

        is_valid_connection = self._connection and self._channel

        if is_valid_connection:
            __log__.info("Connection successfully created.")
        else:
            __log__.error("FAILED to create connection or channel!")

        return is_valid_connection

    def disconnect(self):
        """
        Disconnects all connections and handles cleanup.

        :returns: Result of the connection close method.
        """
        return self._connection.close()

    def send(self, message):
        """
        Send the data to the registered connections. Requires that
        a valid connection has been established.

        :param ProviderEventsUpdateMessage message: Message to send (publish), typically as a JSON string.
        :type message: ProviderEventsUpdateMessage.ProviderEventsUpdateMessage
        :returns: Promise representing the publish request
        :rtype: Promise
        """
        if self._connection is None or self._channel is None:
            __log__.error("Connection or channel is not defined! Must call `connect` first!")
            return False

        if message is None or (not isinstance(message, ProviderEventsUpdateMessage) and not isinstance(message, ProviderCloudVMUpdateMessage)):
            __log__.error(
                "Message is not valid! %s. Expected to be ProviderEventsUpdateMessage",
                message
            )
            return False

        body = self._build_message_body(message)
        publish_result = self._channel.basic_publish_confirm(
            body,
            exchange = self.__amqp_config__["exchange"],
        )

        __log__.info("Message sent to %s", self._config["connection"]["host"])

        return publish_result

    ###
    # HELPERS
    ###
    def _build_connection_params(self):
        """
        Build connection parameters, including the SSL configuration.

        :returns: The dict of configuration for setting up connection
        :rtype: dict
        """
        amqp_config = self.__amqp_config__
        creds_config = self._config["credentials"]
        ssl_config = self.__ssl_config__
        ssl_dir = partial(path.join, self._current_dir, ssl_config["directory"])

        ssl_opts = {
            "ca_certs": ssl_dir(ssl_config["ca_certs"]),
            "certfile": ssl_dir(ssl_config["certfile"]),
            "keyfile": ssl_dir(ssl_config["keyfile"]),
            "cert_reqs": ssl_config["cert_reqs"],
        }

        params = {
            "host": "{}:{}".format(self._config["connection"]["host"], amqp_config["port"]),
            "insist": amqp_config["insist"],
            "login_method": amqp_config["login_method"],
            "password": creds_config["password"],
            "ssl": ssl_opts,
            "userid": creds_config["user"],
            "virtual_host": amqp_config["virtualhost"],
        }

        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            __log__.debug("Connection params: \n" + json.dumps(params, indent = 4))

        return params

    def _build_config_from_file(self):
        """
        Handles building config dict from the standard config file, typically `config.ini`.

        :returns: The config object from the default config file
        :rtype: dict
        """
        config_file = path.join(self._get_current_dir(), "config.ini")
        if not path.exists(config_file):
            message = (
                "Expected to see config file at {}. \n\n"
                "Copy `config.sample.ini` to `config.ini`, and update the required \n"
                "fields such as username, password, and hostname. \n"
            ).format(config_file)
            sys.stderr.write(message)
            sys.exit(1)

        # Uses the RawConfigParser to prevent interpolation
        parser = RawConfigParser()
        parser.read(config_file)

        # Convert configparser into regular dict
        config = {}
        for section in parser.sections():
            config[section] = {}
            for opt in parser.options(section):
                config[section][opt] = parser.get(section, opt)

        return config

    def _build_message_body(self, message):
        """
        Build the AMQP message based on the input data
        and the client's config.

        :param ProviderEventsUpdateMessage message: Data for message body
        :returns: Message with configuration
        :rtype: amqp.Message
        """
        message_str = json.dumps(message, default = self._serialize_models)

        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            txt = json.dumps(json.loads(message_str), indent = 4, separators = (',', ': '))
            __log__.debug("Message: \n" + txt)

        return amqp.Message(
            body = message_str,
            content_type = self.__amqp_config__["content_type"],
            content_encoding = self.__amqp_config__["content_encoding"],
            application_headers = {
                "__TypeId__": "com.sios.stc.model.messaging." + type(message).__name__
            }
        )

    def _get_current_dir(self):
        """
        :returns str: Current directory of script
        """
        if self._current_dir:
            return self._current_dir

        self._current_dir = path.dirname(path.realpath(__file__))
        return self._current_dir

    def _serialize_models(self, obj):
        """
        Generic handler passed to `json.dumps`. This handles serializing
        the models to the JSON string.

        :param object obj: The model (or builtin type) currently being iterated over
        :returns: The objects `__dict__` property.
        """
        return obj.__dict__

    ###
    # PROPERTIES
    ###
    __amqp_config__ = {
        "content_encoding": "UTF-8",
        "content_type": "application/json",
        "exchange": "cldo.exchange.provider.allservices",
        "insist": True,
        "login_method": "AMQPLAIN",
        "port": 5671,
        "type": "EVENT_INTERNAL_TYPE_PROVIDER_THIRD_PARTY",
        "virtualhost": "/",
    }

    __ssl_config__ = {
        "ca_certs": "ca_certificate.pem",
        "cert_reqs": ssl.CERT_REQUIRED,
        "certfile": "client_certificate.pem",
        "directory": "certs",
        "keyfile": "client_key.pem",
    }
