# Echo server program
import socket
import os

HOST = ''       # Symbolic name meaning the local host
PORT = 2221     # Arbitrary non-privileged port

class MailServer():
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
        self.conn, addr = self.s.accept()                                       # Wait for a request

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
            print 'Server:\t+OK dewey POP3 server signing off'                  # -""-

        else:                                                                   # If the request was not known...
            valid_request = False                                               # Then it was an invalid request

        return valid_request                                                    # Return the outcome wether the request was valid or not


    def check_transaction_requests(self, request, data=None):
        ''' How do we check transaction requests from the user? '''
        print "User:  \t", request, data                                        # Print the request
        valid_request = True                                                    # The request is valid until proven otherwise

        if request == 'STAT':                                                   #
            self.conn.send('+OK 2 320\r\n')                                     #
            print 'Server:\t+OK 2 320'                                          #

        elif request == 'UIDL':                                                 #
            msg_1 = '1 whqtswO00WBw4144e4382sdf345f9t5JxYwZ'
            msg_2 = '2 whqtswO00sadf4WBeaslk443234dfjhauZfe'
            self.conn.send('+OK\r\n')                                           #
            self.conn.send(msg_1 + '\r\n')
            self.conn.send(msg_2 + '\r\n')
            self.conn.send('.\r\n')                                             #
            print 'Server:\t+OK'                                                #
            print 'Server:\t' + msg_1
            print 'Server:\t' + msg_2
            print 'Server:\t.'                                                  #

        elif request == 'LIST':                                                 #
            self.conn.send('+OK 2 messages (320 octets)\r\n')                   #
            self.conn.send('1 120\r\n')                                         #
            self.conn.send('2 200\r\n')                                         #
            self.conn.send('.\r\n')                                             #
            print 'Server:\t+OK 2 messages (320 octets)'                        #
            print 'Server:\t1 120'                                              #
            print 'Server:\t1 200'                                              #
            print 'Server:\t.'                                                  #

        elif request == 'RETR':                                                 #
            if int(data) == 1:
                self.conn.send('+OK 120 octets\r\n')
<<<<<<< .mine
                self.conn.send('From: John Doe <jdoe@machine.example>\r\n')
                self.conn.send('To: John Doe <jdoe@machine.example>\r\n')
                self.conn.send('Subject: Saying Hello\r\n')
                self.conn.send('Date: Fri, 21 Nov 1997 09:55:06 -0600\r\n')
                self.conn.send('Message-ID: <1234@local.machine.example>\r\n')
                self.conn.send('\nThis is a message just to say hello\r\n')
=======

                self.conn.send('.\r\n')
                print 'Server:\t+OK 120 octets'
                print 'Server:\tHere is the fucking message....'
                print 'Server:\t.'
            elif int(data) == 2:
                self.conn.send('+OK 200 octets\r\n')
                self.conn.send('Here is the beautiful message...\r\n')
                self.conn.send('.\r\n')
                print 'Server:\t+OK 200 octets'
                print 'Server:\tHere is the beautiful message...'
                print 'Server:\t.'

        elif request == 'DELE':
            if int(data) == 1:
                self.conn.send('+OK message 1 deleted')
                msg_1 = None
                print 'Server:\t+Here is the beautiful message...'
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
    server_created = mail_server.create()                                       # Try to connect the Server

    if server_created:                                                          # If the server was created successfully...
        mail_server.wait_for_request()                                          # Be ready for requests...

    print '\n*** Program Stopped ***'                                           # Print that the program is over

main()