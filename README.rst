abracadabra: Sound recognition in Python
========================================

*abracadabra à la Shazam*

abracadabra is sound recogniser written in Python. It is an implementation of the Shazam paper: `An Industrial Strength Audio Search Algorithm <https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf>`_.

Read the `docs here <https://abracadabra.readthedocs.io/en/latest/>`_ or read `an explanation of how it works <https://www.cameronmacleod.com/blog/how-does-shazam-work>`_.


What can you use it for?
------------------------

abracadabra works like Shazam. You register songs in advance and then later you can use your computer's microphone to identify what song is playing. It could be used (as part of another system) to:

* Align multiple videos of the same event using the audio
* De-duplicate your music library


Installation
------------

First, clone or download this repository::

    git clone https://github.com/notexactlyawe/abracadabra.git

Next, install the dependencies abracadabra relies on. On Ubuntu you can install them with the following line::

    sudo apt-get install gcc portaudio19-dev python3-dev ffmpeg

Now you can use pip to install the project::

    cd abracadabra
    pip install .


Usage as a script
-----------------

Installing the project through pip will install the ``song_recogniser`` script. To see all the options you can pass to the script, run the following::

    song_recogniser --help

Below is an example of how you can use ``song_recogniser``::

    $ song_recogniser initialise
    Initialised DB
    $ song_recogniser register ~/Music/CoolArtist/AwesomeAlbum
    $ song_recogniser recognise --listen  # records a 10 second clip for recognition
    ALSA ...
    * recording
    * done recording
    ('CoolArtist', 'AwesomeAlbum', 'SweetTrack')


Usage as a library
------------------

You can use abracadabra as part of your own project by using it as a library. The main modules you'll be interested in are the `recognise <https://abracadabra.readthedocs.io/en/latest/source/abracadabra.html#abracadabra-recognise-module>`_ and `settings <https://abracadabra.readthedocs.io/en/latest/source/abracadabra.html#module-abracadabra.settings>`_ modules.

Most functions in the library are documented. If you want to use lower-level components in your project, please take a look at the `docs <https://abracadabra.readthedocs.io/>`_.


Issues and contributing
-----------------------

If you encounter an issue with abracadabra or have a suggestion for improving the project, please `create an issue <https://github.com/notexactlyawe/abracadabra/issues/new>`_!

Pull requests are welcome, but please create an issue first to discuss what you intend to do.


------------------------

This project is maintained by `Cameron MacLeod <https://www.cameronmacleod.com>`_.

------------------------
