
Before reading this file, please read the [CONTRIBUTE](CONTRIBUTE.md) file, that
contains the main guidelines of the project.

## Development Environment setup

This project is based on python (version 3.5).

We recommend that you install python ```virtualenv``` so you can install the
required and recommended python libraries without messing up with your system.
To install them run the following commands:

   ```shell
   $ sudo apt install python3-pip
   $ sudo pip3 install virtualenv virtualenvwrapper
   ```
   
If you are working with **bash**, add the following lines on your
```~/.bash_profile``` or ```~/.bashrc``` to setup ```virtualenvwrapper```:

   ```shell
   export WORKON_HOME=~/.virtualenvs
   source /usr/local/bin/virtualenvwrapper.sh
   ```

If you are using [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh) you can
just add the ```virtualenvwrapper``` plugin to your plugins list
(inside ```~/.zshrc```). This plugin will:
  - Loads Python's [virtualenvwrapper shell tools](http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html), and
  - Automatically activates virtualenv on cd into git repository with matching name

After installed, clone this repository locally, ```cd``` into it and create the
required virtualenv with the same name as the repository directory:

   ```shell
   $ mkvirtualenv "${PWD##*/}"
   ```

This will create the virtualenv and also activate it. Now we will install the 
project requirements on the virtualenv:

    ```shell
    $ pip3 install -r requirements.txt
    ```

The standard setup finishes here.

If you are using ```oh-my-zsh``` plugin then every time you enter on the project
directory the virtualenvironment will be automaticaly loaded. If you are using
bash, then you need to run the ```workon``` command to activate the environment:

    ```shell
    $ workon ofx-parser
    ```

See more virtualenvwrapper commands on:
http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html

## TDD (Test Driven Development)
The tests are run for each implemented version of the protocol. So, to run
the tests of a specific version use the following command from the project root
directory:

```shell
python3 -m unittest discover -s ofp/VERSION/tests/
```

To run all the tests, from all version, use the following command from the
project root directory:

```shell
python3 -m unittest discover
```