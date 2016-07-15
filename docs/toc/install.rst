Installation
============

This library was built to run on Unix-like distributions. You need at least
`python3` as a dependency. We also make use of `setuptools` to ease the
installation process.

You can install this package with pip package installer or from source code.

Installing from PyPI
--------------------

*python-openflow* is in PyPI, so you can easily install it via `pip3` (`pip`
for Python 3) and it is also possible to include this project in your
`requirements.txt` (don't worry if you don't recognize this file):

.. code-block:: shell

   $ sudo pip3 install python-openflow

Installing from source/git
--------------------------

First you need to clone `python-openflow` repository:

.. code-block:: shell

   $ git clone https://github.com/kytos/python-openflow.git


After cloning, the installation process is done by `setuptools` in the usual
way:

.. code-block:: shell

   $ cd python-openflow
   $ sudo python3 setup.py install

Checking installation
---------------------

That's it! To check wether it is installed successfully, please try to import
after running ``python3`` or ``ipython3``:

.. code-block:: python3

   >>> import pyof
   >>> # no errors should be displayed
