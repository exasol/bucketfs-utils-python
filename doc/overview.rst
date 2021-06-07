********
Overview
********

This project provides a python library for the Exasol BucketFS system.

In a Nutshell
=============

Prerequisites
-------------

- Python 3.6+

Installation
-------------

Install the package from Github via `pip`:

```
pip install -e git://github.com/exasol/bucketfs-utils-python.git@{tag name}#egg=exasol-bucketfs-utils-python
```

Features
========

* Object-based specification of BucketFS connection information
* Download into or upload from files, file objects, string and objects ((De-)Serialization with [Joblib](https://joblib.readthedocs.io/en/latest/persistence.html))
* Loading files directly from Github Releases
