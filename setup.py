# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.0a3'
shortdesc = 'Perfmetrics configuration for Zope/Plone.'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'CHANGES.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()

setup(
    name='zperfmetrics',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    keywords='plone zope perfmetrics statsd graphite monitor performance',
    author='BlueDynamics Alliance',
    author_email='dev@bluedynamics.com',
    url="http://github.com/collective/zperfmetrics",
    license='Simplified BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'perfmetrics',
        'setuptools',
        'zope.globalrequest',
        'Zope2',
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
