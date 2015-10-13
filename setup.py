"""Setup for fuzzybit module"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import setup


def readme():
    """Returns documentation"""
    with open('README.rst') as readme_file:
        return readme_file.read()


setup(name='fuzzybit',
      version='0.2.0',
      description='Fuzzy bit library',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Security',
          'Topic :: Utilities',
      ],
      keywords='fuzzy bit integer entropy',
      url='https://github.com/tmfink/fuzzybit',
      download_url='https://github.com/tmfink/fuzzybit/tarball/master',
      author='Travis Finkenauer',
      author_email='tmfink@umich.edu',
      license='GPLv3',
      packages=['fuzzybit'],
      install_requires=['six'],
      test_suite='fuzzybit.tests.test_fuzzybit',
      include_package_data=True,
      zip_safe=True)
