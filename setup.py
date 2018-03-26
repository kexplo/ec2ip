# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


def requirements(filename):
    """Reads requirements from a file."""
    with open(filename) as f:
        return [x.strip() for x in f.readlines() if x.strip()]


setup(name='ec2ip',
      version='0.1.0',
      description='ec2ip',
      author='',
      author_email='',
      url='',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['ec2ip = ec2ip.__main__:cli']
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities',
      ],
      install_requires=requirements('requirements.txt'),
      # tests_require=requirements('tests/requirements.txt'),
      )
