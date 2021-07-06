import codecs
import os.path

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements/release.txt") as f:
    requirements = f.read().splitlines()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="mnqueues",
    version=get_version("mnqueues/__init__.py"),
    author="amor71",
    author_email="amor71@sgeltd.com",
    description="Monitored Multiprocessing Queues in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amor71/mnqueues",
    license="MIT",
    install_requires=requirements,
    data_files=[("mnqueues", ["requirements/release.txt"])],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    scripts=[],
)
