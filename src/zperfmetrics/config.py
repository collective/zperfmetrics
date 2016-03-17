# -*- coding: utf-8 -*-
from perfmetrics import set_statsd_client

import socket
import urlparse


class PerfmetricsConfig(object):

    def __init__(self, config):
        prefix = ''
        if config.before:
            prefix += config.before + '.'
        if config.hostname:
            prefix += socket.gethostname() + '.'
        if config.after:
            prefix += config.after + '.'

        url = urlparse.urlparse(config.uri)
        if url.query:
            qs = urlparse.parse_qs(url.query)
            preset = qs.get('prefix', [])
            if preset:
                prefix = preset[0] + '.' + prefix
        parts = list(url)
        parts[4] = 'prefix=' + prefix
        set_statsd_client(urlparse.urlunparse(parts))

    def prepare(self, *args):
        pass

    def create(self, *args):
        pass
