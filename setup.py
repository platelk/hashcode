from setuptools import setup, find_packages

setup(
    name="hashcode",
    version="0.1",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    packages=find_packages(),
)
