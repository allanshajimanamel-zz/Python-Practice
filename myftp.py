# A FTP client.
#
# The user will be prompted to enter his or her username and password
# for the ftp server at the begining. User commands are passed uninterpreted
#  to the server.  However, the user never needs to send a PORT command.
# Rather, the client opens a port right away and sends the appropriate
# PORT command to the server. When a response code 150 is received, this
# port is used to receive the data, and when the data is exhausted, a new
# port is opened and a corresponding PORT command sent. In order to avoid
#  errors when reusing ports quickly we cycle through a number of ports
# in the 50000 range.
#
# I acknowledge that part of the code was used from pythons official demo repository at
# https://svn.python.org/projects/python/trunk/Demo/sockets/ftp.py
#

import sys, string, io
from socket import *

#Default buffer size.
BUFSIZE = 1024

# Default port numbers used by the FTP protocol.
#
FTP_PORT = 21
FTP_DATA_PORT = FTP_PORT - 1

# Change the data port to something not needing root permissions.
#
FTP_DATA_PORT = FTP_DATA_PORT + 50000


# Main program (called at the end of this file).
#
def main():
    hostname = sys.argv[1]
    control(hostname)


# Control process (user interface and user protocol interpreter).
#
def control(hostname):
    #
    # Create control connection
    #
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((hostname, FTP_PORT))
    f = s.makefile('r') # Reading the replies is easier from a file...
    #
    # Control loop
    #
    r = None
    while 1:
        code = getreply(f)
        if code in ('221', 'EOF'): break
        if code == '150':
            if cmd.startswith('RETR',0,4):
                fname = cmd[5:]
                getFileData(r,fname)
                code = getreply(f)
            elif cmd.startswith('STOR',0,4):
                fname = cmd[5:]
                sendData(r, fname)
                code = getreply(f)
            else:
                getdata(r)
                code = getreply(f)
            r = None
        if code == '230':
            r = None
        if not r:
            r = newdataport(s, f)
        if code == '530' or code == '220':
            print('Please enter the username for the server')
            cmd = getcommand()
            cmd = 'USER ' + cmd
        elif code == '331':
            print('Please enter the password for the server')
            cmd = getcommand()
            cmd = 'PASS ' + cmd
        else:
            cmd = getcommand()
        if not cmd: break
        s.send((cmd + '\r\n').encode())


# Create a new data port and send a PORT command to the server for it.
# (Cycle through a number of ports to avoid problems with reusing
# a port within a short time.)
#
nextport = 0
#
def newdataport(s, f):
    global nextport
    port = nextport + FTP_DATA_PORT
    nextport = (nextport+1) % 16
    r = socket(AF_INET, SOCK_STREAM)
    r.bind((gethostbyname(gethostname()), port))
    r.listen(1)
    sendportcmd(s, f, port)
    return r


# Send an appropriate port command.
#
def sendportcmd(s, f, port):
    hostname = gethostname()
    hostaddr = gethostbyname(hostname)
    hbytes = hostaddr.split(".")
    pbytes = [repr(port//256), repr(port%256)]
    bytes = hbytes + pbytes
    cmd = ('PORT ' + ','.join(bytes)).encode()
    s.send(cmd + ('\r\n').encode())
    code = getreply(f)


# Process an ftp reply and return the 3-digit reply code (as a string).
# The reply should be a line of text starting with a 3-digit number.
# If the 4th char is '-', it is a multi-line reply and is
# terminate by a line starting with the same 3-digit number.
# Any text while receiving the reply is echoed to the file.
#
def getreply(f):
    line = f.readline()
    if not line: return 'EOF'
    if not line.startswith('200'):
        print (line),
    code = line[:3]
    if line[3:4] == '-':
        while 1:
            line = f.readline()
            if not line: break # Really an error
            print (line),
            if line[:3] == code and line[3:4] != '-': break
    return code


# Get the data from the data connection to print.
# Mainly used for LIST command.
#
def getdata(r):
    print ('accepting data connection')
    conn, host = r.accept()
    print ('data connection accepted')
    while 1:
        data = conn.recv(BUFSIZE)
        if not data: break
        sys.stdout.write(data.decode(encoding='UTF-8'))
    print ('end of data connection')

# Get the file data from the ftp server data connection to save on the client.
# fname is the name of the file requested.
#
def getFileData(r, fname):
    print('accepting data connection')
    conn, host = r.accept()
    print('data connection accepted')
    while 1:
        data = conn.recv(BUFSIZE)
        if not data: break
        # Write binary data to a file
        with open(fname, 'ab') as f:
            f.write(data)
    print('end of data connection')

# Send the file data from the client on the data connection to save on ftp server.
# fname is the name of the file being sent.
#
def sendData(r, fname):
    print('accepting data connection')
    conn, host = r.accept()
    print('data connection accepted')
    f = open(fname, 'rb')
    l=f.read(BUFSIZE)
    print('Sending data')
    while l:
        conn.send(l)
        l=f.read(BUFSIZE)
    conn.shutdown(SHUT_WR)
    print('end of data connection')

# Get a command from the user.
#
def getcommand():
    try:
        while 1:
            line = input('myftp> ')
            if line.startswith('ls'):
                cmd = 'LIST '
            elif line.startswith('get'):
                cmd = 'RETR '+ line[4:]
            elif line.startswith('put'):
                cmd = 'STOR '+ line[4:]
            elif line.startswith('delete'):
                cmd = 'DELE '+ line[7:]
            elif line.startswith('quit'):
                cmd = 'QUIT'
            else:
                cmd = line
            if cmd: return cmd
    except EOFError:
        return ''


# Call the main program.
#
main()