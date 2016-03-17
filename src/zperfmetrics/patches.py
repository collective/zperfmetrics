# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)


def initialize(context):
    try:
        from plone.app.theming.transform import ThemeTransform
        from perfmetrics import Metric
        from zperfmetrics import ZMetric
    except ImportError:
        logger.info('No Plone patches for zperfmetrics')
        return

    # patch to measure plone.app.theming
    logger.info('Activating Plone patches for zperfmetrics')
    ThemeTransform.setupTransform = Metric(
        stat='diazo.setup',
        method=True,
    )(
        ThemeTransform.setupTransform
    )
    ThemeTransform.transformIterable = ZMetric(
        stat='diazo.transform',
        method=True
    )(
        ThemeTransform.transformIterable
    )
