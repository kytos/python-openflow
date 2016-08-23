Hacking
=======

Before reading this file, please read the :doc:`CONTRIBUTE` section that
contains the main guidelines of the project.

Development Environment Setup
-----------------------------

This project is written in Python (version 3.5).

You need to add the pyof folder, located in this repository root, to your
PYTHONPATH environment variable. For that, you have to execute the following on
the command line (while in the repository root folder):

.. code:: shell

    export PYTHONPATH=`pwd`/ofp:$PYTHONPATH

Remember that every time you start a new shell instance you will have to repeat
the command above, since this is an environment variable. To have it executed
automatically in every shell, add it to ``~/.bashrc`` replacing ``pwd`` by the
full path of the repository (output of ``pwd``).

Virtualenv
~~~~~~~~~~

Another option is to use *virtualenv*. It installs the required and
recommended python libraries without messing up with your system. Besides, you
don't need to manually change the PYTHONPATH variable. To install it, run
the following commands:

.. code:: shell

    sudo apt install python3-pip
    sudo pip3 install virtualenv virtualenvwrapper

If you are working with **bash**, add the following lines on your
``~/.bash_profile`` or ``~/.bashrc`` to setup *virtualenvwrapper*:

.. code:: shell

    export WORKON_HOME=~/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh

If you are using `oh-my-zsh <https://github.com/robbyrussell/oh-my-zsh>`__, you
can just add the *virtualenvwrapper* plugin to your plugins list
(inside ``~/.zshrc``). This plugin will:

-  Load Python's `virtualenvwrapper shell tools <http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html>`__;
-  Automatically activate virtualenv when ``cd``'ing into git repository with a
   matching name.

We also recommend adding the bellow code to your
``~/.virtualenvs/postmkvirtualenv`` file:

.. code:: shell

    echo '_OLD_PYTHONPATH="$PYTHONPATH"' >> ~/.virtualenvs/"${PWD##*/}"/bin/postactivate
    echo "PYTHONPATH="'"'$(pwd)'"' >> ~/.virtualenvs/"${PWD##*/}"/bin/postactivate
    echo 'PYTHONPATH="$_OLD_PYTHONPATH"' >> ~/.virtualenvs/"${PWD##*/}"/bin/postdeactivate

This will change the PYTHONPATH environment variable to your projects path when
the virtualenv is activated.

After installed, clone this repository locally, ``cd`` into it and create the
required virtualenv with the same name as the repository directory:

.. code:: shell

    mkvirtualenv "${PWD##*/}" -r requirements-dev.txt

This will create the virtualenv with all project requirements and also activate
it.

The standard setup finishes here.

If you are using ``oh-my-zsh`` plugin then every time you enter on the project
directory, the virtualenvironment will be automaticaly loaded. If you are using
bash, then you need to run the ``workon`` command to activate the environment:

.. code:: shell

    workon python-openflow

See more virtualenvwrapper commands on:
http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html

Virtualenv Extras
^^^^^^^^^^^^^^^^^

If you want to show the current activated virtualenv on the right side of your
shell, add the following code to your ``~/.virtualenvs/postactivate`` file:

.. code:: shell

    PS1="$_OLD_VIRTUAL_PS1"
    _OLD_RPROMPT="$RPROMPT"
    RPROMPT="%{${fg_bold[white]}%}(env: %{${fg[white]}%}`basename \"$VIRTUAL_ENV\"`%{${fg_bold[white]}%})%{${reset_color}%} $RPROMPT"

Change the colors to your own preferences.

and also this code to your ``~/.virtualenvs/postdeactivate`` file:

.. code:: shell

    RPROMPT="$_OLD_RPROMPT"

TDD (Test Driven Development)
-----------------------------

We aim at 100% of test coverage. We are using
Python `unittest <https://docs.python.org/3.5/library/unittest.html>`__ to
write tests and
`coverage.py <https://coverage.readthedocs.org/en/coverage-4.0.3/>`__ for
coverage metrics. To install the coverage (python3 version), run:

.. code:: shell

    pip3 install coverage

To run the tests, use the following command on the root folder of the project:

.. code:: shell

    python3 setup.py test

To run check the code test coverage, first run:

.. code:: shell

    coverage run setup.py test

To see the command line report run the command ``coverage report`` and, to
generate a HTML report, run: ``coverage html`` and open the file
**html\_cov/index.html** into your browser
(you can run ``open html_cov/index.html``).
