Colosseum Command Line Interface (ColosseumCLI)

# About
Use this utility to manage:
* GPS scenarios
* LXC container snapshots
* RF scenarios
* Traffic generation
* USRP flashed images

# Quick start
This utility is probably already installed, but might be an older version (e.g., `18.0.1`).

* Run `colosseumcli --version`.
* If you get an error `command not found`, or you have a version older than `19.0.0`, see installation instructions below

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
copy the images into your container. Both techniques are left as an exercise for
the reader.

* Get colosseumcli source by checking the common folder
    * `ls /common/colosseumcli/src/`
* Copy the source into your home directory, since building requires write access to this directory, but the `/common` directory is a read-only volume
    * `cp /common/colosseumcli/src ~/`
* Change to the source directory
    * `cd ~/src`
* Install
    * `pip3 install .`
* If the previous command fails, build and install
    * `pip3 wheel . && pip3 install *.whl`
