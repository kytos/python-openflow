"""Setup script.

Run "python3 setup --help-commands" to list all available commands and their
descriptions.
"""
import sys
from abc import abstractmethod
from subprocess import CalledProcessError, call, check_call

from setuptools import Command, find_packages, setup
from setuptools.command.test import test as TestCommand

from pyof import __version__


class SimpleCommand(Command):
    """Make Command implementation simpler."""

    user_options = []

    @abstractmethod
    def run(self):
        """Run when command is invoked.

        Use *call* instead of *check_call* to ignore failures.
        """
        pass

    def initialize_options(self):
        """Set defa ult values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass


class Linter(SimpleCommand):
    """Code linters."""

    description = 'run Pylama on Python files'

    def run(self):
        """Run linter."""
        self.lint()

    @staticmethod
    def lint():
        """Run pylama and radon."""
        files = 'tests setup.py pyof'
        print('Pylama is running. It may take several seconds...')
        cmd = 'pylama {}'.format(files)
        try:
            check_call(cmd, shell=True)
        except CalledProcessError as e:
            print('FAILED: please, fix the error(s) above.')
            sys.exit(e.returncode)


class Cleaner(SimpleCommand):
    """Custom clean command to tidy up the project root."""

    description = 'clean build, dist, pyc and egg from package and docs'

    def run(self):
        """Clean build, dist, pyc and egg from package and docs."""
        call('rm -vrf ./build ./dist ./*.pyc ./*.egg-info', shell=True)
        call('cd docs; make clean', shell=True)


class Test(TestCommand):
    """Run doctest and linter besides tests/*."""

    def run(self):
        """First, tests/*."""
        super().run()
        print('Running examples in documentation')
        check_call('make doctest -C docs/', shell=True)
        Linter.lint()


requirements = [i.strip() for i in open("requirements.txt").readlines()]

setup(name='python-openflow',
      version=__version__,
      description='Library to parse and generate OpenFlow messages',
      url='http://github.com/kytos/python-openflow',
      author='Kytos Team',
      author_email='of-ng-dev@ncc.unesp.br',
      license='MIT',
      test_suite='tests',
      include_package_data=True,
      install_requires=requirements,
      packages=find_packages(exclude=['tests', '*v0x02*']),
      cmdclass={
          'lint': Linter,
          'clean': Cleaner,
          'test': Test
      },
      zip_safe=False)
