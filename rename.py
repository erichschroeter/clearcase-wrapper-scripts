import os
import sys
import argparse
import re
import string
from subprocess import call

verbose = False
preview = False
recursive = False
lower_case = False
upper_case = False
regex = '[\W^\.]'
replace = '_'

def main():
    global regex
    global replace

    # parse command line options
    parser = argparse.ArgumentParser(description='Rename files to follow a common naming convention.')
    parser.add_argument('files', help='The files to be renamed.', nargs='+')
    #parser.add_argument('-b', '--before', help='To rename a single file, this is name of the file before renaming.')
    #parser.add_argument('-a', '--after', help='To rename a single file, this is to be the name of the file after renaming.')
    parser.add_argument('-R', '--regex', help='The regular expression to search for. Default is \'' + regex + '\'', default=regex)
    parser.add_argument('-s', '--replace', help='The text to replace whenever the regular expression finds a match. Default is \'' + replace + '\'', default=replace)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-l', '--lower-case', help='This flag converts all file names to lower case.', action='store_true', default=False)
    group.add_argument('-u', '--upper-case', help='This flag converts all file names to upper case.', action='store_true', default=False)
    parser.add_argument('-p', '--preview', help='Prints to the console what will be changed without actually changing.', action='store_true', default=False)
    parser.add_argument('-r', '--recursive', help='Recursively rename elements by entering subdirectories.', action='store_true',  default=False)
    parser.add_argument('-v', '--verbose', help='The script will print to standard out its progress.', action='store_true', default=False)
    args = parser.parse_args()

    # Set the global variable values
    # these are so we can use the switches in other functions without passing them everytime
    global verbose
    verbose = args.verbose
    global preview
    preview = args.preview
    global recursive
    recursive = args.recursive
    global lower_case
    lower_case = args.lower_case
    global upper_case
    upper_case = args.upper_case
    regex = args.regex
    replace = args.replace
    
    for filename in args.files:
        file = os.path.abspath(filename)
        renameElem(file)

def renameElem(file):
    '''
    Renames the file using the regex and replace variables.
    '''
    file = os.path.abspath(file)
    newfile = regexFileReplace(file)

    if os.path.exists(file):
        if os.path.isfile(file):
            rename(file, newfile)
        elif os.path.isdir(file):
            directory = file
            if recursive:
                for filename in os.listdir(directory):
                    subpath = directory + os.sep + filename
                    renameElem(subpath)
            else:
                rename(file, directory)
    else:
        std.stderr.write(file + ' does not exist')

def rename(file, newfile):
    '''
    Renames the first argument to the second argument. Handles checking for the
    various switches from the commandline (i.e. preview, upper-case, etc)
    '''
    newfile = regexFileReplace(file)

    if lower_case:
        newfile = toLower(newfile)
    if upper_case:
        newfile = toUpper(newfile)

    if preview:
        print 'cleartool mv ' + file + ' ' + newfile
    else:
        # handle the case when the filename == newfilename
        if not file == newfile:
            #call(["cleartool", "mv", filename, newfilename])
            vprint('renaming:: ' + file)
            vprint(' to:: ' + newfile)
        else:
            print newfile + ' already exists. Skipping it.'

def toLower(file, ext=False):
    '''
    Returns the file as lower case. This method does not conver the entire path
    to lower case.
    @param ext Include the extension in casting upper case
    '''
    if ext:
        basefilename = string.lower(os.path.basename(file))
    else:
        if hasExtension(file):
            basefilename = string.lower(getBaseFilename(file)) + '.' + getExtension(file)
        else:
            basefilename = string.lower(getBaseFilename(file))
    path = os.path.dirname(file) + os.sep
    file = path + basefilename
    return file

def toUpper(file, ext=False):
    '''
    Returns the file as upper case. This method does not conver the entire path
    to upper case.
    @param ext Include the extension in casting upper case
    '''
    if ext:
        basefilename = string.upper(os.path.basename(file))
    else:
        if hasExtension(file):
            basefilename = string.upper(getBaseFilename(file)) + '.' + getExtension(file)
        else:
            basefilename = string.upper(getBaseFilename(file))
    path = os.path.dirname(file) + os.sep
    file = path + basefilename
    return file

def regexFileReplace(file):
    '''
    Formats the filename using the regex and replace variables.
    '''
    basefilename = getBaseFilename(file)
    extension = getExtension(file)
    pattern = re.compile(regex)
    newfilename = re.sub(pattern, replace, basefilename)
    if hasExtension(file):
        newfilename = os.path.dirname(file) + os.sep + newfilename + '.' + extension
    else:
        newfilename = os.path.dirname(file) + os.sep + newfilename
    return newfilename

def getBaseFilename(file):
    '''
    Returns the base file name, excluding the extension.
    '''
    file = os.path.basename(file)
    # split the filename on a period to separate the extension
    split = string.rsplit(file, '.', 1)
    file = split[0]
    return file

def hasExtension(file):
    '''
    Returns true if the file has an extension.
    '''
    extension = getExtension(file)
    if extension == '':
        return False
    else:
        return True

def getExtension(file):
    '''
    Returns the file's extension.
    '''
    file = os.path.basename(file)
    # split the filename on a period to separate the extension
    split = string.rsplit(file, '.', 1)
    # set the default value to the guaranteed
    extension = split[0]
    if len(split) > 1:
        extension = split[1]
    else:
        extension = ''
    return extension

def vprint(message):
    '''
    Prints the message to standard output if the verbose global variable is True.
    '''
    if verbose:
        print message

if __name__ == "__main__":
    main()
