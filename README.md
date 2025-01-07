Colosseum Command Line Interface

# About
Use this utility to manage:
* GPS scenarios
* LXC container snapshots
* RF scenarios
* Traffic generation
* USRP flashed images

# Quick start
This utility is probably already installed!

* Run `colosseumcli --help`.
* If you get error `command not found`, see installation instructions below

# Installing from packages
**NOTE: requires Python 3**

If you do not see a package for your Python version, try building from source - see below.

* Get your Python minor version
    * `export python_minor=$(python3 -c 'import sys; print(sys.version_info.minor)')`
* Install your Python version's packages
    * `pip3 install --ignore-installed /common/colosseumcli/packages/python-3.${python_minor}/*.whl`
    * This example ignores installed versions because we install on the root file system
* Verify installation
    * `colosseumcli --version`
    * As of November 2024, this returns `19.0.0`

# Installing from source
If you want to install from source, first pull build prerequisites into your
image. Either get internet access for your container, or manually identify and
copy the images into your container. Both techniques are left as an exercise to
the reader.

* Get colosseumcli source
    * Look in `/common/colosseumcli/src/`
* Copy the source into your home directory
    * Building requires write access to this directory, but the `/common` directory is a read-only volume
* Change to the source directory
* Install
    * `pip3 install .`
* OR Build and install
    * `pip3 wheel . && pip3 install *.whl`
