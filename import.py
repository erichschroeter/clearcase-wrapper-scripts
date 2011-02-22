import os
import sys
import argparse
from subprocess import call

preview = False
verbose = False
recursive = False

def main():
    # parse command line options
    parser = argparse.ArgumentParser(description='Import elements into VOB.')
    parser.add_argument('files', help='The files to be imported.', nargs='+')
    parser.add_argument('-t', '--target-vob', help='The target VOB to import into.', required=True)
    parser.add_argument('-p', '--preview', help='See what will be imported into the VOB.', type=bool, default=False)
    parser.add_argument('-r', '--recursive', help='Recursively import files into the VOB.', type=bool, default=False)
    parser.add_argument('-v', '--verbose', help='The script will print to standard out its progress.', type=bool, default=False)
    args = parser.parse_args()

    # Set the global variable values
    # these are so we can use the switches in other functions without passing them everytime
    global verbose
    verbose = args.verbose
    global preview
    preview = args.preview
    global recursive
    recursive = args.recursive

    # add processing
    for file in args.files:
        file = os.path.abspath(file)
        importElem(file, os.path.abspath(args.target_vob))
    
def importElem(file, target):
    '''
    Handles calling the clearfsimport tool.
    '''
    if os.path.isfile(file):
        if preview:
            print 'clearfsimport ' + file + ' ' + target
        else:
            call(["clearfsimport", file, target])
            vprint('imported ' + file)
    elif os.path.isdir(file):
        if recursive:
            directory = file
            vprint('recursively importing ' + directory)
            for file in os.listdir(directory):
                subpath = directory + os.sep + file
                importElem(subpath, target)
        else:
            call(["clearfsimport", file, target])
            vprint('imported ' + file)

def vprint(message):
    '''
    Prints the message to standard output if the verbose global variable is True.
    '''
    if verbose:
        print message

if __name__ == "__main__":
    main()
