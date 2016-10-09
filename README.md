# Python-Practice
some sample programs I did in python for practice

1. myftp.py

	A simple FTP client.
	
	The user will be prompted to enter his or her username and password
	for the ftp server at the begining. User commands are passed uninterpreted
	to the server.  However, the user never needs to send a PORT command.
	Rather, the client opens a port right away and sends the appropriate
	PORT command to the server. When a response code 150 is received, this
	port is used to receive the data, and when the data is exhausted, a new
	port is opened and a corresponding PORT command sent. In order to avoid
	errors when reusing ports quickly we cycle through a number of ports
	in the 50000 range.
	
	Running instructions:
	
		You must have Python istalled in your system.
		1. Open a command line interface and navigate to the folder containing the file myftp.py
		2. Run the client file using the following command
			2.1. python myftp <ftp server hostname> eg python myftp.py inet.cis.fiu.edu
			2.2. You will be prompted to enter the username and password for the ftp server
			2.3. After successful login onto the ftp server the following commands are available for user
					2.3.1 ls -> List out ftp directory content
					2.3.2 get <filename> -> Get the file with specified name from the ftp server. e.g. get pbin.pdf
					2.3.3 put <filename> -> Put the file with specified name from the client onto the ftp server. e.g. put abcd.txt
					2.3.4 delete <filename> -> Delete the specified file from the ftp server. e.g. delete abcd.txt
					2.3.5 quit -> Quit the connection to the ftp server
