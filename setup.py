"""Setup script.

Run "python3 setup --help-commands" to list all available commands and their
descriptions.
"""
from abc import abstractmethod
# Disabling checks due to https://github.com/PyCQA/pylint/issues/73
from distutils.command.clean import clean  # pylint: disable=E0401,E0611
from os import path
from subprocess import call

from setuptools import Command, find_packages, setup

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
        cmd = 'coverage3 run -m unittest discover -qs tests' \
              ' && coverage3 report'
        call(cmd, shell=True)


class DocTest(SimpleCommand):
    """Run documentation tests."""

    description = 'run documentation tests'

    def run(self):
        """Run doctests using Sphinx Makefile."""
        cmd = 'make -C docs/ doctest'
        call(cmd, shell=True)


class Linter(SimpleCommand):
    """Lint Python source code."""

    description = 'lint Python source code'

    def run(self):
        """Run pylama."""
        print('Running pylama. This may take several seconds...')
        cmd = 'pylama tests setup.py pyof'
        call(cmd, shell=True)


def read_packages(filename):
    """Return list of packages from a file with requirements.

    Remove in-line comments.
    """
    filename = f'requirements/{filename}'
    print(filename)
    if not path.exists(filename):
        return []
    with open(filename) as lines:
        return [line.split()[0] for line in lines if not line.startswith('#')]


INSTALL_REQUIRES = {'install': read_packages('install.txt')}.values()
EXTRA_REQUIRES = {k: read_packages(filename) for k, filename in {
    'docs': 'docs.txt',
    'dev': 'dev.txt'}.items()}

setup(name='python-openflow',
      version=__version__,
      description='Library to parse and generate OpenFlow messages',
      url='http://github.com/kytos/python-openflow',
      author='Kytos Team',
      author_email='devel@lists.kytos.io',
      license='MIT',
      test_suite='tests',
      include_package_data=True,
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRA_REQUIRES,
      packages=find_packages(exclude=['tests']),
      cmdclass={
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
