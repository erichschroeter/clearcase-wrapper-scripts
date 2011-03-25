# Clearcase Wrapper Scripts

Contributors:	Erich Schroeter

A collection of scripts wrapping IBM ClearCase CLI tools and helper scripts
for ClearQuest administration.

## Description

These are a collection of helper scripts to increase productivity through
adding additional features to existing ClearCase CLI tools such as cleartool
and clearfsimport. Features such as recursively importing many files which
may include spaces in their absolute paths; clearfsimport fails when spaces
exist in the absolute path.

ClearQuest script(s) exist as well to help with productive administration.

## Usage

### ClearCase

These scripts should be run while in the view.

Examples:

    python /path/to/rename.py -h
    python /path/to/import.py -h
    python /path/to/rmelem.py -h

### ClearQuest

The user.py script works on the exported file from the ClearQuest User
Administration application, which should be installed via the administration
tools during installation. The basic procedure would consist of exporting
the user information to a userinfo.txt file, then running the user.py
script, and finally importing the modified userinfo.txt.

    python /path/to/user.py help
    python /path/to/user.py -h

## Installation

There is no installation for these scripts. Simply call them from somewhere
on your system.

### Prerequisites

- **Python 2.7**
- **ClearCase 7.1.2** _(I'm guessing, since that is what I've tested it on)_
    - _cleartool_
- **ClearQuest 7.1.2** _(I'm guessing, since that is what I've tested it on)_
    - User Administration application
