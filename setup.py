"""Setup script.

Run "python3 setup --help-commands" to list all available commands and their
descriptions.
"""
import sys
from subprocess import call

from setuptools import Command, find_packages, setup


class Doctest(Command):
    """Run Sphinx doctest."""

    if sys.argv[-1] == 'test':
        print('Running examples in documentation')
        call('make doctest -C docs/', shell=True)


class Linter(Command):
    """Run several code linters."""

    description = 'Run many code linters. It may take a while'
    user_options = []

    def __init__(self, *args, **kwargs):
        """Define linters and a message about them."""
        super().__init__(*args, **kwargs)
        self.linters = ['pep257', 'pyflakes', 'mccabe', 'isort', 'pep8',
                        'pylint']
        self.extra_msg = 'It may take a while. For a faster version (and ' \
                         'less checks), run "quick_lint".'

    def initialize_options(self):
        """For now, options are ignored."""
        pass

    def finalize_options(self):
        """For now, options are ignored."""
        pass

    def run(self):
        """Run pylama and radon."""
        files = 'tests setup.py pyof'
        print('running pylama with {}. {}'.format(', '.join(self.linters),
                                                  self.extra_msg))
        cmd = 'pylama -l {} {}'.format(','.join(self.linters), files)
        call(cmd, shell=True)
        print('Low grades (<= C) for Cyclomatic Complexity:')
        call('radon cc --min=C ' + files, shell=True)
        print('Low grades (<= C) for Maintainability Index:')
        call('radon mi --min=C ' + files, shell=True)


class FastLinter(Linter):
    """Same as Linter, but without the slow pylint"""

    description = 'Same as "lint", but much faster (no pylama_pylint).'

    def __init__(self, *args, **kwargs):
        """Remove slow linters and redefine the message about the rest."""
        super().__init__(*args, **kwargs)
        self.linters.remove('pylint')
        self.extra_msg = 'This a faster version of "lint", without pylint. ' \
                         'Run the slower "lint" after solving these issues:'


setup(name='python-openflow',
      version='1.1.0a0',
      description='Library to parse and generate OpenFlow messages',
      url='http://github.com/kytos/python-openflow',
      author='Kytos Team',
      author_email='of-ng-dev@ncc.unesp.br',
      license='MIT',
      test_suite='tests',
      packages=find_packages(exclude=['tests', '*v0x02*']),
      cmdclass={
          'lint': Linter,
          'quick_lint': FastLinter
      },
      zip_safe=False)
