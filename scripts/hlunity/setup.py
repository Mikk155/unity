from setuptools import setup, find_packages

setup(
    name="hlunity",
    version="1.0",
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
    libraries=[ ]
)
