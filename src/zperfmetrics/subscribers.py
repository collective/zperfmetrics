# -*- coding: utf-8 -*-
from time import time
from zperfmetrics import ZMetric


def annotate_start_publish(event):
    """annotate start time of publisher
    """
    event.request._zperfmetrics_pubstart = time()


def measurement_after_traversal(event):
    """record time used for traversal.

    annotate start time next steps
    """
    with ZMetric(stat='publish.traversal') as metric:
        metric.start = event.request._zperfmetrics_pubstart
    event.request._zperfmetrics_start = time()


def measurement_after_base_rendering(event):
    """record time needed to prepare the request
    but w/o transforms and database writes.

    This is a bit fuzzy, since there maybe more subscribers to this event.
    What we are interested in is the time when all those subscribers are
    processed.
    But there is no good way to figure this out.
    In order to makes this less fuzzy, we can fallback to different subscriber
    using to this event, the plone.transformchain. So if plone.transformchain
    is not available we log here, otherwise we do nothing here, bit let
    plone.transformchain do the job.
    We achieve this by ZCML registering either this subscriber or the
    plone.transformchain one, but never both.
    """
    try:
        start = event.request._zperfmetrics_start
    except AttributeError:
        # some requests do not fire an after traversal event, so we
        # use the pubstart instead
        start = event.request._zperfmetrics_pubstart
    with ZMetric(stat='publish.rendering') as metric:
        metric.start = start
    event.request._zperfmetrics_start = time()


def measurement_request_success(event):
    """record overall time needed to publish the request.
    """
    with ZMetric(stat='publish.finalize') as metric:
        metric.start = event.request._zperfmetrics_start
        metric.request = event.request
    with ZMetric(stat='publish.sum') as metric:
        metric.start = event.request._zperfmetrics_pubstart
        metric.request = event.request


# measure plone.transformchain transforms
def annotate_start_transforms(event):
    """annotate start time of all transforms.
    """

    # see docstring of this function above
    measurement_after_base_rendering(event)

    event.request._zperfmetrics_transforms_start = time()


def annotate_start_single_transform(event):
    """annotate start time of a single transform.
    """
    start = time()
    try:
        event.request._zperfmetrics_transform_start[event.name] = start
    except AttributeError:
        event.request._zperfmetrics_transform_start = {}
        event.request._zperfmetrics_transform_start[event.name] = start


def measurement_after_single_transform(event):
    """record metric of the single transform
    """
    start = event.request._zperfmetrics_transform_start[event.name]
    stat = 'publish.transform_single.{0}-{1}'.format(
        event.handler.order,
        event.name.replace('.', '-')
    )
    with ZMetric(stat=stat) as metric:
        metric.start = start
        metric.request = event.request


def measurement_after_transforms(event):
    """record metric of the all transforms
    """

    start = event.request._zperfmetrics_transforms_start
    with ZMetric(stat='publish.transform_all') as metric:
        metric.start = start
        metric.request = event.request

    # reset start to measure db commit time
    event.request._zperfmetrics_start = time()
