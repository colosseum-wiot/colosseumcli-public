#!/usr/bin/env python

PROJECT = 'colosseumcli'

# Change docs/sphinx/conf.py too!
VERSION = '18.05.0'

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Cliff app for the colosseum',
    long_description=long_description,

    author='Alex White',
    author_email='alex.white@jhuapl.edu',

    url='https://github.com/openstack/cliff',
    download_url='https://github.com/openstack/cliff/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'colosseumcli = colosseum_cli.cli_app:main'
        ],
        'cliff.colosseum': [
            'rf_start = colosseum_cli.rf_scenario:rf_scenario_start',
            'rf_stop = colosseum_cli.rf_scenario:rf_scenario_stop',
            'rf_info = colosseum_cli.rf_scenario:rf_scenario_info',
            'rf_radiomap = colosseum_cli.rf_scenario:rf_scenario_radio_map',
            'rf_scenario_list = colosseum_cli.rf_scenario:rf_scenario_list',
            'rf_scenario_nodelist = colosseum_cli.rf_scenario:rf_scenario_list_nodes',
            'snapshot = colosseum_cli.container:container_snapshot',
            'gps_start = colosseum_cli.gps:gps_start',
            'gps_stop = colosseum_cli.gps:gps_stop',
            'gps_scenario_list = colosseum_cli.gps:gps_scenario_list',
            'gps_info = colosseum_cli.gps:gps_info',
            'tg_start = colosseum_cli.tgen:tgen_start',
            'tg_stop = colosseum_cli.tgen:tgen_stop',
            'tg_info = colosseum_cli.tgen:tgen_info',
            'tg_nodemap = colosseum_cli.tgen:tgen_nodemap',
            'tg_scenario_list = colosseum_cli.tgen:tgen_scenario_list',
        ],
    },

    zip_safe=False,
)
