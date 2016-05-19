Software Architecture Specification
===================================

1. Introduction
---------------

This document outlines how abracadbra is to be built and how it will be split up into different modules. This document originally came from [this GitHub repo](https://github.com/notexactlyawe/abracadabra).

Abracadabra is a Shazam-style music identification service buit in Python mostly for personal interest. It will be demoed at EuroPython 2016 and was inspired by [this talk] from FOSDEM 2016.

2. High Level Overview
----------------------

The basic data flow through the application will be as follows:

### Audio > Normaliser > Fingerprinter > (Storage | Search > Matching metadata) ###

**Normaliser** will be a module that takes audio in various formats and converts it into a single format that can be used by the fingerprinter.

**Fingerprinter** will be the real beef of the application. It will take in audio and produce fingerprints of it based off of these papers <sup>[1](#shazam)</sup> <sup>[2](#cvfmi)</sup> <sup>[3](#specfing)</sup>.

**Storage/Search** will be a module that acts as an interface to a database. It will be what allows for fast retrieval with large amounts of records.

3. Detailed Modules
-------------------
### 3.1 Normaliser ###
The normaliser will consist of a main module that identifies the type of input and separate modules for each type that can be called. (eg mp3, aac, flac etc).
Each module will know its own type and how to convert it to the base type that will be used.

Normaliser

 | - identifier.py

 | - mp3.py

 | - aac.py

etc

### 3.2 Fingerprinter ###
Fingerprinter will be accessible through a high-level interface where you pass it some audio and it will return you overlapping fingerprints.

### 3.3 Storage/Search ###
Storage/search is as of yet undefined. I will almost certainly use some third party system such as elastic search in combination with some main data store.

<a name="shazam">1</a>: [An Industrial-Strength Audio Search Alogrithm](http://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf)

<a name="cvfmi">2</a>: [Computer Vision for Music Identification](http://www.cs.cmu.edu/~yke/musicretrieval/cvpr2005-mr.pdf)

<a name="specfing">3</a>: [Improvement of Spectral Fingerprint for Audio Content Recognition](http://onlinepresent.org/proceedings/vol122_2016/47.pdf)
