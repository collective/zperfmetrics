# -*- coding: utf-8 -*-
from time import time
from zperfmetrics import ZMetric


def start_measurement(request):
    request._zperfmetrics_start = time()


def end_measurement(request):
    with ZMetric(stat='request') as metric:
        metric.start = request._zperfmetrics_start
