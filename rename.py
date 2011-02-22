import os
import sys
import argparse
import re
import string
from subprocess import call

def main():
    # parse command line options
    parser = argparse.ArgumentParser(description='Rename files to follow a common naming convention.')
    parser.add_argument('-f', '--file', help='The name of the file.')
    parser.add_argument('-d', '--directory', help='The directory path to rename the files in. The default is the present working directory.', default='.')
    parser.add_argument('-r', '--regex', help='The regular expression to search for.', default='[\W^\.]')
    parser.add_argument('-s', '--set', help='The text to replace whenever the regular expression finds a match.', default='_')
    parser.add_argument('-l', '--lower-case', help='This flag converts all file names to lower case.', type=bool, default=False)
    parser.add_argument('-u', '--upper-case', help='This flag converts all file names to upper case.', type=bool, default=False)
    parser.add_argument('-p', '--preview', help='Prints to the console what will be changed without actually changing.', type=bool, default=False)
    parser.add_argument('-c', '--cleartool', help='Use cleartool mv to rename the files. This requires the directory the files reside in to be checked out.', type=bool, default=False)
    parser.add_argument('-v', '--verbose', help='The script will print to standard out its progress.', type=bool, default=False)
    args = parser.parse_args()

    pattern = re.compile(args.regex)

    for filename in os.listdir(args.directory):
        #print filename
        extension = ''
        split = string.rsplit(filename, '.', 1)
        if len(split) > 1 :
            # it's a file
            extension = split[1]
            newfilename = re.sub(pattern, args.set, split[0])
            newfilename = newfilename + '.'
            newfilename = newfilename + extension
            if args.lower_case :
                newfilename = string.lower(newfilename)
            if args.upper_case :
                newfilename = string.upper(newfilename)
            if args.preview :
                print newfilename
            else:
                if args.cleartool :
                    if not os.path.isfile(newfilename) :
                        call(["cleartool", "mv", filename, newfilename])
                    else:
                        print newfilename + ' already exists and is valid.'
                else:
                    os.rename(filename, newfilename)
        else:
            # it's a directory
            newfilename = re.sub(pattern, args.set, filename)
            if args.lower_case :
                newfilename = string.lower(newfilename)
            if args.upper_case :
                newfilename = string.upper(newfilename)
            if args.preview :
                print newfilename
            else:
                if args.cleartool :
                    if not os.path.isfile(newfilename) :
                        call(["cleartool", "mv", filename, newfilename])
                    else:
                        print newfilename + ' already exists and is valid.'
                else:
                    os.rename(filename, newfilename)
        
if __name__ == "__main__":
    main()
