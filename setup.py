"""Setup script.

Run "python3 setup --help-commands" to list all available commands and their
descriptions.
"""
from abc import abstractmethod
# Disabling checks due to https://github.com/PyCQA/pylint/issues/73
# pylint: disable=import-error,no-name-in-module
from distutils.command.clean import clean
# pylint: enable=import-error,no-name-in-module
from subprocess import CalledProcessError, call, check_call

from setuptools import Command, find_packages, setup

from pyof import __version__


class SimpleCommand(Command):
    """Make Command implementation simpler."""

    user_options = []

    def __init__(self, *args, **kwargs):
        """Store arguments so it's possible to call other commands later."""
        super().__init__(*args, **kwargs)
        self.__args = args
        self.__kwargs = kwargs

    @abstractmethod
    def run(self):
        """Run when command is invoked.

        Use *call* instead of *check_call* to ignore failures.
        """
        pass

    def run_command(self, command_class):
        """Run another command with same __init__ arguments."""
        command_class(*self.__args, **self.__kwargs).run()

    def initialize_options(self):
        """Set defa ult values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass


class Cleaner(clean):
    """Custom clean command to tidy up the project root."""

    description = 'clean build, dist, pyc and egg from package and docs'

    def run(self):
        """Clean build, dist, pyc and egg from package and docs."""
        super().run()
        call('rm -vrf ./build ./dist ./*.pyc ./*.egg-info', shell=True)
        call('find . -name __pycache__ -type d | xargs rm -rf', shell=True)
        call('test -d docs && make -C docs/ clean', shell=True)


class TestCoverage(SimpleCommand):
    """Display test coverage."""

    description = 'run unit tests and display code coverage'

    def run(self):
        """Run unittest quietly and display coverage report."""
        cmd = 'coverage3 run setup.py test && coverage3 report'
        check_call(cmd, shell=True)


class DocTest(SimpleCommand):
    """Run documentation tests."""

    description = 'run documentation tests'

    def run(self):
        """Run doctests using Sphinx Makefile."""
        cmd = 'make -C docs/ default doctest'
        check_call(cmd, shell=True)


class CITest(SimpleCommand):
    """Run all CI tests."""

    description = 'run all CI tests: unit and doc tests, linter'

    def run(self):
        """Run unit tests with coverage, doc tests and linter."""
        for command in TestCoverage, DocTest, Linter:
            self.run_command(command)


class Linter(SimpleCommand):
    """Lint Python source code."""

    description = 'lint Python source code'

    def run(self):
        """Run yala."""
        print('Yala is running. It may take several seconds...')
        try:
            check_call('yala pyof setup.py', shell=True)
            print('No linter error found.')
        except CalledProcessError:
            print('Linter check failed. Fix the error(s) above and try again.')
            exit(-1)


setup(name='python-openflow',
      version=__version__,
      description='Library to parse and generate OpenFlow messages',
      url='http://github.com/kytos/python-openflow',
      author='Kytos Team',
      author_email='devel@lists.kytos.io',
      license='MIT',
      test_suite='tests',
      include_package_data=True,
      extras_require={
          'dev': [
              'coverage',
              'tox',
              'pip-tools',
              'yala',
          ],
      },
      packages=find_packages(exclude=['tests']),
      cmdclass={
          'ci': CITest,
          'clean': Cleaner,
          'coverage': TestCoverage,
          'doctest': DocTest,
          'lint': Linter
      },
      zip_safe=False,
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.6',
          'Topic :: System :: Networking',
          'Topic :: Software Development :: Libraries'
      ])
