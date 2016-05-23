from setuptools import setup, find_packages

setup(name='Kytos OpenFlow Parser library',
      version='0.1',
      description='Library to parse and generate OpenFlow messages',
      url='http://github.com/kytos/python-openflow',
      author='Kytos Team',
      author_email='of-ng-dev@ncc.unesp.br',
      license='MIT',
      test_suite='tests',
      packages=find_packages(exclude=["tests", "*v0x02*"]),
      zip_safe=False)

