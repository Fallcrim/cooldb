import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '1.0.1'
DESCRIPTION = 'A simple database handler for SQLite3'
LONG_DESCRIPTION = open(os.path.join(here, 'README.md')).read()

# Setting up
setup(
    name="cooldb",
    version=VERSION,
    author="Fallcrim",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'db', 'database', 'wrapper', 'sqlite3'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
