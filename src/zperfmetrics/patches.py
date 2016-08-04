# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)


def _patch_diazo():
    """Measure setup/compile time of diazo.

    This is the time needed to build the xslt from the rules and index.html
    files.
    """
    try:
        from plone.app.theming.transform import ThemeTransform
        from perfmetrics import Metric
    except ImportError:
        logger.debug('No Plone Diazo patche for zperfmetrics')
        return

    # patch to measure plone.app.theming by wrapping with a Metric,
    # similar to decorating.
    logger.info('Activating Plone Diazo patch for zperfmetrics')
    ThemeTransform.setupTransform = Metric(
        stat='diazo.setup',
        method=True,
    )(
        ThemeTransform.setupTransform
    )


def initialize(context):
    _patch_diazo()
