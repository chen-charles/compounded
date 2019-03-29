import setuptools
import re
import os
import codecs

with open("README.md", "r") as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="compounded",
    version=find_version("compounded", "__init__.py"),
    author="Jianye Chen",
    author_email="chen-charles@users.noreply.github.com",
    description="Compounds methods with base classes'",
    python_requires='>=3.3.*, <4',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chen-charles/compounded",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
