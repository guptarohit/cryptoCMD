#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree
from setuptools import setup, find_packages, Command

# Package meta-data.
NAME = "cryptocmd"
DESCRIPTION = "Cryptocurrency historical market price data scrapper."
URL = "https://github.com/guptarohit/cryptocmd"
AUTHOR = "Rohit Gupta"

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = "\n" + f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPi via Twine...")
        os.system("twine upload dist/*")

        sys.exit()


about = {}
with io.open(os.path.join(here, "cryptocmd", "__version__.py"), encoding="utf-8") as f:
    exec(f.read(), about)

setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    install_requires=["requests", "pyquery", "tablib==0.11.4"],
    include_package_data=True,
    extras_require={"pandas": ["pandas"]},
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD License",
    ],
    # $ setup.py publish support.
    cmdclass={"upload": UploadCommand},
)
