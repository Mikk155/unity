from setuptools import setup, find_packages
from os import getenv
from requests import get

PACKAGE_VERSION = getenv( "PACKAGE_VERSION" )

if not PACKAGE_VERSION or PACKAGE_VERSION == '':
    raise ValueError( f'Can not get PACKAGE_VERSION from enviroment variables {PACKAGE_VERSION}' )

proj_url = "https://pypi.org/pypi/hlunity/json"

response = get( proj_url )

#if response.status_code != 200:
#    print(f'Failed to get a response from ')
#    exit(1)

response.raise_for_status()

data = response.json()

versions = list( data[ 'releases' ].keys() )

latest_version = float( versions[ len( versions ) - 1 ] )

PACKAGE_VERSION = 1.6

if PACKAGE_VERSION <= latest_version:
    raise FileExistsError( f'Version can NOT update {PACKAGE_VERSION}, a newer version already exists ({latest_version})' )

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
