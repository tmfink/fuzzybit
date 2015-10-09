"""Setup for fuzzybit module"""


from setuptools import setup


def readme():
    """Returns documentation"""
    with open('README.rst') as readme_file:
        return readme_file.read()


setup(name='fuzzybit',
      version='0.1.1',
      description='Fuzzy bit library',
      long_description=readme(),
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 2.7',
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
      test_suite='fuzzybit.tests.test_fuzzybit',
      include_package_data=True,
      zip_safe=True)
