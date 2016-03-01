Sound recogniser
================

Mostly to see whether it's possible, this is a project to identify sounds from a finite set. The current plan is to divide it into the following modules:

Sound recogniser
Sound storage
Sound classifier

The classifying of tracks will require performing a fourier on each time interval (to be decided) in the track and identifying amplitude peaks in different sections of the resulting transform.

Fingerprint block diagram
-------------------------
![Fingerprinting](fingerprint.png "Fingerprinting")

This is an idea coming from the talk Over The Air Identification at FOSDEM 2016.
