Installation
============

This library was built to run on Unix-Like distributions. You need at least
``python3`` as dependency. We also make use of ``setuptools`` to make it easy
for you the installation process.

You can install this package from sources or via pip.

Installing from source/git
--------------------------

First you need to clone ``python-openflow`` repository:

.. code-block:: shell

   $ git clone https://github.com/kytos/python-openflow.git


After clone, the installation process is normal when using ``setuptools``:

.. code-block:: shell

   $ cd python-openflow
   $ sudo python3 setup.py install

Installing from pypi
--------------------

Yes, you can include this project in your ``requirements.txt`` or install from
``pip3``:

.. code-block:: shell

   $ sudo pip3 install python-openflow

Checking installation
---------------------

That is it! To check if you have installed please try to import with `python` or
`ipython`:

.. code-block:: python3

   >>> import pyof

