# Echo server program
# this file uses encoding:utf8

import socket
import os

HOST = ''       # Symbolic name meaning the local host
PORT = 110     # Arbitrary non-privileged port

class MailServer():

    fileCount = 0
    strSize = 0
    count = 0
    dirList = None
    path = None
    path2 = None

    def __init__(self):
        ''' Initialize the mail server '''
        self.continue_request_checking = True                                   # Is the session still on?
        self.in_authorization_state = True                                      # Are we in authorization state?
        self.in_transaction_state = False                                       # Are we in transaction state?

    def create(self):
        ''' How do we create the server? '''
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          # Create the socket
            self.s.bind((HOST, PORT))                                           # Bind the host and port
            self.s.listen(1)                                                    # Hold on for 1 sek
            print 'Server running....'                                          # Print that the server is running
            print 'Waiting for requests....'                                    # Print that the server is waiting for requests
            return True                                                         # Return that server creation was a success

        except socket.error, error:                                             # If it failed...
            print "Error %1i: %1s" % (error[0], error[1])                       # Print the error
            return False                                                        # Return that server creation was a failure

    def wait_for_request(self):
        '''  How do we wait for requests? '''
        self.conn, addr = self.s.accept()                                                                          # Wait for a request

        print 'Request made by', addr, "\n"                                     # When a request comes...
        self.service_request()                                                  # service it...

    def service_request(self):
        ''' How do we check requests from the user? '''
        self.conn.send('+OK POP3 server ready\r\n')                             # Let everybody know that you are ready for the request
        print 'Server:\t+OK POP3 server ready'                                  # -""-

        while self.continue_request_checking == True:                           # Should we still be checking for requests?

            received_data = self.conn.recv(1024)                                # What does the user request?
            code, data = repr(received_data)[1:5], repr(received_data)[6:-5]    # Decipher the request

            if self.in_transaction_state:                                       # Are we in transaction mode?
                valid_request = self.check_transaction_requests(code, data)     # If yes, then check the user request

            elif self.in_authorization_state:                                   # Are we in authorization mode?
                valid_request = self.check_authorization_requests(code, data)   # If yes, then check the user request

            else:                                                               # Otherwise....
                self.continue_request_checking = False                          # Stop checking requests
                print 'WTF Mode are we in?'                                     # Are we in some mode we don't know how to handle?

            if not valid_request:                                               # Did the user make a valid request?
                self.continue_request_checking = False                          # If no, Stop checking requests
                print '\n*** WTF is a', repr(code), 'request ?? ***'            # Did we get a request we don't know how to handle?


    def check_authorization_requests(self, request, data=None):
        ''' How do we check authorization requests from the user? '''
        print "User:  \t", request, data                                        # Print the request
        valid_request = True                                                    # The request is valid unless proven otherwise

        if request == 'USER':                                                   # If the request is user login
            self.conn.send('+OK User accepted\r\n')                             # Accept
            print 'Server:\t+OK  User accepted'                                 # -""-

        elif request == 'PASS':                                                 # If the request is password
            self.conn.send('+OK Pass accepted\r\n')                             # Accept
            self.in_authorization_state = False                                 # We are no longer in authorization state?
            self.in_transaction_state = True                                    # We are now in transaction state?
            print 'Server:\t+OK Pass accepted'                                  # -""-

        elif request == 'QUIT':                                                 # If the request is Quit
            self.conn.send('+OK\r\n')                                           # Accept
            self.continue_request_checking = False                              # Stop checking requests
            print 'Server:\t+OK dewey POP3 server signing off'

        elif request == 'AUTH':
            self.conn.send('+OK')
            self.in_authorization_state = False
            self.in_transaction_state = True

        elif request == 'CAPA':
            self.conn.send('+OK')
            self.in_authorization_state = False
            self.in_transaction_state = True

        else:                                                                   # If the request was not known...
            valid_request = False                                               # Then it was an invalid request

        return valid_request                                                    # Return the outcome wether the request was valid or not


    def check_transaction_requests(self, request, data=None):
        ''' How do we check transaction requests from the user? '''
        print "User:  \t", request, data                                        # Print the request
        valid_request = True
                                                                                 # The request is valid until proven otherwise
        if request == 'STAT':

            global path
            path = os.getcwd()
            global path2
            path2 = path + os.sep +'messages'
            global dirList
            dirList = os.listdir(path2)
            global fileCount
            fileCount = dirList.__len__()
            print fileCount
            
            global count
            count = 1;
            size = fileCount*200
            global strSize
            strSize = str(size)
            
            self.conn.send('+OK '+ str(fileCount) + ' '+ strSize +'\r\n')                                     #
            print 'Server:\t+OK messages: '+ str(fileCount) + ' total size: '+ strSize                                          #

        elif request == 'UIDL':
    
            self.conn.send('+OK\r\n')
            global count
            while count<fileCount+1:
                self.conn.send(str(count)+ ' '+ dirList[count-1] + '\r\n')
                count +=1

 
            count = 1
            print 'Server:\t+OK'
            while count<fileCount+1:
                print 'Server:\t' + str(count)+ ' '+ dirList[count-1]
                count +=1

            print 'Server:\t.'
            count = 1

            self.conn.send('.\r\n')



        elif request == 'LIST':                                                 #
            self.conn.send('+OK '+ str(fileCount) + ' messages ('+strSize+ ' octets)\r\n')
            while count<fileCount+1:
                self.conn.send(str(count) + ' 200 \r\n')
                count +=1

            self.conn.send('.\r\n')
            count = 1
            print dirList                                              #
            print 'Server:\t.'                                                  #

        elif request == 'RETR':
            if int(data):
                msgCount = int(data)-1
                msg = dirList[msgCount]
                infile = open(path2+os.sep+msg)
                self.conn.send('+OK 200 octets\r\n')
                self.conn.send(infile.readline())
                self.conn.send(infile.readline())
                self.conn.send(infile.readline())
                self.conn.send(infile.readline())
                self.conn.send(infile.readline())
                self.conn.send(infile.read()+'\r\n')
                self.conn.send('.\r\n')
                print 'Server:\t+OK'
                print 'File message sent: '+ path2+os.sep+msg
                print 'Server:\t.'
                infile.close()
    



        elif request == 'DELE':
                delCount = int(data)-1
                self.conn.send('+OK\r\n')
                msg = dirList[delCount]
                os.remove(path2+os.sep+msg)
                print 'file deleted: ' + path2+os.sep+msg
                print 'Server:\t+OK'
                print 'Server:\t.'

        elif request == 'NOOP':                                                 #
            print 'NOOP'                                                        #

        elif request == 'RSET':                                                 #
            print 'RSET'                                                        #

        elif request == 'QUIT':                                                 #
            self.conn.send('+OK\r\n')                                           # Accept
            self.continue_request_checking = False                              # Stop checking requests
            print 'Server:\t+OK dewey POP3 server signing off'                  # -""-

        else:                                                                   # If the request was not known...
            valid_request = False                                               # It was an invalid request

        return valid_request                                                    # Return the outcome wether the request was valid or not


def main():
    ''' Main part of the Assignment '''
    mail_server = MailServer()                                                  # Create the Mail Server class
    server_created = mail_server.create()


                                                                            # Try to connect the Server

    if server_created:                                                          # If the server was created successfully...
        mail_server.wait_for_request()                                          # Be ready for requests...

    print '\n*** Program Stopped ***'                                           # Print that the program is over

main()
