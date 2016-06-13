import os
import sys
from setuptools import setup, find_packages, Command

SEP='<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>'


class Doctest(Command):
    if sys.argv[-1] == 'test':
        print(SEP)
        print("Running docs make and make doctest")
        os.system("make doctest -C docs/")
        print(SEP)


class Pep8Test(Command):
    if sys.argv[-1] == 'test':
        print("Running pep8 under source code folder")
        os.system("python setup.py pep8 --exclude '.eggs*'")
        print(SEP)

setup(name='Kytos OpenFlow Parser library',
      version='0.1',
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
