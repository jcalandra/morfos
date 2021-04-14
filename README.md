Cognitive Algorithm and its Musical Applications


- **data/**
    Contains examples of audio files in .wav.
- **lib/vmo/master/**
    Contains files that we need from the Variable Markov Oracle library developped by C. Wang: 
    https://github.com/wangsix/vmo.
- **src/**
    Contains the main files for the application.
    - **generic/**
        Necessary files for every versions of the cognitive algorithm.
    - **midi_version/**
        Necessary files for the MIDI version of the cognitive algorithm. Not updated. This folder will be updated in order to obtain 
        formal diagrams from MIDI data, using the Multi-Scale Oracle (MSO).
    - **oracle_version/**
        Necessary files for the MSO version of the cognitive algorithm.
    - **standard_version/**
        Necessary files for a standard version without MSO. The standard version is not updated and might be deleted.

- **tests/**
    Contains some tests.

First you should apply the parameters you want in `parameters.py`, then you can run:
 - `main_mso.py` to obtain formal diagrams from signal.
 - `char_main.py` to obtain formal diagrams from character strings.
