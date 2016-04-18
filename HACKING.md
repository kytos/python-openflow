Before reading this file, please read the [CONTRIBUTE](CONTRIBUTE.md) file, that
contains the main guidelines of the project.

## Development Environment setup

This project is based on python (version 3.5).

During the devlopment of the project what you need is to add the ofp folder,
inside this repository, to your PYTHONPATH environment variable. For that,
you have to execute the following on the command line (being on this current
folder):

```shell
export PYTHONPATH=`pwd`/ofp:$PYTHONPATH
```

Remember that everytime you start a new shell instance you will have to
repeat the command above, since this is an environment variable.

### Virtualenv

To make things easier and avoid the need of redo the export all the time,
we recommend that you install python `virtualenv`. This is not necessary, but
recommended. With `virtualenv` you can install the required and recommended
python libraries without messing up with your system. To install them run
the following commands:

   ```shell
   $ sudo apt install python3-pip
   $ sudo pip3 install virtualenv virtualenvwrapper
   ```
   
If you are working with **bash**, add the following lines on your
`~/.bash_profile` or `~/.bashrc` to setup `virtualenvwrapper`:

   ```shell
   export WORKON_HOME=~/.virtualenvs
   source /usr/local/bin/virtualenvwrapper.sh
   ```

If you are using **[oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh)** you
can just add the `virtualenvwrapper` plugin to your plugins list
(inside `~/.zshrc`). This plugin will:
  - Loads Python's [virtualenvwrapper shell tools](http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html), and
  - Automatically activates virtualenv on cd into git repository with matching name

We also recommend adding the bellow code to your `~/.virtualenvs/postmkvirtualenv` file:
```shell
echo '_OLD_PYTHONPATH="$PYTHONPATH"' >> ~/.virtualenvs/"${PWD##*/}"/bin/postactivate
echo "PYTHONPATH="'"'$(pwd)'"' >> ~/.virtualenvs/"${PWD##*/}"/bin/postactivate
echo 'PYTHONPATH="$_OLD_PYTHONPATH"' >> ~/.virtualenvs/"${PWD##*/}"/bin/postdeactivate
```

This will change the PYTHONPATH environment variable to your projects path when
the virtualenv is activated.

After installed, clone this repository locally, `cd` into it and create the
required virtualenv with the same name as the repository directory:

```shell
$ mkvirtualenv "${PWD##*/}" -r requirements.txt
```

This will create the virtualenv with all project requirements and also activate it.

The standard setup finishes here.

If you are using `oh-my-zsh` plugin then every time you enter on the project
directory the virtualenvironment will be automaticaly loaded. If you are using
bash, then you need to run the `workon` command to activate the environment:

```shell
workon ofx-parser
```

See more virtualenvwrapper commands on:
http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html

#### Virtualenv Extras

if you want to show the current activated virtualenv on the right side of your
shell, add the following code to your `~/.virtualenvs/postactivate` file:

```shell
PS1="$_OLD_VIRTUAL_PS1"
_OLD_RPROMPT="$RPROMPT"
RPROMPT="%{${fg_bold[white]}%}(env: %{${fg[white]}%}`basename \"$VIRTUAL_ENV\"`%{${fg_bold[white]}%})%{${reset_color}%} $RPROMPT"
```

Change the colors to your own preferences.

and also this code to your `~/.virtualenvs/postdeactivate` file:

```shell
RPROMPT="$_OLD_RPROMPT"
```

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
