.. contents:: Table of Contents
   :depth: 2

Perfmetrics configuration for Zope and Plone
============================================

zperfmetrics works like and depends on `perfmetrics <https://pypi.python.org/pypi/perfmetrics>`_, additional it:

- offers a ZConfig configuration for the statsd,
- uses the current requests path in the statd dotted path prefix,
- also provides a patch to measure plone.app.theming for diazo compile and diazo transform if Plone is available,


Installation
============

First get your ``statsd`` configured properly.
This is out of scope of this module.

Depend on this module in your packages ``setup.py``.

Given you use ``zc.builodut`` to set up your Zope2 or Plone,
add to your ``[instance]`` section or the section with ``recipe = plone.recipe.zope2instance`` the lines::

    [instance01]
    recipe = plone.recipe.zope2instance
    ...
    zope-conf-imports =
        zperfmetrics
    zope-conf-additional =
        <perfmetrics>
            uri statsd://localhost:8125
            before MyFancyProject
            hostname on
            after ${:_buildout_section_name_}
        </perfmetrics>
    ...

Given this runs on a host called ``w-plone1``,
this will result in a prefix ``MyFancyProject.w-plone1.instance01``

uri
    Full URI of statd.

before
    Prefix path before the hostname.

hostname
    Get hostname and insert into prefix. (Boolean: ``on`` or ``off``)

after
    Prefix path after the hostname.


Usage
=====

You need to decorate your code or use the ``with`` statement to measure a code block.

Usage::

    from zperfmetrics import ZMetric
    from zperfmetrics import zmetric
    from zperfmetrics import zmetricmethod

    @zmetric
    def some_function():
        # whole functions timing and call counts will be measured
        pass

    @ZMetric(stat='a_custom_prefix')
    def some_other_function():
        # set a custom prefix instead of module path and fucntion name.
        pass

    class Foo(object):

        @zmetricmethod
        def some_method(self):
            # whole methods timing and call counts will be measured
            pass

        @ZMetric(method=True, timing=False):
        def some_counted_method(self):
            # whole methods number of calls will be measured, but no times
            pass

        @ZMetric(method=True, count=False):
        def some_timed_method(self):
            # whole methods timing be measured, but no counts
            pass

        def some_method_partly_measured(self):
            # do something here you dont want to measure
            with ZMetric(stat='part_of_other_method_time'):
                # do something to measure
                # call counts and timing will be measured
                pass
            # do something here you dont want to measure

        @ZMetric(method=True, rate=0.5):
        def some_random_recorded_method(self):
            # randomly record 50% of the calls.
            pass


Zope Request Integration
========================

This package provides subscribers to measure the time a request takes,
including some points in time between.

These subscribers are loaded via zcml and are logging under ``publish.*``:

``publish.traversal``
    time needed from publication start until traversal is finished.

``publish.rendering``
    time needed from traversal end until before commit begin.

``publish.beforecommit``
    time needed from rendering end until database commit begins.
    This value is a bit fuzzy and should be taken with a grain of salt,
    because there can be other subscribers to this event which take their time.
    Since the order of execution of the subscribers is not defined,
    processing may happen after this measurement
    Future improvements planned here.

``publish.commit``
    time needed from rendering end until database commit is done.

``publish.sum``
    whole time needed from publication start until request is completly processed.


Plone Patches
=============

This package provides two default patches:

``diazo.setup``
    ``plone.app.theming.transform.ThemeTransform.setupTransform`` is patched as a basic (path-less) perfmetrics ``Metric``.

``diazo.transform``
    ``plone.app.theming.transform.ThemeTransform.transformIterable`` is patched as a zperfmetrics ``ZMetric``.
    This patch is planned to be removed and replaced by event listeners to every single transform (events available since plone.transformchain 1.2.0).


Source Code
===========

The sources are in a GIT DVCS with its main branches at `github <https://github.com/collective/zperfmetrics>`_.

We'd be happy to see many branches, forks and pull-requests to make zperfmetrics even better.

Contributors
============

- Jens W. Klein <jens@bluedynamics.com>

- Zalán Somogyváry
