
History
=======

1.0b3 (unreleased)
------------------

- Nothing changed yet.


1.0b2 (2016-08-04)
------------------

- Fix: Name of a single transform may contaibn dots.
  They are now replaced by ``_``.
  [jensens]

- Fix: The root element of a path was not shown on the same level as all other paths.
  Now it is shown as ``__root__``
  [jensens]

- Feature: It was not possible to filter by virtual host in environment with more than one site per Zope.
  A new configuration option ``virtualhost`` was introduced.
  If set to on, the virtualhost name will be inserted before ``PATH``.
  [jensens]

- Support: In order to make a test installation easier,
  an example docker-compose setup was added to the Github repository together with some documentation in the README.rst.
  [jensens]

1.0b1 (2016-08-04)
------------------

- Added subscribers to ``plone.transformchain`` events.
  New setup extra ``[plone]``.
  Removed one patch for diazo transform.
  Made ``publish.beforecommit`` less fuzzy in Plone.
  [jensens]

1.0a7 (2016-08-03)
------------------

- Fix: virtual path config in ZMetric class.
  [syzn]


1.0a6 (2016-07-28)
------------------

- Feature: New value publish.commit.
  Delta time used from publish.beforecommit to request end.
  [jensens]

- Fix: publish.sum shows now overall time of request processing.
  [jensens]

- Fix: Update README to reflect last changes.
  [jensens]

- Use more beautiful paths if VirtualHostMonster is used.
  [syzn]


1.0a5 (2016-06-28)
------------------

- Fix: Before/after hooks were not assigned correctly.
  [jensens]


1.0a4 (2016-06-10)
------------------

- Fixes measurements of zope request, also add more detailed metrics.
  [jensens]


1.0a3 (2016-06-09)
------------------

- Measure time a zope request needs.
  [jensens]


1.0a2 (2016-03-22)
------------------

- Refactored: ZConfig best practice
  [jensens]

- Fix: Strip trailing dot from prefix
  [jensens]


1.0a1 (2016-03-22)
------------------

- Fix: README was wrong.
  [jensens]


1.0a0 (2016-03-22)
------------------

- made it work [jensens, 2016-03-17]

