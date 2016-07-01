import os
import sys
from setuptools import setup, find_packages, Command


class Doctest(Command):
    if sys.argv[-1] == 'test':
        print("Running docs make and make doctest")
        os.system("make doctest -C docs/")


class Pep8Test(Command):
    if sys.argv[-1] == 'test':
        print("Running pep8 under source code folder")
        os.system("python3 setup.py pep8 --exclude '.eggs*'")

setup(name='python-openflow',
      version='1.1.0-alpha',
      description='Library to parse and generate OpenFlow messages',
      url='http://github.com/kytos/python-openflow',
      author='Kytos Team',
      author_email='of-ng-dev@ncc.unesp.br',
      license='MIT',
      test_suite='tests',
      packages=find_packages(exclude=["tests", "*v0x02*"]),
      setup_requires=['setuptools-pep8'],
      cmdclass={
        'doctests': Doctest
      },
      zip_safe=False)
