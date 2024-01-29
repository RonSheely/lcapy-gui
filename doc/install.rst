.. _installation:

============
Installation
============

Recommended Install Method
==========================
It is recommended to install lcapy-gui inside a python venv.  This will
ensure that the lcapy-gui installation does not interfere with other python packages.

Arch Linux requires a virtual environment to be used, as lcapy-gui is unavailable in the Arch Linux repositories, and
Arch disallows packages to be installed by pip into the system python.

For more information on using virtual environments, see https://docs.python.org/3/library/venv.html

Before installing, please ensure you have python version 3.8 or greater installed on your system.

1. Create a new python venv

    This can be done using the following command:

    .. code-block:: console

        $ python -m venv INSTALL_PATH

    be sure to replace ``INSTALL_PATH`` with the path to the new virtual environment.
    Make sure this path is somewhere you wont erase it by mistake.

    Because lcapy-gui uses ``~/.lcapy`` to store its settings, file, a good place for your venv  could be ``~/.lcapy/venv``


2. Install lcapy-gui

    To use python in the venv, you must use the new python binaries located in the venv directory.

    **Linux/macOS**

    .. code-block:: console

        $ INSTALL_PATH/bin/pip install lcapygui

    **Windows**

    .. code-block:: console

        $ INSTALL_PATH/scripts/pip install lcapygui

    This will automatically download Lcapy and the other required Python
    packages.  However, if you wish to create PDF and PNG images, you will
    need to install LaTeX and Circuitikz (see
    https://lcapy.readthedocs.io/en/latest/install.html).

3. Running lcapy-gui

    Lcapy-gui can be run using the following command:

    **Linux/macOS***

    .. code-block:: console

        $ INSTALL_PATH/bin/lcapy-tk

    **Windows**

    .. code-block:: console

        $ INSTALL_PATH/scripts/lcapy-tk

4. Get a start menu shortcut

    Sometimes it can be nice to have a desktop shortcut to launch lcapy-gui. To do this, we use the ``pyshortcuts`` package.
    The specific command to execute varies between devices.

    **Linux/macOS***

    .. code-block:: console

        $ INSTALL_PATH/bin/lcapy-tk --create-shortcut

    **Windows**

    .. code-block:: console

        $ INSTALL_PATH/scripts/lcapy-tk --create-shortcut

    If the icon does not appear right away, you may need to log out and log back in. If the icon still does not appear,
    check the shortcut directory output from the command above.




Installation of latest version
==============================

If you wish to install the latest version from the git repository use:

.. code-block:: console

   $ pip install git+https://github.com/mph-/lcapy-gui.git#egg=lcapy-gui

However, it is better to fork or clone the git repository if you wish to make fixes.
