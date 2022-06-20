High Level Api
###############
The high level API documented bellow, abstracts away repetitive tasks and information.

BucketFSFactory
---------------
Factory for creating bucket accessors (*BucketFSLocation*) or Fake/Mock accessors which can be used for testing.

.. literalinclude:: /examples/bucketfs_location.py
   :caption: Example: Create Bucket Accessor
   :lines: 1-2
   :language: python3

.. literalinclude:: /examples/bucketfs_location.py
   :caption: Example: Create Mock Bucket Accessor
   :lines: 1-2
   :language: python3

BucketFSLocation
----------------
Keeps track of connection information and provides access to specific bucket in a bucketfs.

.. literalinclude:: /examples/bucketfs_location.py
   :caption: Example
   :lines: 5-6
   :language: python3

