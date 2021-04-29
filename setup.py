"""Setup script.

Run "python3 setup --help-commands" to list all available commands and their
descriptions.
"""
import sys
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

    def run_command(self, command_class):
        """Run another command with same __init__ arguments."""
        command_class(*self.__args, **self.__kwargs).run()

    def initialize_options(self):
        """Set default values for options."""

    def finalize_options(self):
        """Post-process options."""


# pylint: disable=attribute-defined-outside-init, abstract-method
class TestCommand(Command):
    """Test tags decorators."""

    user_options = [
        ('size=', None, 'Specify the size of tests to be executed.'),
        ('type=', None, 'Specify the type of tests to be executed.'),
    ]

    sizes = ('small', 'medium', 'large', 'all')
    types = ('unit', 'integration', 'e2e')

    def get_args(self):
        """Return args to be used in test command."""
        return '--size %s --type %s' % (self.size, self.type)

    def initialize_options(self):
        """Set default size and type args."""
        self.size = 'all'
        self.type = 'unit'

    def finalize_options(self):
        """Post-process."""
        try:
            assert self.size in self.sizes, ('ERROR: Invalid size:'
                                             f':{self.size}')
            assert self.type in self.types, ('ERROR: Invalid type:'
                                             f':{self.type}')
        except AssertionError as exc:
            print(exc)
            sys.exit(-1)


class Cleaner(clean):
    """Custom clean command to tidy up the project root."""

    description = 'clean build, dist, pyc and egg from package and docs'

    def run(self):
        """Clean build, dist, pyc and egg from package and docs."""
        super().run()
        call('rm -vrf ./build ./dist ./*.pyc ./*.egg-info', shell=True)
        call('find . -name __pycache__ -type d | xargs rm -rf', shell=True)
        call('test -d docs && make -C docs/ clean', shell=True)


class Test(TestCommand):
    """Run all tests."""

    description = 'run tests and display results'

    def get_args(self):
        """Return args to be used in test command."""
        markers = self.size
        if markers == "small":
            markers = 'not medium and not large'
        size_args = "" if self.size == "all" else "-m '%s'" % markers
        return '--addopts="tests/%s %s"' % (self.type, size_args)

    def run(self):
        """Run tests."""
        cmd = 'python setup.py pytest %s' % self.get_args()
        try:
            check_call(cmd, shell=True)
        except CalledProcessError as exc:
            print(exc)
            print('Unit tests failed. Fix the error(s) above and try again.')
            sys.exit(-1)


class TestCoverage(Test):
    """Display test coverage."""

    description = 'run tests and display code coverage'

    def run(self):
        """Run tests quietly and display coverage report."""
        cmd = 'coverage3 run setup.py pytest %s' % self.get_args()
        cmd += '&& coverage3 report'
        try:
            check_call(cmd, shell=True)
        except CalledProcessError as exc:
            print(exc)
            print('Coverage tests failed. Fix the errors above and try again.')
            sys.exit(-1)


class DocTest(SimpleCommand):
    """Run documentation tests."""

    description = 'run documentation tests'

    def run(self):
        """Run doctests using Sphinx Makefile."""
        cmd = 'make -C docs/ default doctest'
        check_call(cmd, shell=True)


class Linter(SimpleCommand):
    """Lint Python source code."""

    description = 'Lint Python source code'

    def run(self):
        """Run yala."""
        print('Yala is running. It may take several seconds...')
        try:
            check_call('yala pyof setup.py', shell=True)
            print('No linter error found.')
        except CalledProcessError:
            print('Linter check failed. Fix the error(s) above and try again.')
            sys.exit(-1)


class CITest(TestCommand):
    """Run all CI tests."""

    description = 'run all CI tests: unit and doc tests, linter'

    def run(self):
        """Run unit tests with coverage, doc tests and linter."""
        coverage_cmd = 'python setup.py coverage %s' % self.get_args()
        doctest_cmd = 'python setup.py doctest'
        lint_cmd = 'python setup.py lint'
        cmd = '%s && %s && %s' % (coverage_cmd, doctest_cmd, lint_cmd)
        check_call(cmd, shell=True)


NEEDS_PYTEST = {'pytest', 'test', 'coverage'}.intersection(sys.argv)
PYTEST_RUNNER = ['pytest-runner'] if NEEDS_PYTEST else []

setup(name='python-openflow',
      version=__version__,
      description='Library to parse and generate OpenFlow messages',
      long_description=open("README.rst", "r").read(),
      url='http://github.com/kytos/python-openflow',
      author='Kytos Team',
      author_email='devel@lists.kytos.io',
      license='MIT',
      test_suite='tests',
      include_package_data=True,
      setup_requires=PYTEST_RUNNER,
      tests_require=['pytest'],
      extras_require={'dev': ['pip-tools >= 2.0',
                              'coverage', 'pytest', 'yala', 'tox']},
      packages=find_packages(exclude=['tests']),
      cmdclass={
          'ci': CITest,
          'clean': Cleaner,
          'coverage': TestCoverage,
          'doctest': DocTest,
          'lint': Linter,
          'test': Test
      },
      zip_safe=False,
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: System :: Networking',
          'Topic :: Software Development :: Libraries'
      ])
