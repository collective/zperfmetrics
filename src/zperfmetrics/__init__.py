# -*- coding: utf-8 -*-
from perfmetrics import Metric
from perfmetrics import client_stack
from perfmetrics import statsd_client_stack
from time import time
from zope.globalrequest import getRequest

import functools
import zperfmetrics.patches

zperfmetrics.patches  # flake 8 happiness


class ZMetric(Metric):
    """Make metric decorator/context managers for Zope Requests.
    """

    def __call__(self, f):
        """Decorate a function or method so it can send statistics to statsd.
        """
        func_name = f.__name__
        func_full_name = (f.__module__, func_name)

        instance_stat = self.stat
        rate = self.rate
        method = self.method
        count = self.count
        timing = self.timing
        timing_format = self.timing_format
        instance_random = self.random

        def call_with_metric(*args, **kw):
            if rate < 1 and instance_random() >= rate:
                # Ignore this sample.
                return f(*args, **kw)

            stack = statsd_client_stack.stack
            client = stack[-1] if stack else client_stack.default
            if client is None:
                # No statsd client has been configured.
                return f(*args, **kw)

            if instance_stat:
                statpart = instance_stat
            elif method:
                cls = args[0].__class__
                statpart = '.'.join([cls.__module__, cls.__name__, func_name])
            else:
                statpart = func_full_name

            stat = ''
            request = getRequest()
            if request:
                stat += '.PATH.' + request['PATH_INFO']
                stat += '.' + statpart
            else:
                stat = statpart

            if timing:
                if count:
                    buf = []
                    client.incr(stat, 1, rate, buf=buf, rate_applied=True)
                else:
                    buf = None
                start = time()
                try:
                    return f(*args, **kw)
                finally:
                    elapsed_ms = int((time() - start) * 1000.0)
                    client.timing(timing_format % stat, elapsed_ms,
                                  rate, buf=buf, rate_applied=True)
                    if buf:
                        client.sendbuf(buf)

            else:
                if count:
                    client.incr(stat, 1, rate, rate_applied=True)
                return f(*args, **kw)

        return functools.update_wrapper(call_with_metric, f)

    # Metric can also be used as a context manager.

    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, _typ, _value, _tb):
        rate = self.rate
        if rate < 1 and self.random() >= rate:
            # Ignore this sample.
            return

        stack = statsd_client_stack.stack
        client = stack[-1] if stack else client_stack.default
        if client is not None and self.stat:
            buf = []
            request = getRequest()
            if request:
                stat = '.PATH.' + request['PATH_INFO']
                stat += '.' + self.stat
            else:
                stat = self.stat
            if stat:
                if self.count:
                    client.incr(stat, rate=rate, buf=buf, rate_applied=True)
                if self.timing:
                    elapsed = int((time() - self.start) * 1000.0)
                    client.timing(self.timing_format % stat, elapsed,
                                  rate=rate, buf=buf, rate_applied=True)
                if buf:
                    client.sendbuf(buf)

zmetric = ZMetric()

zmetricmethod = ZMetric(method=True)
