"""Setup script.

Run "python3 setup --help-commands" to list all available commands and their
descriptions.
"""
import sys
from distutils.command.build import build
from subprocess import call, check_call

from setuptools import find_packages, setup

from pyof import __version__


class Linter(build):
    """Code linters."""

    def run(self):
        """Run pylama and radon."""
        files = 'tests setup.py pyof'
        print('Running pylama. It may take a while...')
        cmd = 'pylama {}'.format(files)
        call(cmd, shell=True)
        print('Low grades (<= C) for Maintainability Index:')
        call('radon mi --min=C ' + files, shell=True)


class Cleaner(build):
    """Custom clean command to tidy up the project root."""

    def run(self):
        """Clean build, dist, pyc and egg from package and docs."""
        call('rm -vrf ./build ./dist ./*.pyc ./*.egg-info', shell=True)
        call('cd docs; make clean', shell=True)


class Doctest(build):
    """Run Sphinx doctest during test."""

    if sys.argv[-1] == 'test':
        print('Running examples in documentation')
        check_call('make doctest -C docs/', shell=True)


setup(name='python-openflow',
      version=__version__,
      description='Library to parse and generate OpenFlow messages',
      url='http://github.com/kytos/python-openflow',
      author='Kytos Team',
      author_email='of-ng-dev@ncc.unesp.br',
      license='MIT',
      test_suite='tests',
      packages=find_packages(exclude=['tests', '*v0x02*', '*v0x04*']),
      cmdclass={
          'lint': Linter,
          'clean': Cleaner,
      },
      zip_safe=False)
