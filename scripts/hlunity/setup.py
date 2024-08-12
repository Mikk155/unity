from setuptools import setup, find_packages
from os import getenv

PACKAGE_VERSION = getenv( "PACKAGE_VERSION" )

if not PACKAGE_VERSION or PACKAGE_VERSION == '':
    raise ValueError( f'Can not get PACKAGE_VERSION from enviroment variables {PACKAGE_VERSION}')

setup(
    name="hlunity",
    version=f"{PACKAGE_VERSION}",
    author="Mikk155",
    author_email="",
    description="Utilities for scripting in my projects, almost is goldsource-related",
    long_description="Convenience utilities for mod porting into Half-Life: Unity",
    long_description_content_type="text/markdown",
    url="https://github.com/Mikk155/unity/scripts/hlunity",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=[
        "requests"
    ],
)
