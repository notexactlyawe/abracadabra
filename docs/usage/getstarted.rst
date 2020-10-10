Getting Started
===============

Installation
------------

First, create a virtual environment to install the dependencies and activate it:

.. code-block:: bash

   virtualenv -p python3 venv
   source venv/bin/activate


Next, install the pre-requisites for the Python packages. On Ubuntu, you can do this using:

.. code-block:: bash

   sudo apt-get install gcc portaudio19-dev python3-dev ffmpeg

Now install the project with:

.. code-block:: bash

   pip install .

If you have problems with dependency clashes, then try running the following:

.. code-block:: bash

   pip install -r requirements.txt
   pip install .

``requirements.txt`` contains a set of dependencies that are known to work together.

Basic usage
-----------

abracadabra is best used as a library in other projects, but a simple script for song recognition is included. Once you've installed abracadabra, then the script will be available by running the following command:

.. code-block:: bash

   song_recogniser --help

``song_recogniser`` provides three commands that you can use.

* ``initialise``: Creates the database in which fingerprints are stored.
* ``register``: Takes a file or a directory and registers it to the database.
* ``recognise``: Recognises a song. Takes a filename, or listens using your computer's microphone.

Below is an example where ``song_recogniser`` is used:

.. code-block:: bash

   $ song_recogniser initialise
   Initialised DB
   $ song_recogniser register ~/Music/CoolArtist/AwesomeAlbum
   $ song_recogniser recognise --listen  # records a 10 second clip for recognition
   ALSA ...
   * recording
   * done recording
   ('CoolArtist', 'AwesomeAlbum', 'SweetTrack')

The source code for this simple application is under ``abracadbra/scripts/song_recogniser.py``.
