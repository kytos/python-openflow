#! /usr/bin/env python3
"""Create a new OpenFlow version and import old implementation.

The implementation of a new OpenFlow specification starts by importing all
the previous version's code. Then, it is modified to match the new version.
This script helps to create the necessary folders and files for the new
version, including import statements.
"""
import os
import sys
from pathlib import Path
from subprocess import PIPE, run


def shell(cmd):
    """Run a shell command or only print it for debuggin."""
    if DRY_RUN:
        print(cmd)
    else:
        run(cmd, shell=True, check=True)


def shell_stdout(cmd):
    """Run a shell command and return its output as a string."""
    output = run(cmd, shell=True, stdout=PIPE, check=True).stdout
    return output.decode(encoding='ascii')


def list_classes(file):
    """Parse all class names in a file and return as a list."""
    cmd = r"grep -o '^class [[:alnum:]]\+' {} | cut -d' ' -f2".format(file)
    classes = shell_stdout(cmd).split()
    return sorted(classes)


def get_docstring(file):
    """Return the module docstring of a file."""
    cmd = 'perl -0777 -e \'$_=<>; print /(^""".+?"""$)/ms;\' {}'.format(file)
    return shell_stdout(cmd)


def get_new_file(old_file):
    """Replace the old_version in filename by the new version."""
    filename = str(old_file).replace(old_version, new_version)
    return Path(filename)


def check_parent(path):
    """If parent folder doesn't exist, create it."""
    parent = path.parent
    if not parent.exists():
        if DRY_RUN:
            print('mkdir -p {}'.format(parent))
        else:
            parent.mkdir(parents=True)


def copy_init(old_file):
    """Copy __init__.py from old version to the new version.

    Args:
        old_file (Path): source file.
    """
    new_file = get_new_file(old_file)
    if new_file.exists():
        print('Warning: will not override {}.'.format(new_file))
    else:
        check_parent(new_file)
        shell('cp {} {}'.format(old_file, new_file))


def path2module(path):
    """Return the dotted module for the given path."""
    filename = str(path)
    begin = filename.find('pyof/v')
    module = filename[begin:].replace('/', '.')
    if filename.endswith('.py'):
        return module[:-3]


def create_module_file(old_file):
    """Create the new version py file, add docstring and import statement."""
    new_file = get_new_file(old_file)
    if new_file.exists():
        print('Warning: will not override {}.'.format(new_file))
    else:
        check_parent(new_file)
        shell('touch ' + str(new_file))
        classes = list_classes(old_file)
        if classes:
            module = path2module(old_file)
            # Add module docstring
            docstring = get_docstring(old_file)
            cmd = "echo '{}' > {}".format(docstring, new_file)
            shell(cmd)
            # Add import statement
            imp = 'from {} import {}'.format(module, ', '.join(classes))
            cmd = "echo '{}' >> {}".format(imp, new_file)
            shell(cmd)
            # Format import statement with isort
            cmd = 'isort {}'.format(new_file)
            shell(cmd)


def create_module(module):
    """Create the new version of the module."""
    if str(module).endswith('__init__.py'):
        copy_init(module)
    else:
        create_module_file(module)


def should_skip(path):
    """Return whether to skip this path."""
    path_str = str(path)
    return '__pycache__' in path_str or path_str[-4:] == '.pyc'


def dfs(path):
    """Depth-first search."""
    if path.is_file():
        if not should_skip(path):
            create_module(path)
    else:
        for child in path.iterdir():
            create_module(child)


if __name__ == '__main__':
    # Print help if no arguments are given
    if len(sys.argv) < 3:
        exe = sys.argv[0]
        print('  Usage: {} old_version new_version [--dry-run]'.format(exe))
        print('Example: {} v0x01 v0x02 [--dry-run]'.format(exe))

    DRY_RUN = len(sys.argv) > 3

    old_version = sys.argv[1]
    new_version = sys.argv[2]
    root = Path(os.path.dirname(__file__)) / '..' / 'pyof'
    old_root = root / old_version
    new_root = root / new_version

    # Test old_version existence
    if not old_root.is_dir():
        raise Exception('Folder {} was not found.'.format(old_root))

    dfs(old_root)
