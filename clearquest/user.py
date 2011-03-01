import os
import sys
import argparse
import re

preview = False
verbose = False
recursive = False

UserIndexPath = ''
UserIndex = {}
ExportedFile = ''

def main():
    # parse command line options
    parser = argparse.ArgumentParser(description='Modify user information of an exported ClearQuest User Administration file.')
    parser.add_argument('command', help='The command to issue.', nargs=1)
    parser.add_argument('-f', '--file', help='The exported ClearQuest User Administration file.', default='userinfo.txt')
    parser.add_argument('-p', '--preview', help='See what will be imported into the VOB.', action='store_true', default=False)
    parser.add_argument('-u', '--usernames', help='The username. This needs to be specified for certain commands.', nargs='+')
    parser.add_argument('-db', '--databases', help='The databases to set. This needs to be specified for the chdb command.', nargs='+')
    parser.add_argument('-v', '--verbose', help='The script will print to standard out its progress.', action='store_true', default=False)
    args = parser.parse_args()

    # Set the global variable values
    # these are so we can use the switches in other functions without passing them everytime
    global verbose
    verbose = args.verbose
    global preview
    preview = args.preview

    # add processing
    cmd = args.command[0]

    # the user.index file contains all the users in the exported userinfo.txt
    global ExportedFile
    ExportedFile = os.path.abspath(args.file)
    directory = os.path.dirname(os.path.abspath(args.file)) + os.sep
    global UserIndexPath
    UserIndexPath = directory + 'user.index'

    # Update the UserIndex since several methods rely on it
    updateUserIndex(args.file)
    UserIndex = getUserIndex()

    if cmd == 'help':
        printCommandHelp()
    elif cmd == 'ls':
        users = getUsernames()
        for user in users:
            print user
    elif cmd == 'lsf':
        users = getUsernames()
        for username in users:
            sys.stdout.write(username +' -- ' + fullnameOf(username))
    elif cmd == 'ln':
        if args.usernames:
            for username in args.usernames:
                sys.stdout.write(UserIndex[username])
        else:
            print 'Specify -u [--username] USERNAME'
    elif cmd == 'info':
        if args.usernames:
            for username in args.usernames:
                infoFor(username)
        else:
            print 'Specify -u [--username] USERNAME'
    elif cmd == 'chdb':
        if args.usernames and args.databases:
            for username in args.usernames:
                changeDatabases(username, args.databases)
        else:
            print 'Specify -u [--username] USERNAME'
    # read file and update users.index
    # put all user mappings (to line numbers) in map to efficiently access

def printCommandHelp():
    '''
    Prints the available commands to standard output.
    '''
    print 'COMMANDS:'
    print '\tls'    + '\tlists all the usernames'
    print '\tlsf'   + '\tlists all the usernames\' with full names'
    print '\tln'    + '\treturns the line number for the given username'
    print '\tinfo'  + '\tdisplays the information for the given username'
    print '\t\t-u [--username] USERNAME'
    print '\tchdb'  + '\tchanges the databases for the given username'
    print '\t\t-u [--username] USERNAME'
    print '\t\t-db [--databases] DATABASES'

def changeDatabases(username, dbs):
    '''
    Changes the databases for the given username.
    '''
    UserIndex = getUserIndex()
    #dbLineNo = int(UserIndex[username]) + 21
    dbLineNo = int(UserIndex[username]) + 19
    file = open(ExportedFile, 'r+')
    tmpFile = ExportedFile + '.tmp'

    # create the new database string
    dbStr = ''
    for db in dbs:
        dbStr += db + ' '

    regex = re.compile('(=\s)(.)+?($)')
    #sys.stdout.write(username + ' databases: ')
    with open(tmpFile, 'w') as outfile:
        for i, line in enumerate(file):
            if i == dbLineNo:
                # replace the current databases with the new
                replaceStr = regex.sub('= ' + dbStr, line)
                outfile.write(replaceStr)
            else:
                outfile.write(line)
        outfile.close()
    file.close()
    os.remove(ExportedFile)
    os.rename(tmpFile, ExportedFile)

def infoFor(username):
    '''
    Prints the info for the specified user.
    '''
    file = open(ExportedFile, 'r')
    # modify the beginning line since the line number starts at 1 instead of 0
    beginLineNo = int(UserIndex[username]) - 1
    endLineNo = beginLineNo + 20
    for i, line in enumerate(file):
        if i >= beginLineNo and i <= endLineNo:
            # we don't need to include a newline since input = output and the input has a newline
            sys.stdout.write(line)

    file.close()

def fullnameOf(username):
    '''
    Returns the full name of the given username. If the fullname does not contain
    any text, an empty string is returned.

    @param username The username to search for.
    '''
    UserIndex = getUserIndex();
    lineno = UserIndex[username];
    vprint(username + ' info starts on line ' + str(lineno))
    file = open(ExportedFile, 'r')
    # set the line number to read as the line with the fullname info
    fullnameLineNo = int(lineno) + 5
    fullname = ''
    regex = re.compile('(=\s)')
    for i, line in enumerate(file):
        if i == fullnameLineNo:
            split = re.split(regex, line)
            # by convention in the file, the line will be split into 3 if text exists in the fullname
            if len(split) > 2:
                fullname = split[2]
            else:
                fullname = ''

    file.close()
    return fullname

def getUsernames():
    '''
    Returns a list of users. This method pulls the users from the UserIndex.
    '''
    UserIndex = getUserIndex()
    users = []

    for username, lineno in UserIndex.items():
        users.append(username)

    return users

def updateUserIndex(file):
    '''
    Updates the UserIndex. Returns the number of users updated/added. This method
    does not necessarily update, but instead deletes the old UserIndex and repopulates
    it.
    @param file The exported file from ClearQuest User Administration application
    '''
    file = open(file, 'r')
    if os.path.exists(UserIndexPath):
        os.remove(UserIndexPath)
    UserIndexFile = open(UserIndexPath, 'a')

    numOfUsers = 0
    regex = re.compile('[\s=]')
    lineno = 0
    for line in file.readlines():
        lineno += 1
        # a user is specified if the line begins with 'USER'
        split = re.split(regex, line)
        if split[0] == 'USER':
            username = split[1]
            # append the username to 'user.index'
            UserIndexFile.write(username + ':' + str(lineno) + '\n')
            vprint('wrote \'' + username + ':' + str(lineno) + '\'')
            numOfUsers += 1
    return numOfUsers

def getUserIndex():
    '''
    Returns the user index which consists of a key value map where:
        key = username
        value   = line number in the exported file from ClearQuest User Administration application.
    '''
    file = open(UserIndexPath, 'r')
    global UserIndex

    if len(UserIndex) > 0:
        return UserIndex
    else:
        for line in file.readlines():
            split = line.split(':')
            username = split[0]
            lineno = split[1]
            UserIndex[username] = lineno
            vprint('added ' + username + ' to index')
    
    return UserIndex

def vprint(message):
    '''
    Prints the message to standard output if the verbose global variable is True.
    '''
    if verbose:
        print message

if __name__ == "__main__":
    main()
