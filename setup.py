#!/usr/bin/env python2.6

import setuptools


setuptools.setup(
    name='clicast',
    version='0.4.5',

    author='Max Zheng',
    author_email='maxzheng.os @t gmail.com',

    description='Broadcast messages for CLI tools, such as a warning for critical bug '
                'or notification about new features.',
    long_description=open('README.rst').read(),

    url='https://github.com/maxzheng/clicast',

    entry_points={
        'console_scripts': [
            'cast = clicast.editor:cast',
        ],
    },

    install_requires=open('requirements.txt').read(),

    license='MIT',

    packages=setuptools.find_packages(),
    include_package_data=True,

    setup_requires=['setuptools-git', 'wheel'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='cli broadcast command warning critical bug',
)
