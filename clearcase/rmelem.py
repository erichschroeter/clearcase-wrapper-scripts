import os
import sys
import argparse
import string
from subprocess import call

verbose = False
force = False
preview = False
recursive = False
exceptions = []

def main():
    # parse command line options
    parser = argparse.ArgumentParser(description='Remove elements from the clearcase VOB.')
    parser.add_argument('files', nargs='+', help='The files to remove.')
    parser.add_argument('-f', '--force', help='Force the removal, otherwise you will be prompted for each file.', action='store_true', default=False)
    parser.add_argument('-e', '--exceptions', help='A list of files to exclude from removing. Format is -e="file1.txt;"file 2.txt""')
    parser.add_argument('-p', '--preview', help='Prints to the console what will be changed without actually changing.', action='store_true', default=False)
    parser.add_argument('-r', '--recursive', help='Recursively remove elements by entering subdirectories.', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', help='The script will print to standard out its progress.', action='store_true', default=False)
    args = parser.parse_args()

    # Set the global variable values
    # these are so we can use the switches in other functions without passing them everytime
    global verbose
    verbose = args.verbose
    global force
    force = args.force
    global preview
    preview = args.preview
    global recursive
    recursive = args.recursive
    global exceptions
    exceptions = getExceptions(args.exceptions)

    for filename in args.files :
        file = os.path.abspath(filename)
        rmElement(file)

def rmElement(file):
    '''
    Handles removing the element from the VOB. This calls the remove method to do the actual removing.
    '''
    file = os.path.abspath(file)
    if os.path.exists(file):
        if os.path.isfile(file):
            # TODO use regex to determine whether to remove files matching a wildcard
            if file in exceptions:
                print 'skipping ' + file
            else:
                remove(file)
        elif os.path.isdir(file):
            if recursive:
                directory = file
                for filename in os.listdir(directory):
                    subpath = directory + os.sep + filename
                    rmElement(subpath)
            else:
                remove(file)
    else:
        std.stderr.write(file + ' does not exist')

def remove(file):
    '''
    Handles checking for the various switches entered via the commandline (i.e. preview, force, etc)
    before actually 
    '''
    if force:
        if preview:
            print 'cleartool rmelem --force ' + file
        else:
            call(["cleartool", "rmelem", "-f", filename])
            vprint('removed ' + file)
    else:
        if preview:
            print 'cleartool rmelem ' + file
        else:
            call(["cleartool", "rmelem", filename])
            vprint('removed ' + file)

def getExceptions(str):
    '''
    Handles breaking the single string argument into an array of files.
    '''
    exceptions = []
    array = str.split(';')
    for file in array:
        exceptions.append(os.path.abspath(file))
    return exceptions

def vprint(message):
    '''
    Prints the message to standard output if the verbose global variable is True.
    '''
    if verbose:
        print message

if __name__ == "__main__":
    main()
