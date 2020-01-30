"""Python Client for EBUS daemon."""

from os import path

from setuptools import setup


def _read_metainfo(filepath):
    import re

    pat = re.compile(r"__(?P<name>[a-z_]+)__ = (?P<expr>.*)")
    metainfo = {}
    with open(filepath) as fh:
        for line in fh:
            if isinstance(line, bytes):
                line = line.decode("utf-8")
            match = pat.match(line)
            if match:
                metainfo[match.group("name")] = eval(match.group("expr"))
    return metainfo


config = _read_metainfo("ebus/__init__.py")
config["name"] = "ebus"
config["license"] = "Apache 2.0"
config["classifiers"] = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
]
config["keywords"] = "ebus, ebusd, ebus client"
config["packages"] = ["ebus"]
config["extras_require"] = {
    "test": ["coverage"],
}
config["tests_require"] = ["nose"]
config["test_suite"] = "nose.collector"

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    config["long_description"] = f.read()

setup(**config)
