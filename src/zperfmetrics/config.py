# -*- coding: utf-8 -*-
from perfmetrics import set_statsd_client

import socket
import urlparse


class PerfmetricsConfig(object):

    def __init__(self, config):
        self.uri = config.uri
        self.before = config.before
        self.after = config.after
        self.hostname = config.hostname

    def prepare(self, *args):
        pass

    def create(self, *args):
        prefix = ''
        if self.before:
            prefix += self.before + '.'
        if self.hostname:
            prefix += socket.gethostname() + '.'
        if self.after:
            prefix += self.after + '.'
        prefix = prefix.strip('.')
        url = urlparse.urlparse(self.uri)
        if url.query:
            qs = urlparse.parse_qs(url.query)
            preset = qs.get('prefix', [])
            if preset:
                prefix = preset[0] + '.' + prefix
        parts = list(url)
        parts[4] = 'prefix=' + prefix
        set_statsd_client(urlparse.urlunparse(parts))
