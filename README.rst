#####################
BucketFS Utils Python
#####################

********
Overview
********

This project provides a python library for accessing the Exasol BucketFS system.
It provides functions to upload and download files to and from the BucketFS.

In a Nutshell
=============

Prerequisites
-------------

- Python 3.8+

Installation
-------------

Install the package from Github via `pip`::

    pip install -e git://github.com/exasol/bucketfs-utils-python.git@{tag name}#egg=exasol-bucketfs-utils-python

Documentation
-------------

`Documentation for the latest release <https://exasol.github.io/bucketfs-utils-python/main>`_ is hosted on the Github Pages of this project.

Features
========

* Download or upload files from/to the Exasol BucketFS
* Supported sources and targets for the uploads and downloads:

  * Files on the local Filesystem
  * Python file objects
  * Python Strings
  * Python objects ((De-)Serialization with [Joblib](https://joblib.readthedocs.io/en/latest/persistence.html))

* Loading an artefact from a public Github Release into the BucketFS
