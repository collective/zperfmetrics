# -*- coding: utf-8 -*-
from time import time
from zperfmetrics import ZMetric


def annotate_start_publish(event):
    event.request._zperfmetrics_pubstart = time()


def measurement_after_traversal(event):
    with ZMetric(stat='publish.traversal') as metric:
        metric.start = event.request._zperfmetrics_pubstart
    event.request._zperfmetrics_start = time()


def measurement_before_commit(event):
    with ZMetric(stat='publish.beforecommit') as metric:
        metric.start = event.request._zperfmetrics_start
    event.request._zperfmetrics_start = time()


def measurement_request_success(event):
    with ZMetric(stat='publish.sum') as metric:
        metric.start = event.request._zperfmetrics_start
        metric.request = event.request
