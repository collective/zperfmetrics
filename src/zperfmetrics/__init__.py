# -*- coding: utf-8 -*-
from perfmetrics import client_stack
from perfmetrics import Metric
from perfmetrics import statsd_client_stack
from time import time
from urlparse import urlparse
from zope.globalrequest import getRequest
from zperfmetrics.config import CONFIG

import functools
import random
import zperfmetrics.patches


zperfmetrics.patches  # flake 8 happiness


class ZMetric(Metric):
    """Make metric decorator/context managers for Zope Requests.
    """

    def __init__(
        self,
        stat=None,
        rate=1,
        method=False,
        count=True,
        timing=True,
        timing_format='%s.t',
        random=random.random,
        before_hook=None,
        after_hook=None,
    ):
        super(ZMetric, self).__init__(
            stat=stat,
            rate=rate,
            method=method,
            count=count,
            timing=timing,
            timing_format=timing_format,
            random=random,
        )
        self.before_hook = before_hook
        self.after_hook = after_hook

    def _handle_virtual_url(self, request, stat_postfix):
        stat = ['request_lifecycle']
        path_info = request['PATH_INFO']
        if (
            'VIRTUAL_URL_PARTS' in request and
            request['VIRTUAL_URL_PARTS'] and
            len(request['VIRTUAL_URL_PARTS']) > 1
        ):
            if CONFIG['virtualhost']:
                parsed = urlparse(request['VIRTUAL_URL_PARTS'][0])
                stat.append(parsed.hostname.replace('.', '_'))
            path_info = request['VIRTUAL_URL_PARTS'][1]
        elif CONFIG['virtualhost']:
            stat.append('__no_virtualhost__')
        if not path_info:
            path_info = '__root__'
        stat.append(path_info.replace('.', '_'))
        stat.append(stat_postfix)
        return '.'.join(stat)

    def __call__(self, f):
        """Decorate a function or method so it can send statistics to statsd.
        """
        if self.before_hook is not None:
            self.before_hook(self)
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
                stat = instance_stat
            elif method:
                cls = args[0].__class__
                stat = '.'.join([cls.__module__, cls.__name__, func_name])
            else:
                stat = func_full_name

            request = self._request
            if request:
                stat = self._handle_virtual_url(request, stat)

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
                    client.timing(
                        timing_format % stat,
                        elapsed_ms,
                        rate,
                        buf=buf,
                        rate_applied=True
                    )
                    if buf:
                        client.sendbuf(buf)

            else:
                if count:
                    client.incr(stat, 1, rate, rate_applied=True)
                return f(*args, **kw)

        if self.after_hook is not None:
            self.after_hook(self)

        return functools.update_wrapper(call_with_metric, f)

    # Metric can also be used as a context manager.

    def __enter__(self):
        if self.before_hook is not None:
            self.before_hook(self)
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
            request = self._request
            if request:
                stat = self._handle_virtual_url(request, self.stat)
            else:
                stat = self.stat
            if stat:
                if self.count:
                    client.incr(stat, rate=rate, buf=buf, rate_applied=True)
                if self.timing:
                    elapsed_ms = int((time() - self.start) * 1000.0)
                    client.timing(
                        self.timing_format % stat,
                        elapsed_ms,
                        rate=rate,
                        buf=buf,
                        rate_applied=True
                    )
                if buf:
                    client.sendbuf(buf)

        if self.after_hook is not None:
            self.after_hook(self)

    @property
    def _request(self):
        return getattr(self, 'request', getRequest())


zmetric = ZMetric()

zmetricmethod = ZMetric(method=True)
