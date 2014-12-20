#!/usr/bin/env python2.6

import os
import setuptools


setuptools.setup(
  name='clicast',
  version='0.1.2',

  author='Max Zheng',
  author_email='mzheng@linkedin.com',

  description=open('README.rst').read(),

  install_requires=[
    'requests',
  ],

  license='MIT',

  package_dir={'': 'src'},
  packages=setuptools.find_packages('src'),
  include_package_data=True,

  setup_requires=['setuptools-git'],

  classifiers=[
    'Development Status :: 5 - Production/Stable',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Development Tools',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
  ],

  keywords='cli broadcast command warning critical bug',
)
