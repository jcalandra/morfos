Cognitive Algorithm and its Musical Applications


- **data/**
    Contains examples of audio files in .wav.
- **lib/vmo/master/**
    Contains files that we need from the Variable Markov Oracle library developped by C. Wang: 
    https://github.com/wangsix/vmo.
- **src/**
    Contains the main files for the application.
    MORFOS is implemented in two versions 1.0 and 2.0 
    - **version1/**
    The version 1.0 is the version implemented until july 2023. In this version, objects are represented by audio at 
    level 0 and symbols at superior level. This version is the most stable version for now.
        - **compression/**
            This folder contains encoding and decoding algorithms to study the interest of the cognitive algorithm for 
            compression.
        - **generic/**
            Necessary files for every versions of the cognitive algorithm.
            This folder contains generic functions for data analysis, discovery front computation, formal diagram 
            display and similarity computation.
        - **midi_version/**
            Necessary files for the MIDI version of the cognitive algorithm. Not updated. This folder will be updated 
            in order to obtain formal diagrams from MIDI data, using the Multi-Scale Oracle (MSO).
        - **oracle_version/**
            Necessary files for the MSO (Multi-Scale Oracle) version of the cognitive algorithm. It also implement a 
            sort of polyphonic representation.
        - **standard_version/**
            Necessary files for a standard version without MSO. The standard version is not updated and will be deleted.
    - **version2/**
    The version 2.0 is a new implementation started from july 2023. The architecture is modular and the classification 
    test and the segmentation test of the cognitive algorithm are inverted. The objects are represented by audio and
    symbols at every levels. This version still need some debugs.
        - **core/**
        This folder contain the modules that are the core of the software and are aimed to be modified by the main 
        developers of MORFOS. It contains the modules for the algorithm, the data structure (MSO), the parameters and
        the 2D visualisation.
        - **criterias/**
        Contains the modules that might be completed with external modules. The three folders are pre-computing
        criterias, classification criterias and segmentation criterias.
        - **others/**
        Other features such as cost and phases computation.

- **tests/**
    Contains some tests.

In the version you want to try:
First you should apply the parameters you want in `parameters.json`. 
Commentary about the different parameters can be found in `parameters.py`.
Then you can run:

In version 1.0:
 - `main_mso.py` to obtain formal diagrams from signal.
 - `main_mso_char.py` to obtain formal diagrams from character strings.
 
 In version 2.0:
- `class_main.py` to obtain formal diagrams either from signal or character strings.


# How to install MORFOS:
git clone https://github.com/jcalandra/morfos.git
or download the ZIP package


# Setup Guide for macOS

This guide will help you set up Morfos on macOS using **Conda**, including all necessary dependencies.

## Install Miniconda

1. Go to the official Miniconda website: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)  
2. Download the **macOS version with Python 3.11** (avoid 3.12 or 3.13 for compatibility).  
3. Install following the instructions.  
4. Open a **new terminal** after installation.

## Initialize Conda for your shell
copy :
conda init zsh
source ~/.zshrc

## unzip MORFOS project in the folder of your choice
Then type on your shell :
cd /morfos-project/path/folder/
where '/morfos-project/path/folder/' is the path to your morfos's project folder

Copy the following lines :
conda create -n morfos_env python=3.11 -y
conda activate morfos_env
conda install -c conda-forge cmake llvm llvmlite numba -y
pip install -r requirements.txt
