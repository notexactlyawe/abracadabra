Documentation
=============

Pre-requisites
--------------

The abracadabra docs are written using `Sphinx <https://www.sphinx-doc.org>`_. Everything you need to work on the docs is described in ``docs/requirements.txt``.

.. code-block:: bash

   cd docs
   virtualenv -p python3 venv
   source venv/bin/activate
   pip install -r requirements.txt


Building the docs
-----------------

The docs come with a Makefile that builds the docs for you. The easiest way to get started writing the docs is to run the ``livehtml`` command.

.. code-block:: bash

   make livehtml


This will start a live-reloading server that is accessible from `localhost:8000 <http://localhost:8000>`_.
