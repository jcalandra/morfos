Cognitive Algorithm and its Musical Applications


- **data/**
    Contains examples of audio files in .wav.
- **lib/vmo/master/**
    Contains files that we need from the Variable Markov Oracle library developped by C. Wang: 
    https://github.com/wangsix/vmo.
- **src/**
    Contains the main files for the application.
    - **class_implementation/**
        This folder contains a new implementation of the cognitive algorithm using Classes and MSO.
        It aims at integrating signal at every level of hyerarchy and will be the only implementation in few weeks (still bugged for now).
    - **compression/**
        This folder contains encoding and decoding algorithms to study the interest of the cognitive algorithm for compression.
    - **generic/**
        Necessary files for every versions of the cognitive algorithm.
        This folder contains generic functions for data analysis, discovery front computation, formal diagram display and similarity computation.
    - **midi_version/**
        Necessary files for the MIDI version of the cognitive algorithm. Not updated. This folder will be updated in order to obtain 
        formal diagrams from MIDI data, using the Multi-Scale Oracle (MSO).
    - **oracle_version/**
        Necessary files for the MSO (Multi-Scale Oracle) version of the cognitive algorithm. It also implement a sort of polyphonic representation that will be merged as soon as possible with the Class version using signal at every levels.
    - **standard_version/**
        Necessary files for a standard version without MSO. The standard version is not updated and might be deleted.

- **tests/**
    Contains some tests.

First you should apply the parameters you want in `parameters.py`, then you can run:
 - `main_mso.py` to obtain formal diagrams from signal.
 - `main_mso_char.py` to obtain formal diagrams from character strings.
